"""
Definition of urls for translationrequest.
"""
from django.conf import settings
from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

   
   
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),

    path('faq/', views.faq, name='faq'),
    path('services/', views.services, name='services'),
 
    path('tracker/', views.translation_tracker, name='translation_tracker'),
   


    path('create_client/', views.create_client, name='create_client'),
    path('client/<int:client_id>/', views.client_dashboard, name='client_dashboard'),
    path('client/<int:client_id>/create_request/', views.create_translation_request, name='create_translation_request'),
    #dddpath('client/request/<int:request_id>/upload_files/', views.upload_files_for_request, name='upload_files_for_request'),
    path('view_client_requests/<int:pk>/', views.view_client_requests, name='view_client_requests'),
     # View Translation Request Details
    path('request/<int:request_id>/', views.view_translation_request, name='view_translation_request'),
    path('request/all/', views.translation_request_all, name='translation_request_all'),
    path('extract_text/<int:file_id>/', views.extract_text, name='extract_text'),
    path('list_clients/', views.list_clients, name='list_clients'),

  
    path('request/<int:request_id>/files/', views.request_files, name='request_files'),
    path('request/<int:request_id>/file/<int:file_id>/', views.file_details, name='file_details'),
    path('request/<int:request_id>/file/<int:file_id>/download/', views.download_file, name='download_file'),
    path('request/<int:request_id>/file/<int:file_id>/updatestatus/', views.update_file_status, name='update_file_status'),
    path('request/<int:request_id>/file/<int:file_id>/message/', views.message_user_about_file, name='message_user_about_file'),
    path('request/<int:request_id>/file/<int:file_id>/delete/', views.delete_file, name='delete_file'),
    path('request/<int:request_id>/file/<int:file_id>/upload/', views.upload_translated_file, name='upload_translated_file'),
    path('view_files_by_status/<int:client_id>/<int:request_id>/<str:status>/', views.view_files_by_status, name='view_files_by_status'),
    path('generate_receipt/', views.generate_fictional_receipt, name='generate_receipt'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),
    path('view_client_files/<int:pk>/', views.view_client_files, name='view_client_files'),
    path('sandbox', views.sandbox, name='sandbox')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)