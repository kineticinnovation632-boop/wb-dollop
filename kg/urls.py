from django.urls import path
from . import views

app_name = 'kg'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about-us/', views.about_view, name='about-us'),
    path('contact-us/', views.contact_us_view, name='contact-us'),
    path('licence/', views.licence_view, name='licence'),
    path('codes/', views.issued_codes_view, name='codes'),
    path('events/', views.events_view, name='events'),
    path('incident/', views.incident_view, name='incident'),
    path('kerc-form/', views.kerc_form_view, name='kerc-form'),
    path('tips/', views.tips_view, name='tips'),
    path('complaint/', views.complaints_view, name='complaint'),
    path('news/', views.news_view, name='news'),
    path('order/', views.order_view, name='order'),
    path('petition/', views.petition_view, name='petition'),
    path('regulations/', views.regulation_view, name='regulations'),
    path('standard/', views.standard_view, name='standard'),
    path('right-obligation/', views.obligation_view, name='right-obligation'),
    path('search_result/', views.search_result_view, name='finder'),
    path('mini-grid/', views.minigrid_view, name='mini-grid'),
    path('market-document/', views.market_documents_view, name='market-document'),   
    path('regulation-documents/', views.home_view, name='regulation-documents'),   
    path('<str:person_id>/read-more/', views.readmore_view, name='read-more'),   
    path('<str:blog_id>/blog/', views.blog_view, name='blog'),
    path('regulation/<str:id>/read-more/', views.read_regulation_view, name='read-regulation'),
    path('<str:id>/reviews', views.add_comment_view, name='reviews'),
    path('exclusivity/developer-list/', views.exclusivity_view, name='exclusivity'),
    path('exclusivity/<str:slug>/sites/', views.exclusivity_detail_view, name='developer-site'),
    
]