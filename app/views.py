"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.mail import send_mail
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

            send_email_receipt(form.cleaned_data)
            notifyadmin();
            #flash message , clean form or redirect to receipt page. 
            #add detail about an emila has been sent. 

            return redirect('translationrequestdashboard')
            # Redirect to a success page or do any other processing.
    else:
        form = TranslationRequestForm()
    
    return render(request, 'app/translation_request_form.html', {'form': form})



def send_email_receipt(form_data):
    # Format the email content using the form data
    subject = 'Translation Request Receipt'
    message = f'Thank you for your translation request!\n\n' \
              f'Here are the details of your request:\n' \
              f'First Name: {form_data["first_name"]}\n' \
              f'Last Name: {form_data["last_name"]}\n' \
              f'Company: {form_data["company"]}\n' \
              f'Email: {form_data["email"]}\n' \
              f'Phone Number: {form_data["phone_number"]}\n' \
              # Include other relevant form fields here

    # Send the email
    send_mail(subject, message, 'your_email@example.com', [form_data['email']])


from django.core.mail import send_mail

def notifyadmin():
    subject = "New Translation Request Submitted"
    message = "A new translation request has been submitted on the website."
    recipient_list = ["admin@example.com"]  # Replace with the admin's email address

    # Using Django's built-in send_mail function
    send_mail(subject, message, "your_email@example.com", recipient_list)


def translation_request_dashboard(request):
    # Retrieve all submitted requests from the database
    submitted_requests = TranslationRequest.objects.all()

    return render(request, 'app/translation_request_dashboard.html', {'submitted_requests': submitted_requests})


def faq(request):
    return render(request, 'app/faq.html')

