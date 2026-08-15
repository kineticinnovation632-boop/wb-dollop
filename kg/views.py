from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .utils import KgHelper


# Create your views here. 
def home_view(request):
    url = 'kg/pages/home/home.html'
    apiH = KgHelper()
    apiH.req = request.GET

    if request.method == 'POST':
        form = request.POST
        apiH.modal = 'contact-messages'
        route = apiH.get_route()
        post = apiH.post_document(route=route, payload=form)       
        if post and post.get('error'):
            messages.error(request, post['error'])
        else: 
            messages.success(request, post.get('success') or 'Your submission was successful...')
        
    # Get pinned event and news
    apiH.modal = 'posts'
    route = apiH.get_route(wb='hm', pgd='HOME')
    posts = apiH.get_posts(route=route) or []
    context = apiH.get_news_and_pinned_events(posts=posts)
    return render(request, url, context)
        
def about_view(request):
    url = 'kg/pages/about-us/about-us.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'board-members'
    
    route = apiH.get_route(pgd='ABOUT')
    persons = apiH.get_documents(route=route) or []
    pages = persons.get('pages', []) if persons else []
    results = persons.get('results', []) if persons else []
    arrange_personel = apiH.arrange_by_office(results)
    page_contents = apiH.has_page_contents(persons)

    return render(request, url, {'persons': arrange_personel, 'pages': pages, 'page_content': page_contents })
        
 
def regulation_view(request):
    url = 'kg/pages/regulations/regulations.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'regulations'

    route = apiH.get_route(wb='REGULATION')
    regulations = apiH.get_documents(route=route) or []
    pages = regulations.get('pages', []) if regulations else []
    results = regulations.get('results', []) if regulations else []
    
    return render(request, url, {'documents': results, 'pages': pages, 'title': 'Standard & Regulation'})

def issued_codes_view(request):
    url = 'kg/pages/regulations/codes.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'regulations'
    apiH.page_modal = 'codes'

    route = apiH.get_route(wb='CODES')
    codes = apiH.get_documents(route=route) or []
    pages = codes.get('pages', []) if codes else []
    results = codes.get('results', []) if codes else []
    return render(request, url, {'documents': results, 'pages': pages, 'title': 'Issued Codes'})

def market_documents_view(request):
    url = 'kg/pages/regulations/market-doc.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'regulations'
    apiH.page_modal = 'market-document'

    route = apiH.get_route(wb='MARKET')
    market = apiH.get_documents(route=route) or []
    pages = market.get('pages', []) if market else []
    results = market.get('results', []) if market else []
    return render(request, url, {'documents': results, 'pages': pages, 'title': 'Market'})

def order_view(request):
    url = 'kg/pages/regulations/order.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'regulations'
    apiH.page_modal = 'order'

    route = apiH.get_route(wb='ORDER')
    order = apiH.get_documents(route=route) or []
    pages = order.get('pages', []) if order else []
    results = order.get('results', []) if order else []
    return render(request, url, {'documents': results, 'pages': pages, 'title': 'Order'})        

def standard_view(request):
    url = 'kg/pages/regulations/standard.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'regulations'
    apiH.page_modal = 'standard'

    route = apiH.get_route(wb='STANDARDS')
    standard = apiH.get_documents(route=route) or []
    pages = standard.get('pages', []) if standard else []
    results = standard.get('results', []) if standard else []

    return render(request, url, {'documents': results, 'pages': pages, 'title': 'Standard & Rules'})

def kerc_form_view(request):
    url = 'kg/pages/regulations/kerc-form.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'regulations'
    apiH.page_modal = 'kerc-form'

    route = apiH.get_route(wb='FORMS')
    manual = apiH.get_documents(route=route) or []
    pages = manual.get('pages', []) if manual else []
    results = manual.get('results', []) if manual else []
    return render(request, url, {'documents': results, 'pages': pages, 'title': 'Forms & Manuals'})

