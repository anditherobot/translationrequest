"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpRequest
from django.core.mail import send_mail
from app.forms import TranslationRequestForm
from app.models import TranslationRequest, ClientFiles, ClientInfo
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
    form = TranslationRequestForm(request.POST or None, request.FILES or None)
    #form.helper.template = 'app/custom_crispy_form.html'

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            send_email_receipt(form.cleaned_data)
            notifyadmin()
            # Flash message, clean form or redirect to receipt page.
            # Add details about an email has been sent.

            return redirect('translationrequestdashboard')
            # Redirect to a success page or do any other processing.

    return render(request, 'app/translation_request_form.html', {'form': form})




def send_email_receipt(form_data):
    # Format the email content using the form data
    subject = 'Translation Request Receipt'
    message = f'Thank you for your translation request!\n\n' \
              f'Here are the details of your request:\n' \
              f'First Name: {form_data["first_name"]}\n' \
              f'Last Name: {form_data["last_name"]}\n' \
              f'Email: {form_data["email"]}\n' \
              f'Phone Number: {form_data["phone_number"]}\n' \
              # Include other relevant form fields here

    # Send the email
    send_mail(subject, message, 'info@example.com', [form_data['email']])


from django.core.mail import send_mail

def notifyadmin():
    subject = "New Translation Request Submitted"
    message = "A new translation request has been submitted on the website."
    recipient_list = ["info@mokreyol.com"]  # Replace with the admin's email address

    # Using Django's built-in send_mail function
    send_mail(subject, message, "info@mokreyol.com", recipient_list)


def translation_request_dashboard(request):
    # Retrieve all submitted requests from the database
    submitted_requests = TranslationRequest.objects.all()

    return render(request, 'app/translation_request_dashboard.html', {'submitted_requests': submitted_requests})


def faq(request):
    return render(request, 'app/faq.html')

def services(request):
    return render(request, 'app/services.html')

def translation_tracker(request):
    return render(request, 'app/translation_tracker.html')


from django.shortcuts import render, redirect
from .forms import ClientInfoForm, ClientFilesForm

def create_client(request):
    if request.method == 'POST':
        form = ClientInfoForm(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect('client_dashboard', client_id=client.pk)
    else:
        form = ClientInfoForm()
    return render(request, 'app/create_client.html', {'form': form})

def upload_files(request, client_id):
    client = ClientInfo.objects.get(pk=client_id)

    if request.method == 'POST':
        form = ClientFilesForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data['file']
            for file in files:
                ClientFiles.objects.create(client=client, file=file)
        # Redirect to the 'client_dashboard' URL with the 'client_id' argument
        return redirect('client_dashboard', client_id=client_id)
    else:
        form = ClientFilesForm()

    return render(request, 'app/upload_files.html', {'form': form, 'client': client})

def client_dashboard(request, client_id):
    client = get_object_or_404(ClientInfo, pk=client_id)
    return render(request, 'app/client_dashboard.html', {'client': client})
