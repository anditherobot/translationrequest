"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Submit, Layout, Row, Column
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
            'email',
            'phone_number',
            'source_language',
            'target_language',
            'certified_translation_needed',
            'translation_quality',
            'files_to_translate',
            'description',
            'discount_code',
            'terms_and_conditions',
        ]
    helper = FormHelper()
   
    helper.form_method = 'POST'
    helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-3'),
                Column('last_name', css_class='form-group col-md-3'),
            ),
            Row(
                Column('email', css_class='form-group col-md-3'),
                Column('phone_number', css_class='form-group col-md-3'),
            ),
            Row(
                Column('source_language', css_class='form-group col-md-3'),
                Column('target_language', css_class='form-group col-md-3'),
            ),
            Row(
                Column('certified_translation_needed', css_class='form-group col-md-3'),
                Column('translation_quality', css_class='form-group col-md-3'),
            ),
            'files_to_translate',
            'description',
            'discount_code',
            'terms_and_conditions',
            ButtonHolder(
                Submit('submit', 'Create Translation Request', css_class='btn btn-primary btn-success')
            )
        )