def read_regulation_view(request, id):
    url = 'kg/pages/regulations/sections/document-post.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'regulations'
    route = apiH.get_route(id=id)
    regulation = apiH.get_documents(route=route) or {}

    if regulation and isinstance(regulation, dict) and 'slug' in regulation:
        regulation['description'] = apiH.format_post_content(regulation['description'])
        # Format the published_at field to a more readable format
        if 'published_at' in regulation:
            try:
                regulation['published_at'] = apiH.format_date_time({'published_at': regulation['published_at']})['published_at']
            except Exception as e:
                print(f"Error formatting date: {e}")
    return render(request, url, {'regulation': regulation, 'review_id':id })

def exclusivity_view(request):
    url = 'kg/pages/exclusivity/developers.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'exclusivity-developers'
    apiH.page_modal = 'exclusivity'
    route = apiH.get_route()
    exclusivity = apiH.get_documents(route=route) or []
    pages = exclusivity.get('pages', []) if exclusivity else []
    results = exclusivity.get('results', []) if exclusivity else []
    
    return render(request, url, {'developers': results, 'pages': pages, 'title': 'Exclusivity'})

def exclusivity_detail_view(request, slug):
    url = 'kg/pages/exclusivity/sites.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'exclusivity-developers'
    route = apiH.get_route(id=slug)
    developer = apiH.get_documents(route=route) or {}
    sites = developer.get('sites', []) if developer else []
    
    return render(request, url, {'developer': developer, 'sites': sites })


def news_view(request):
    url = 'kg/pages/posts/news.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'posts'
    apiH.page_modal = 'news'
    route = apiH.get_route(wb='NEWS', pgd='NEWS', srch='hm-news')
    news = apiH.get_documents(route=route) or []
    pages = news.get('pages', []) if news else []
    context = apiH.categorize_posts_by_type(posts=news)

    context['pages'] = pages
    return render(request, url, context)

def events_view(request):
    url = 'kg/pages/posts/events.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'posts'
    apiH.page_modal = 'events'

    route = apiH.get_route(wb='EVENT', pgd='EVENT', srch='hm-event')
    events = apiH.get_documents(route=route) or []
    pages = events.get('pages', []) if events else []
    context = apiH.categorize_posts_by_type(posts=events)
    context['pages'] = pages
    return render(request, url, context)  

def blog_view(request, blog_id):
    url = 'kg/pages/posts/blog.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'posts'
    review_id = None
    route = apiH.get_route(id=blog_id, wb='adimg')
    blog = apiH.get_documents(route=route) or {}
    if blog and isinstance(blog, dict) and 'slug' in blog:
        review_id = blog.get('id')
        blog['content'] = apiH.format_post_content(blog['content'])
        # Format the published_at field to a more readable format
        if 'published_at' in blog:
            try:
                blog['published_at'] = apiH.format_date_time({'published_at': blog['published_at']})['published_at']
            except Exception as e:
                print(f"Error formatting date: {e}")
    return render(request, url, {'blog': blog, 'review_id': review_id})


def add_comment_view(request, id, signal='post'):
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'reviews'
    if request.method == 'POST':
        form = request.POST
        payload = {
            'name': form.get('name'),
            'email': form.get('email'),
            'subject': form.get('subject'),
            'comment': form.get('message'),
            'rating': form.get('rating') or 1.5,
            'message': form.get('message'),
        }
        if signal == 'post':
            payload['post'] = id
        elif signal == 'regulation':
            payload['regulation'] = id

        if not payload['name'] or not payload['email'] or not payload['comment']:
            messages.error(request, 'Make sure you fill out all the required fields')
        else:
            try:
                res = apiH.post_document(route=apiH.get_route(), payload=payload)
                if res and res.get('error'):
                    messages.error(request, res['error'])
                else:
                    # Use signal to return to the appropriate page after submission
                    messages.success(request, res.get('success') or 'Your review submission was successful')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            except Exception as e:
                messages.error(request, f'Your review submission was not successful: {str(e)}')
        return redirect(request.META.get('HTTP_REFERER', '/'))

