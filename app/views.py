"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

from app.forms import TranslationRequestForm
from app.models import TranslationRequest
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



def translation_request_view(request):
    if request.method == 'POST':
        form = TranslationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a success page or do any other processing.
    else:
        form = TranslationRequestForm()
    
    return render(request, 'app/translation_request_form.html', {'form': form})





def translation_request_dashboard(request):
    # Retrieve all submitted requests from the database
    submitted_requests = TranslationRequest.objects.all()

    return render(request, 'app/translation_request_dashboard.html', {'submitted_requests': submitted_requests})

