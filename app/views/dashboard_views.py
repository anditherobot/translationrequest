from django.shortcuts import render, redirect, get_object_or_404
from ..forms import (
    FileUploadForm,
    SandboxForm,
    TranslationRequestForm,
    ClientInfoForm,
    ClientFileForm,
    TranslatedFileUploadForm,
    
)
from ..models import TranslationRequest, ClientInfo, ClientFile
from django.http import HttpResponse, Http404, JsonResponse
import os
import mimetypes
from django.views.decorators.http import require_POST
from django.contrib import messages

from django.views.decorators.http import require_POST

from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
import pytesseract
from PIL import Image

def translation_request_view(request):
    form = TranslationRequestForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            send_email_receipt(form.cleaned_data)
            notify_admin()
            # Flash message, clean form or redirect to receipt page.
            # Add details about an email has been sent.

            return redirect("translationrequestdashboard")
            # Redirect to a success page or do any other processing.

    return render(
        request, "app/dashboard/create_translation_request.html", {"form": form}
    )


def translation_request_dashboard(request):
    # Retrieve all submitted requests from the database
    submitted_requests = TranslationRequest.objects.all()

    return render(
        request,
        "app/dashboard/translation_request_dashboard.html",
        {"submitted_requests": submitted_requests},
    )


def translation_tracker(request):
    return render(request, "app/dashboard/translation_tracker.html")


# notify?
def create_client(request):
    if request.method == "POST":
        form = ClientInfoForm(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect("client_dashboard", client_id=client.pk)
    else:
        form = ClientInfoForm()
    return render(request, "app/dashboard/create_client.html", {"form": form})


def client_dashboard(request, client_id):
    client_info = ClientInfo.objects    .get(pk=client_id)
    translation_requests = TranslationRequest.objects.filter(client=client_info)

    context = {
        "client_info": client_info,
        "translation_requests": translation_requests,
    }
    return render(request, "app/dashboard/client_dashboard.html", context)


def create_translation_request(request, client_id):
    client = get_object_or_404(ClientInfo, id=client_id)

    if request.method == "POST":
        translation_form = TranslationRequestForm(request.POST, request.FILES)
       

        if translation_form.is_valid():
            translation_request = translation_form.save(commit=False)
            translation_request.client = client
            translation_request.save()

            files = request.FILES.getlist("files")

            for file in files:
                client_file = ClientFile(
                    client=client,
                    translation_request=translation_request,
                    original_file=file,
                )
                client_file.save()

            return redirect("view_translation_request", request_id=translation_request.id)
    else:
        translation_form = TranslationRequestForm(initial={"client": client})
      

    context = {
        "translation_form": translation_form,
       
        "client": client,
    }
    return render(request, "app/dashboard/create_translation_request.html", context)




def view_translation_request(request, request_id):
    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    client_files = translation_request.files.all()
    
    
    
    # Check if all files are not pending
    all_files_completed = all(file.status == "Completed" for file in client_files)

    context = {
        "translation_request": translation_request,
        "client_files": client_files,
        'status_counts': translation_request.get_file_status_counts(),
        "all_files_completed": all_files_completed,  # Pass the check variable to the template
    }
    return render(request, "app/dashboard/view_translation_request.html", context)


def list_clients(request):
    clients = ClientInfo.objects.all()
    return render(request, "app/dashboard/list_clients.html", {"clients": clients})


def file_details(request, request_id, file_id):
    # Retrieve the translation request and file objects based on the IDs
    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    file_object = get_object_or_404(ClientFile, id=file_id)

    if request.method == "POST":
        extracted_text = request.POST.get("extracted_text", "")
        file_object.extracted_text = extracted_text
        file_object.save()

    return render(
        request,
        "app/dashboard/file_details.html",
        {"translation_request": translation_request, "file": file_object},
    )


def download_file(request, request_id, file_id):
    # Retrieve the file object based on the file_id and request_id
    file_object = get_object_or_404(
        ClientFile, id=file_id, translation_request_id=request_id
    )

    # Verify that the file exists and has content
    if not file_object.original_file:
        raise Http404("The requested file does not exist.")

    # Get the file path and content type using mimetypes
    file_path = file_object.original_file.path
    content_type, encoding = mimetypes.guess_type(file_path)

    # If the content type is not determined, use a default value
    if not content_type:
        content_type = "application/octet-stream"

    # Prepare the response with file content and content type
    with open(file_path, "rb") as file:
        response = HttpResponse(file.read(), content_type=content_type)

    # Set the 'Content-Disposition' header to trigger the download behavior in the browser
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{os.path.basename(file_path)}"'

    return response


@require_POST
def update_file_status(request, request_id, file_id):
    # Retrieve the translation request and file objects based on the IDs
    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    file = get_object_or_404(ClientFile, id=file_id)

    # Get the new status from the form data
    new_status = request.POST.get("status")

    if new_status not in dict(ClientFile.STATUS_CHOICES):
        # Invalid status, don't update and show an error message
        messages.error(request, f"Invalid status: {new_status}")
    else:
        if new_status == "Completed" and not file.processed_file:
            # File cannot be marked as completed without a processed file
            messages.error(
                request,
                "A processed file must be uploaded before marking as completed.",
            )
        else:
            # Update the status and save the object
            file.status = new_status
            file.save()

            # Flash a success message
            messages.success(request, "File status updated successfully!")

    # Redirect back to the file details page
    return redirect("file_details", request_id=request_id, file_id=file_id)


def message_user_about_file(request, request_id, file_id):
    # Your view logic here

    return redirect("file_details", request_id=request_id, file_id=file_id)


# View stub for deleting a file
def delete_file(request, request_id, file_id):
    # Your view logic here

    return redirect("file_details", request_id=request_id, file_id=file_id)


def translation_tracker(request):
    # Get all translation requests ordered by request date (most recent first)
    translation_requests = TranslationRequest.objects.all().order_by("-request_date")

    return render(
        request,
        "app/dashboard/translation_tracker.html",
        {"translation_requests": translation_requests},
    )


def translation_request_all(request):
    return render(
        request,
        "app/dashboard/view_all_translation_request.html",
        {"allrequests": TranslationRequest.objects.all()},
    )


# View stub for uploading a translated file


def upload_translated_file(request, request_id, file_id):
    # Retrieve the file object based on the file_id and request_id
    file_object = get_object_or_404(
        ClientFile, id=file_id, translation_request_id=request_id
    )

    if request.method == "POST":
        form = TranslatedFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the processed file to the file object
            file_object.processed_file = form.cleaned_data["processed_file"]
            file_object.save()

            # Redirect back to the file details page after successful file upload
            return redirect("file_details", request_id=request_id, file_id=file_id)
    else:
        form = TranslatedFileUploadForm()

    return render(
        request,
        "app/dashboard/upload_translated_file.html",
        {"form": form, "request_id": request_id, "file_id": file_id},
    )


#upload file attached to translation request.
def add_files_to_translation_request(request, request_id, client_id):
    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    client_info = get_object_or_404(ClientInfo, id=client_id)

    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.translation_request = translation_request
            new_file.client = client_info  # Associate the client
            new_file.save()

            # Redirect back to the translation request details page
            return redirect("view_translation_request", request_id=translation_request.id)
    else:
        form = FileUploadForm()

    return render(
        request,
        "app/dashboard/add_files_to_translation_request.html",
        {"form": form, "translation_request": translation_request, "client_info": client_info},
    )


def view_files_by_status(request, client_id, request_id, status):
    client = get_object_or_404(ClientInfo, id=client_id)
    translation_request = get_object_or_404(TranslationRequest, id=request_id)
    client_files = ClientFile.objects.filter(
        client=client, translation_request=translation_request, status=status
    )

    return render(
        request,
        "app/dashboard/view_files_by_status.html",
        {
            "client": client,
            "translation_request": translation_request,
            "status": status,
            "client_files": client_files,
        },
    )


def generate_fictional_receipt(request):
    # Replace the example data with your actual data from the models
    receipt_data = {
        "receipt_id": "RECEIPT123",
        "date": "July 28, 2023",
        "customer_details": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "address": "123 Main Street, City, Country",
        },
        "payment_details": {"total_amount_paid": 12.30},
        "invoice_details": {
            "invoice_number": "INV123",
            "invoice_date": "July 28, 2023",
            "due_date": "August 28, 2023",
            "quote_amount": 25.50,
        },
        "file_payment_details": {"number_of_files_paid": 3},
    }

    # Return the JSON response
    return JsonResponse(receipt_data)

