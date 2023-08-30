from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django import forms

from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

import pytesseract
from PIL import Image
# models.py



def extract_ocr_text(file):
    if file.original_file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        try:
            image = Image.open(file.original_file.path)
            languages = 'hat+fra'  # Replace with the appropriate language codes
            extracted_text = pytesseract.image_to_string(image, lang=languages)
            return extracted_text
        except Exception as e:
            print(f'Error: {str(e)}')
    return None




def file_size(value):
    limit = 10 * 1024 * 1024  # 10 MB

    if isinstance(value, (list, tuple)):
        for file in value:
            if file.size > limit:
                raise forms.ValidationError('File size should not exceed 10 MB.')
    else:
        if value.size > limit:
            raise forms.ValidationError('File size should not exceed 10 MB.')

def client_directory_path(instance, filename):
    return f"uploads/ClientFile/{instance.client.id}/{filename}"

def client_processed_directory_path(instance, filename):
    return f"uploads/ClientFile/{instance.client.id}/processed/{filename}"

class ClientInfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    term_condition = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"








# Define the choices for source and target languages
LANGUAGE_CHOICES = (
    ('French', 'French'),
    ('Haitian Creole', 'Haitian Creole'),
    ('English', 'English'),
    ('Spanish', 'Spanish'),
    # Add more languages here if needed
)

# Define the choices for request status
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
    ('void', 'Void'),
)


def validate_different_languages(cleaned_data):
    source_language = cleaned_data.get('source_language')
    target_language = cleaned_data.get('target_language')

    if source_language == target_language:
        raise ValidationError(
            _('Source language and target language cannot be the same.'),
            code='invalid'
        )

class TranslationRequest(models.Model):
    client = models.ForeignKey('ClientInfo', on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    source_language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, blank=False, default='Unspecified' )
    target_language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, blank=False, default='Unspecified')
    content = models.TextField(verbose_name="Additional information", default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    completed_files = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"Translation Request {self.pk} - Client: {self.client}, Status: {self.status}"

    def clean(self):
        super().clean()
        cleaned_data = super().clean()
       
        if self.source_language == self.target_language:
            raise ValidationError("Source and target languages cannot be the same.")
          

    #related name is files
    def get_file_count(self):
        return self.files.count()

    def get_file_status_counts(self):
        status_counts = {
            'Pending': self.files.filter(status='Pending').count(),
            'InProgress': self.files.filter(status='In Progress').count(),
            'Completed': self.files.filter(status='Completed').count(),
            'Void': self.files.filter(status='Void').count(),
        }
        return status_counts

class ClientFile(models.Model):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    VOID = 'Void'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (VOID, 'Void'),
    ]
    client = models.ForeignKey(ClientInfo, on_delete=models.CASCADE, related_name='client_files')
    translation_request = models.ForeignKey(TranslationRequest, on_delete=models.CASCADE, related_name='files')
    original_file = models.FileField(upload_to=client_directory_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt', 'jpg', 'png', 'jpeg', 'gif']), file_size])
    processed_file = models.FileField(upload_to= client_processed_directory_path, blank=True, null=True, validators=[file_size])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    extracted_text = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"ClientFile - Client: {self.client}"



@receiver(post_save, sender=ClientFile)
def extract_ocr_on_new_file(sender, instance, created, **kwargs):
    if created:
        extracted_text = extract_ocr_text(instance)
        if extracted_text:
            instance.processed_file = instance.original_file  # Save the original image as the processed file
            instance.ocr_text = extracted_text  # Save the extracted text as OCR text
            instance.status = ClientFile.COMPLETED  # Update the status
            instance.save()



            from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"