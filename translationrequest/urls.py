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
    path('translation_request/', views.translation_request_view, name='translation_request'),
    path('translationrequestdashboard/', views.translation_request_dashboard, name='translationrequestdashboard'),
   
   
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
    path('upload_files/<int:client_id>/', views.upload_files, name='upload_files'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)