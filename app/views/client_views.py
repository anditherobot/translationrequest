"""
Definition of views.
"""
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse    
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpRequest
from ..models import ClientInfo, TranslationRequest, ClientFile, UserProfile
from ..forms import ClientInfoForm, TranslationRequestForm, ClientFileForm
import mimetypes, os
from ..notification_utils import send_email_receipt, notify_admin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



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


@login_required
def scene_list(request):
    # Retrieve scenes associated with the logged-in user
    user_profile = UserProfile.objects.get(user=request.user)
    scenes = user_profile.scenes.all()

    return render(request, 'app/scenes.html', {'scenes': scenes})

