# models.py

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
class TranslationRequest(models.Model):
    first_name = models.CharField(max_length=100, help_text="Please enter your first name.")
    last_name = models.CharField(max_length=100, help_text="Please enter your last name.")
   
    email = models.EmailField(help_text="Please enter a valid email address.")
    phone_number = models.CharField(max_length=20, help_text="Please enter your phone number.")

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

class InProgressRequest(models.Model):
    translation_request = models.OneToOneField(
        TranslationRequest, on_delete=models.CASCADE, related_name='in_progress'
    )
    in_progress_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"In Progress: {self.translation_request}"

@receiver(post_save, sender=TranslationRequest)
def create_in_progress_request(sender, instance, created, **kwargs):
    if instance.status == 'in_progress':
        InProgressRequest.objects.get_or_create(translation_request=instance)
