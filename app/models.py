"""
Definition of models.
"""



# Create your models here.
from django.db import models

from django.db import models

class TranslationRequest(models.Model):
    first_name = models.CharField(max_length=100, help_text="Please enter your first name.")
    last_name = models.CharField(max_length=100, help_text="Please enter your last name.")
    company = models.CharField(max_length=200, blank=True, help_text="Please enter your company name (optional).")
    email = models.EmailField(help_text="Please enter a valid email address.")
    phone_number = models.CharField(max_length=20, help_text="Please enter your phone number.")
    source_language = models.CharField(max_length=100, help_text="Please select the source language.")
    target_language = models.CharField(max_length=100, help_text="Please select the target language.")
    additional_languages = models.CharField(max_length=200, blank=True, help_text="If you need to translate to multiple languages, please specify here.")
    translate_to_multiple_languages = models.BooleanField(default=False, help_text="Check this box if you need to translate into multiple languages.")
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

     # Status choices
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    files_to_translate = models.FileField(upload_to='uploads/', help_text="Upload the files you need to be translated.")
    description = models.TextField(help_text="Provide additional information about your translation request.")
    expedited_service = models.BooleanField(default=False, help_text="Check this box if you need expedited service.")
    discount_code = models.CharField(max_length=50, blank=True, help_text="If you have a discount code, enter it here (optional).")
    terms_and_conditions = models.BooleanField(help_text="Check this box to agree to the terms and conditions.")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.source_language} to {self.target_language}"

