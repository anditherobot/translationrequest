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
    path('tracker/', views.translation_tracker, name='tracker'),

   


    path('create_client/', views.create_client, name='create_client'),
    path('client/<int:client_id>/', views.client_dashboard, name='client_dashboard'),
    path('client/<int:client_id>/create_request/', views.create_translation_request_view, name='create_translation_request'),

    path('client/request/<int:request_id>/upload_files/', views.upload_files_for_request, name='upload_files_for_request'),

     # View Translation Request Details
    path('request/<int:request_id>/', views.view_translation_request, name='view_translation_request'),
    path('list_clients/', views.list_clients, name='list_clients'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)