"""
Definition of views.
"""
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse    
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpRequest
from ..models import ClientInfo, TranslationRequest, ClientFile
from ..forms import ClientInfoForm, TranslationRequestForm, ClientFileForm
import mimetypes, os
from ..notification_utils import send_email_receipt, notify_admin
from django.http import JsonResponse




def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def faq(request):
    return render(request, 'app/faq.html')

def services(request):
    return render(request, 'app/services.html')

def terms_conditions(request):
        return HttpResponse("Faq and stuff here, accept" )

