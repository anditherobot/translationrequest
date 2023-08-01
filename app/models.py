from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django import forms

from django.utils.translation import gettext_lazy as _



# models.py




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
    return f"uploads/clientfiles/{instance.client.id}/{filename}"

def client_processed_directory_path(instance, filename):
    return f"uploads/clientfiles/{instance.client.id}/processed/{filename}"

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
    source_language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES )
    target_language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    content = models.TextField(help_text="Additional information")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    completed_files = models.PositiveIntegerField(default=0)  # New field to track completed files

    def __str__(self):
        return f"Translation Request {self.pk} - Client: {self.client}, Status: {self.status}"

    def clean(self):
        if self.source_language == self.target_language:
            raise ValidationError("Source and target languages cannot be the same.")

class ClientFiles(models.Model):
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

    def __str__(self):
        return f"ClientFiles - Client: {self.client}"