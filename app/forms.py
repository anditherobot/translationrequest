"""
Definition of forms.
"""
import os
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Submit, Layout, Row, Column
from app.models import TranslationRequest, ClientFiles, ClientInfo


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result




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

        # Define the MultipleFileField for files_to_translate
    files_to_translate = MultipleFileField(
        help_text="Upload the files you need to be translated.",
       
    )
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


class ClientInfoForm(forms.ModelForm):
    class Meta:
        model = ClientInfo
        fields = ['first_name', 'last_name', 'email', 'term_condition']

   

BLACKLISTED_EXTENSIONS = ['.exe', '.bat', '.cmd']  # Add any other blacklisted extensions here


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class LimitedMultipleFileField(forms.FileField):
    def __init__(self, max_files=5, max_file_size=10 * 1024 * 1024, *args, **kwargs):
        self.max_files = max_files
        self.max_file_size = max_file_size
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            if len(data) > self.max_files:
                raise forms.ValidationError(f"You can upload up to {self.max_files} files only.")
            result = [single_file_clean(d, initial) for d in data]
            for file in result:
                if file.size > self.max_file_size:
                    raise forms.ValidationError(f"File size should not exceed {self.max_file_size} bytes.")
        else:
            result = single_file_clean(data, initial)
        return result

class ClientFilesForm(forms.ModelForm):
    class Meta:
        model = ClientFiles
        fields = ['file']

    file = LimitedMultipleFileField()


