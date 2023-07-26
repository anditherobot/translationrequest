"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from app.models import TranslationRequest

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


 #User forms

class TranslationRequestForm(forms.ModelForm):
    class Meta:
        model = TranslationRequest
        fields = [
            'first_name',
            'last_name',
            'company',
            'email',
            'phone_number',
            'source_language',
            'target_language',
            'additional_languages',
            'translate_to_multiple_languages',
            'certified_translation_needed',
            'translation_quality',
            'files_to_translate',
            'description',
            'expedited_service',
            'discount_code',
            'terms_and_conditions',
        ]

