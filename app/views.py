"""
Definition of views.
"""
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse    
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpRequest
from .models import ClientInfo, TranslationRequest, ClientFiles
from .forms import ClientInfoForm, TranslationRequestForm, ClientFilesForm
import mimetypes, os
from .notification_utils import send_email_receipt, notify_admin

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
   

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            send_email_receipt(form.cleaned_data)
            notify_admin()
            # Flash message, clean form or redirect to receipt page.
            # Add details about an email has been sent.

            return redirect('translationrequestdashboard')
            # Redirect to a success page or do any other processing.

    return render(request, 'app/create_translation_request.html', {'form': form})


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


#notify?
def create_client(request):
    if request.method == 'POST':
        form = ClientInfoForm(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect('client_dashboard', client_id=client.pk)
    else:
        form = ClientInfoForm()
    return render(request, 'app/create_client.html', {'form': form})


def client_dashboard(request, client_id):
    client_info = ClientInfo.objects.get(pk=client_id)
    translation_requests = TranslationRequest.objects.filter(client=client_info)

    context = {
        'client_info': client_info,
        'translation_requests': translation_requests,
    }
    return render(request, 'app/client_dashboard.html', context)


def create_translation_request_view(request, client_id):
    client = get_object_or_404(ClientInfo, id=client_id)
    if request.method == 'POST':
        form = TranslationRequestForm(request.POST)
        if form.is_valid():
            translation_request = form.save(commit=False)
          
            translation_request.client_id = client_id  # Set the client using the foreign key ID
            translation_request.save()
            return redirect('upload_files_for_request', request_id=translation_request.id)
    else:
       
        form = TranslationRequestForm(initial={'client': client})  # Pass the client info to the form as an initial value

    return render(request, 'app/create_translation_request.html', {'form': form})

def upload_files_for_request(request, request_id):
    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    client_info = translation_request.client
    
    if request.method == 'POST':
        form = ClientFilesForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')  # Get multiple files

            for file in files:
                # Save each file and associate them with the translation request
                client_files = ClientFiles(client=client_info, translation_request=translation_request, original_file=file)
                client_files.save()

            return redirect('view_translation_request', request_id=request_id)  # Redirect to the view_translation_request URL
    else:
        form = ClientFilesForm()

    context = {
        'form': form,
        'translation_request': translation_request,
        'client_info': client_info,
    }
    return render(request, 'app/upload_files_for_request.html', context)

def view_translation_request(request, request_id):
    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    client_files = translation_request.files.all()  
    context = {
        'translation_request': translation_request,
        'client_files': client_files,
    }
    return render(request, 'app/view_translation_request.html', context)

def list_clients(request):
    clients = ClientInfo.objects.all()
    return render(request, 'app/list_clients.html', {'clients': clients})

def file_details(request, request_id, file_id):
    # Retrieve the translation request and file objects based on the IDs
    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    file_object = get_object_or_404(ClientFiles, id=file_id)

    # Your view logic here

    return render(request, 'app/file_details.html', {
        'translation_request': translation_request,
        'file': file_object
    })

def download_file(request, request_id, file_id):
    # Retrieve the file object based on the file_id and request_id
    file_object = get_object_or_404(ClientFiles, id=file_id, translation_request_id=request_id)

    # Verify that the file exists and has content
    if not file_object.original_file:
        raise Http404("The requested file does not exist.")

    # Get the file path and content type using mimetypes
    file_path = file_object.original_file.path
    content_type, encoding = mimetypes.guess_type(file_path)

    # If the content type is not determined, use a default value
    if not content_type:
        content_type = 'application/octet-stream'

    # Prepare the response with file content and content type
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=content_type)

    # Set the 'Content-Disposition' header to trigger the download behavior in the browser
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'

    return response

from django.views.decorators.http import require_POST

@require_POST
def update_file_status(request, request_id, file_id):
    # Retrieve the translation request and file objects based on the IDs
    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    file = get_object_or_404(ClientFiles, id=file_id)

    # Get the new status from the form data
    new_status = request.POST.get('status')

    if new_status not in dict(ClientFiles.STATUS_CHOICES):
        # Invalid status, don't update and show an error message
        messages.error(request, f"Invalid status: {new_status}")
    else:
        # Update the status and save the object
        file.status = new_status
        file.save()

        # Flash a success message
        messages.success(request, "File status updated successfully!")

    # Redirect back to the file details page
    return redirect('file_details', request_id=request_id, file_id=file_id)

   

def message_user_about_file(request, request_id, file_id):
    # Your view logic here

    return redirect('file_details', request_id=request_id, file_id=file_id)

# View stub for deleting a file
def delete_file(request, request_id, file_id):
    # Your view logic here

    return redirect('file_details', request_id=request_id, file_id=file_id)


# View stub for uploading a translated file
from .forms import TranslatedFileUploadForm

def upload_translated_file(request, request_id, file_id):
    # Retrieve the file object based on the file_id and request_id
    file_object = get_object_or_404(ClientFiles, id=file_id, translation_request_id=request_id)

    if request.method == 'POST':
        form = TranslatedFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the processed file to the file object
            file_object.processed_file = form.cleaned_data['processed_file']
            file_object.save()

            # Redirect back to the file details page after successful file upload
            return redirect('file_details', request_id=request_id, file_id=file_id)
    else:
        form = TranslatedFileUploadForm()

    return render(request, 'app/upload_translated_file.html', {'form': form, 'request_id': request_id, 'file_id': file_id})






