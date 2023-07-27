from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from django.db.models.signals import post_save
from django.dispatch import receiver

class TranslationRequest(models.Model):

    def validate_no_executable(value):
        if value.name.lower().endswith(('.exe', '.bat', '.cmd')):
            raise ValidationError("Executable files are not allowed.")

    def validate_file_size(value):
        max_size = 10 * 1024 * 1024  # 10 MB in bytes
        if value.size > max_size:
            raise ValidationError(_('File size must be no more than 10 MB.'))

    def validate_max_files(value):
    # Count the number of uploaded files
        file_count = 0
        if isinstance(value, list):
            file_count = len(value)
        elif value:
            file_count = 1

        if file_count > TranslationRequest.MAX_FILES:
            raise ValidationError(f"You can upload up to {TranslationRequest.MAX_FILES} files.")

    # Personal Information
    first_name = models.CharField(max_length=100, help_text="Please enter your first name.")
    last_name = models.CharField(max_length=100, help_text="Please enter your last name.")
    email = models.EmailField(help_text="Please enter a valid email address.")
    phone_number = models.CharField(max_length=20, help_text="Please enter your phone number.")

    # Language Choices
    FRENCH = 'French'
    HAITIAN_CREOLE = 'Haitian Creole'
    ENGLISH = 'English'
    SPANISH = 'Spanish'
    
    LANGUAGE_CHOICES = [
        (FRENCH, 'French'),
        (HAITIAN_CREOLE, 'Haitian Creole'),
        (ENGLISH, 'English'),
        (SPANISH, 'Spanish'),
    ]

    source_language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, help_text="Choose the language of the document.")
    target_language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, help_text="Choose your destination language")
    certified_translation_needed = models.CharField(
        max_length=100,
        choices=[
            ('uscis', 'Yes - Documents for the USCIS, certificates, contracts'),
            ('non_uscis', 'No - Websites, marketing, e-commerce'),
        ],
        help_text="Select whether you need a certified translation for documents related to the USCIS or other purposes."
    )
    translation_quality = models.CharField(
        max_length=100,
        choices=[
            ('superior', 'Superior - Websites and material for print, as well as legal, financial and medical documents. Higher price.'),
            ('good', 'Good - Material for internal use and correspondence. Mid-range.'),
            ('basic', 'Basic - I just need to understand the text. Low price.'),
        ],
        help_text="Select the level of translation quality you require."
    )

    # Translation Request Status
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    # File Upload
    MAX_FILES = 5
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes
    ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt']

    files_to_translate = models.FileField(
        upload_to='uploads/',
        help_text="Upload the files you need to be translated.",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS),
            validate_no_executable,
            validate_max_files,
        ],
    )

    description = models.TextField(help_text="Provide additional information about your translation request.")
    discount_code = models.CharField(max_length=50, blank=True, help_text="If you have a discount code, enter it here (optional).")
    terms_and_conditions = models.BooleanField(help_text="Check this box to agree to the terms and conditions.")
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    

    def clean(self):
        if self.source_language == self.target_language:
            raise ValidationError("Source and target languages cannot be the same.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate the instance before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
