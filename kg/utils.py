from datetime import datetime
import re
from django.conf import settings
import requests
import json, math

class KgHelper:
    def __init__(self):
        self.url = f"{settings.URL_ADDRESS}/api/v1"
        self.root_url = settings.URL_ADDRESS
        self.page_count = 10
        self.page_modal = None
        self.req = None
        self.modal = None
        self.required_fields = ['name', 'email', 'subject', 'message']  # Example required fields

    def get_route(self, id=None, **kwargs):
        if self.modal:
            url = f"{self.url}/{self.modal}/"
            if id is not None:
                url += f"{id}/"
            # Create query parameters based on kwargs
            query_params = []
            for key, value in kwargs.items():
                if value is not None:
                    query_params.append(f"{key}={value}")
            if query_params:
                url += '?' + '&'.join(query_params)
               
            if self.req:
                hs_q = url.__contains__('?')
                srch = self.req.get('srch')
                pg = self.req.get('pg')
                if srch:
                    url = hs_q and f"{url}&srch={srch}" or f"{url}?srch={srch}"
                    search = srch
                    self.search_title = srch
                if pg:
                    url = hs_q and f"{url}&page={pg}" or f"{url}?page={pg}"
            return url
        
    def get_page_numbering(self, count=0):
        page = []
        if count>0 and count>self.page_count:
            pg = 1
            if self.req:
                pg = self.req.get('pg', 1)
                if isinstance(pg, str) and pg.isdigit():
                    pg = int(pg)
                elif isinstance(pg, list) and len(pg)>0 and str(pg[0]).isdigit():
                    pg = int(pg[0])
            rng = math.ceil(count/self.page_count)
            for i in range(rng):
                page.append({ 'label': i+1, 'active_page': pg, 'url_name': self.page_modal or self.modal })
        return page
    
    def format_date_time(self, item):
        published_at = item.get('published_at')
        event_date = item.get('event_date')
        try:
            if published_at:
                published_date = datetime.fromisoformat(published_at)
                item['published_at'] = published_date.strftime('%B %d, %Y')
                item['published_time'] = published_date.strftime('%I:%M %p')
            if event_date:
                event_date_obj = datetime.fromisoformat(event_date)
                item['event_date'] = event_date_obj.strftime('%B %d, %Y')
                item['event_time'] = event_date_obj.strftime('%I:%M %p') 
            return item
        except Exception as e:
            print(f"Error formatting date/time: {e}")
            return item
    
    def has_page_contents(self, posts):
        page_contents = posts.get('page_contents', []) if posts and isinstance(posts, dict) else []
        if page_contents and isinstance(page_contents, list) and len(page_contents) > 0:
            for pg_item in page_contents:
                content = pg_item.get('content')
                pg_item['content'] = self.format_post_content(content)
            # Arrange the page content by title and return the results
            page_contents = self.arrange_page_content_by_title(page_contents)
        return page_contents

    
    def categorize_posts_by_type(self, posts):
        categorized_posts = {
            'news': [],
            'events': [],
            'featured_posts': []
        }
        if posts and isinstance(posts, dict):
            results = posts.get('results', [])
            page_contents = self.has_page_contents(posts)
            if page_contents:
                categorized_posts['page_contents'] = page_contents
            
            for post in results:
                post_type = post.get('post_type')
                if post.get('feature_post') == 'FEATURED':
                    categorized_posts['featured_posts'].append(post)
                elif post_type == 'NEWS':
                    categorized_posts['news'].append(post)
                elif post_type == 'EVENT':
                    categorized_posts['events'].append(post)
                
                # Format the content of each post
                if post.get('content'):
                    post['content'] = self.format_post_content(post['content'])
        return categorized_posts

    def get_news_and_pinned_events(self, posts):
        categorized_posts = {
            'event': None,
            'upcoming_events': [],
            'featured_posts': [],
            'draft': [],
            'news': [],
            'page_contents': self.has_page_contents(posts)
        }

        if posts and isinstance(posts, dict):
            results = posts.get('results', [])
            
            for post in results:       
                post_type = post.get('post_type')
                post_status = post.get('event_status')
            
                if post_status == 'PINNED':
                    categorized_posts['event'] = post
                elif post.get('feature_post') == 'FEATURED' or post.get('regulation_type') == 'DRAFT':
                    categorized_posts['featured_posts'].append(post)
                elif post_type == 'NEWS':
                    categorized_posts['news'].append(post)
                elif post_type == 'EVENT' and post_status == 'UPCOMING':
                    categorized_posts['upcoming_events'].append(post)

                # Format the content of each post
                if post.get('content'):
                    post['content'] = self.format_post_content(post['content'])
        return categorized_posts
    
    def add_pages_to_response_data(self, data):
        if isinstance(data, dict):
            results = data.get('results', [])
            # Format the date and time for each item in the results
            for item in results:
                self.format_date_time(item)
            # Add pagination information to the response data
            count = data.get('count', 0)
            pages = self.get_page_numbering(count=count)
            data['pages'] = pages
        return data
    
    def get_posts(self, route):
        try:
            response = requests.get(route)
            if response.status_code == 200:
                data = response.json()
                return self.add_pages_to_response_data(data)
        except Exception as e:
            print(f"Error fetching post: {e}")
        return None
    
    def get_documents(self, route):
        try:
            response = requests.get(route)
            if response.status_code == 200:
                data = response.json()
                return self.add_pages_to_response_data(data)
        except Exception as e:
            print(f"Error fetching document: {e}")
        return None
    
    def post_document(self, route, payload):
        # Check if required fields are present in the payload
        missing_fields = [field for field in self.required_fields if field not in payload]
        if missing_fields:
            missing_fields_str = ', '.join(missing_fields)
            return {'error': f'Missing required fields: {missing_fields_str}', 'status_code': 400 }
        try:
            res = requests.post(url=route, 
                                data=json.dumps(payload),
                                headers={'Content-Type': 'application/json'})
            data = res.json()
            
            if data and res.status_code in [200, 201]:
                return {'success': 'Document posted successfully', 'data': data, 'status_code': res.status_code }
            elif res.status_code != 200:
                return {'error': f'Failed to post document: {data}', 'status_code': res.status_code }
        except Exception as e:
             print(e)
             return {'error': 'Failed to post document', 'details': str(e), 'status_code': getattr(e.response, 'status_code', None)}
        return None
    
    def arrange_by_office(self, persons):
        chairman = None
        commissioners = []
        secretary = None
        for person in persons:
            if person.get('office') == 'Chairman / CEO':
                chairman = person
            elif person.get('office') == 'Commission Secretary':
                secretary = person
            else:
                commissioners.append(person)
        return {
            'chairman': chairman,
            'secretary': secretary,
            'commissioners': commissioners
        }

    def format_post_content(self, content):
        if content:
            # Split the content into paragraphs based on newlines and carriage returns  
            paragraphs = re.split(r'(?:\r\n\n|\r\n\r\n|\r\n|\n|\r)', content)
            formatted_paragraphs = []
            if len(paragraphs) > 0:
                # Remove any empty paragraphs
                for paragraph in paragraphs:
                    if paragraph.strip() == '':
                        paragraphs.remove(paragraph)
                    # Remove any leading or trailing whitespace from each paragraph
                    paragraph = paragraph.strip()
                    # Look for any '*..*' characters in the paragraph and bold the text that is between them
                    bold_texts = re.findall(r'\*(.*?)\*', paragraph)                    
                    for bold_text in bold_texts:
                        paragraph = paragraph.replace(f'*{bold_text}*', f'<strong>{bold_text}</strong>')                    
                    # Look for any '_.._' characters in the paragraph and italicize the text that is between them
                    italic_texts = re.findall(r'_(.*?)_', paragraph)
                    for italic_text in italic_texts:
                        paragraph = paragraph.replace(f'_{italic_text}_', f'<i>{italic_text}</i>')
                    # Look for any '~..~' characters in the paragraph and strikethrough the text that is between them
                    strikethrough_texts = re.findall(r'~(.*?)~', paragraph)
                    for strikethrough_text in strikethrough_texts:
                        paragraph = paragraph.replace(f'~{strikethrough_text}~', f'<s>{strikethrough_text}</s>')
                    # look for any paragraphs that start with '-#..#' and convert to orders list items    
                    list_items = re.findall(r'-#(.*?)#', paragraph)
                    if list_items:
                        list_html = '<ul>'
                        for list_i in list_items:
                            list_html += f'<li>{list_i.strip()}</li>'
                            paragraph = paragraph.replace(f'-#{list_i}#', '')
                        list_html += '</ul>'
                        paragraph += list_html
                    # look for any paragraphs that start with '#-..#' and convert to unordered list items
                    list_items = re.findall(r'#-(.*?)#', paragraph)
                    if list_items:
                        list_html = '<ol>'
                        for list_i in list_items:
                            list_html += f'<li>{list_i.strip()}</li>'
                            paragraph = paragraph.replace(f'#-{list_i}#', '')
                        list_html += '</ol>'
                        paragraph += list_html
                    # Look for any '>' characters in the paragraph and convert them to blockquotes
                    blockquotes = re.findall(r'>(.*?)\n', paragraph)
                    for blockquote in blockquotes:
                        paragraph = paragraph.replace(f'>{blockquote}\n', f'<blockquote>{blockquote.strip()}</blockquote>')

                    # Look for any '---' characters in the paragraph and convert them to horizontal rules
                    if '---' in paragraph:
                        paragraph = paragraph.replace('---', '<hr>')
                    # Look for any '***' characters in the paragraph and convert them to horizontal rules
                    if '***' in paragraph:
                        paragraph = paragraph.replace('***', '<hr>')
                    
                    # Look for any URLs in the paragraph and convert them to clickable links
                    urls = re.findall(r'(https?://\S+)', paragraph)
                    for url in urls:
                        paragraph = paragraph.replace(url, f'<a href="{url}" target="_blank">{url}</a>')
                    # Look for any email addresses in the paragraph and convert them to clickable mailto links
                    emails = re.findall(r'[\w\.-]+@[\w\.-]+', paragraph)
                    for email in emails:
                        paragraph = paragraph.replace(email, f'<a href="mailto:{email}">{email}</a>')
                    formatted_paragraphs.append(paragraph)
            return formatted_paragraphs
        return []

    def download_file(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.content
        except Exception as e:
            print(f"Error downloading file: {e}")
        return None

    def update_page_content(self, pg_contents):
        if pg_contents and isinstance(pg_contents, list) and len(pg_contents) > 0: 
            for pg_item in pg_contents:
                content = pg_item.get('content')
                pg_item['content'] = self.format_post_content(content)
            # Arrange the page content by title and return the results
            results = self.arrange_page_content_by_title(pg_contents)
            return results
        return None
    

    
    def get_page_content(self, page_name):
        route = f"{self.url}/page-contents/?wb={page_name}"
        try:
            res = requests.get(url=route, 
                                headers={'Content-Type': 'application/json'})
            data = res.json()
            if data:
                if data and isinstance(data, dict) and 'page_contents' in data and len(data['page_contents']) > 0:
                    results = data['page_contents']
                    # Loop through and format the content of each item in the results
                    for item in results:
                        content = item.get('content')
                        item['content'] = self.format_post_content(content)
                    # Arrange the page content by title and return the results
                    results = self.arrange_page_content_by_title(results)
                    return results
                return None
        except requests.exceptions.RequestException as e:
             print(e)
             return {'error': 'Failed to fetch page content', 'details': str(e), 'status_code': getattr(e.response, 'status_code', None)}
        return None
    
    def arrange_page_content_by_title(self, contents):
        arranged_content = {}
        if contents and isinstance(contents, list):
            for content in contents:
                content_list = content.get('content_list', [])
                # Loop through and format the content of each item in the content_list
                for clist in content_list:
                    clist['content_objs'] = self.create_object_with_symbol_from_paragraph(clist.get('content', ''))
                slug = content['slug'] if 'content' in content and 'slug' in content else None
                if slug:
                    # replace any '-' with '_' in the content['slug'] and convert to lowercase
                    slug_title = slug.replace('-', '_').lower()
                    if slug:
                       slug = slug_title
                    arranged_content[slug] = content
        return arranged_content
    
    def create_object_with_symbol_from_paragraph(self, paragraph):
        # Look for any '-{..}' characters in the paragraph and convert them to a dictionary object
        symbols = re.findall(r'\{(.*?)\}', paragraph)
        obj_list = []
    
        for symbol in symbols:
            # Split the symbol by ':' and convert to a dictionary object
            if ':' in symbol:
                obj_array = symbol.split(':', 1)
                if len(obj_array) == 2:
                    title = obj_array[0].strip()
                    content = obj_array[1].strip()
                    typ = 'text'
                    if content and ',' in content:
                        content = [c.strip() for c in content.split(',')]
                        typ = 'list'
                    
                    obj_list.append({'title': title, 'content': content, 'type': typ})
        return obj_list