def view_client_requests(request, pk):
    client = get_object_or_404(ClientInfo, pk=pk)
    # Retrieve and pass requests related to the client to the template
    return render(request, 'app/dashboard/view_client_requests.html', {'client': client})


def view_client_files(request, pk):
    client = get_object_or_404(ClientInfo, pk=pk)
    # Retrieve and pass files related to the client to the template
    return render(request, 'app/dashboard/view_client_files.html', {'client': client})




def sandbox(request):
    if request.method == 'POST':
        form = SandboxForm(request.POST)
        if form.is_valid():
            # Process the form data if it's valid
            subject = form.cleaned_data['subject']
            verb = form.cleaned_data['verb']
            # Do something with the subject data
            
            # Add the subject to the context variable
            context = {'form': form, 'subject': subject, 'verb': verb}
            return render(request, 'app/sandbox.html', context)
    else:
        form = SandboxForm()

    context = {'form': form}
    return render(request, 'app/sandbox.html', context)

#all files related to a particular request id, in a table
def request_files(request, request_id):
    pass


def extract_text(request, file_id):
    file = get_object_or_404(ClientFile, id=file_id)

    if file.original_file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        try:
            image = Image.open(file.original_file.path)

            languages = 'hat+fra'  # Replace with the appropriate language codes
            extracted_text = pytesseract.image_to_string(image, lang=languages)

            return JsonResponse({'extracted_text': extracted_text})

        except Exception as e:
            error_response = f'Error: {str(e)}'
            return JsonResponse({'error': error_response})

    else:
        error_response = 'Error: Not an image file'
        return JsonResponse({'error': error_response})