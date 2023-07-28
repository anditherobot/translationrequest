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
            for file in data:
                self.validate_file(file)
        else:
            self.validate_file(data)

        return data

    def validate_file(self, file):
        if file.size > self.max_file_size:
            raise forms.ValidationError(f"File size should not exceed {self.max_file_size} bytes.")
        _, ext = os.path.splitext(file.name)
        if ext.lower() in BLACKLISTED_EXTENSIONS:
            raise forms.ValidationError("Files with this extension are not allowed.")

class ClientFilesForm(forms.ModelForm):
    class Meta:
        model = ClientFiles
        fields = ['file']

    file = LimitedMultipleFileField()


class TranslationRequestForm(forms.ModelForm):
    class Meta:
        model = TranslationRequest
        fields = ['client', 'source_language', 'target_language', 'content']