def contact_us_view(request):
    url = 'kg/pages/contact-us.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'contact-messages'
    if request.method == 'POST':
        form = request.POST
        payload = {
            'name': form.get('name'),
            'email': form.get('email'),
            'subject': form.get('subject'),
            'message': form.get('message'),
            'phone_number': form.get('phone_number'),
        }
        if not payload['name'] or not payload['email'] or not payload['message'] or not payload['phone_number']:
            messages.error(request, 'Make sure you fill out all the required fields')
        else:
            try:
                res = apiH.post_document(route=apiH.get_route(), payload=payload)
                if res and res.get('error'):
                    messages.error(request, res['error'])
                else:
                    messages.success(request, res.get('success') or 'Your submission was successful...')
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            except Exception as e:
                messages.error(request, f'Your submission was not successful: {str(e)}')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, url, {})


def search_result_view(request):
    url = 'kg/pages/posts/search_results.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'regulations'
    search_query = request.GET.get('srch', '')
    route = apiH.get_route(adost=search_query, srch=search_query)
    search_results = apiH.get_documents(route=route) or {}
    pages = search_results.get('pages', []) if search_results else []
    results = search_results.get('results', []) if search_results else []
    searched_posts = search_results.get('searched_posts', []) if search_results else []
    return render(request, url, {'results': results, 'pages': pages, 'search_query': search_query, 'searched_posts': searched_posts})

def readmore_view(request, person_id):
    url = 'kg/pages/posts/readmore.html'
    apiH = KgHelper()
    apiH.req = request.GET
    apiH.modal = 'board-members'

    route = apiH.get_route(search=person_id)
    person = apiH.get_documents(route=route) or {}
    result = person.get('results', []) if person else {}
    if result and len(result)>0:
        result = result[0]
        # Format the content fields using the helper function
        result['intro'] = apiH.format_post_content(result['intro'])
        result['career'] = apiH.format_post_content(result['career'])
        result['education'] = apiH.format_post_content(result['education'])
    return render(request, url, {'data': result})

def licence_view(request):
    url = 'kg/pages/services/licence.html'
    apiH = KgHelper()
    apiH.req = request.GET
    page_contents = apiH.get_page_content('SERVICES')
    return render(request, url, {'title': 'Licensing & Authorization', 'page_content': page_contents})

def minigrid_view(request):
    url = 'kg/pages/services/mini-grid.html'
    apiH = KgHelper()
    apiH.req = request.GET
    page_contents = apiH.get_page_content('SERVICES')
    return render(request, url, {'title': 'Mini Grids', 'page_content': page_contents})

def petition_view(request):
    url = 'kg/pages/services/petition.html'
    apiH = KgHelper()
    apiH.req = request.GET
    page_contents = apiH.get_page_content('SERVICES')
    return render(request, url, {'title': 'Petition Hearing', 'page_content': page_contents})

def complaints_view(request):
    url = 'kg/pages/needhelp/complaint.html'
    apiH = KgHelper()
    apiH.req = request.GET
    page_contents = apiH.get_page_content('HELP')
    return render(request, url, {'title': 'Consumer Complaints', 'page_content': page_contents})

def incident_view(request):
    url = 'kg/pages/needhelp/incident.html'
    apiH = KgHelper()
    apiH.req = request.GET
    page_contents = apiH.get_page_content('HELP')
    return render(request, url, {'title': 'How to report an accident', 'page_content': page_contents})

def tips_view(request):
    url = 'kg/pages/needhelp/tips.html'
    apiH = KgHelper()
    apiH.req = request.GET
    page_contents = apiH.get_page_content('HELP')
    return render(request, url, {'title': 'Tips for Consumers', 'page_content': page_contents})

def obligation_view(request):
    url = 'kg/pages/needhelp/rights-obligation.html'
    apiH = KgHelper()
    apiH.req = request.GET
    page_contents = apiH.get_page_content('HELP')
    return render(request, url, {'title': 'Rights & Obligations', 'page_content': page_contents})

