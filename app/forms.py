"""
Definition of forms.
"""
import os
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Submit, Layout, Row, Column, Field
from app.models import TranslationRequest, ClientFile, ClientInfo
from django.core.exceptions import ValidationError
from .validators import subject_verb_not_equal

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'class': 'btn btn-secondary'}  # Add the Bootstrap class here
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


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
        fields = ['first_name', 'last_name', 'email']

       

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

class ClientFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ['file']

    file = LimitedMultipleFileField()


class TranslationRequestForm(forms.ModelForm):
    files = LimitedMultipleFileField()

    class Meta:
        model = TranslationRequest
        fields = [
           
            'source_language',
            'target_language',
            'content',  
          
        ]
        widgets = {
            'source_language' : forms.RadioSelect,
            'target_language' : forms.RadioSelect,
            
            'content':forms.Textarea(attrs={'class': 'form-control', }),  # Set cols attribute to 35
            }






class TranslatedFileUploadForm(forms.Form):
    processed_file = forms.FileField()

class SandboxForm(forms.Form):
    LANGUAGE_CHOICES = [
        ('fr', 'French'),
        ('en', 'English'),
        ('es', 'Spanish'),
    ]

    subject = forms.ChoiceField(
        label='Your name',
        choices=LANGUAGE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'vertical-select'}),
        error_messages={
            'required': 'Please select your name.',
        }
    )
    verb = forms.ChoiceField(
        label='Your last name',
        choices=LANGUAGE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'vertical-select'}),
        error_messages={
            'required': 'Please select your last name.',
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        verb = cleaned_data.get('verb')

        if subject == verb and subject is not None:
            raise forms.ValidationError("Subject and verb can't be the same.")

        return cleaned_data




class FileUploadForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ['original_file']




        
class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleImageField(forms.ImageField):
    widget = MultipleImageInput

class ProductImageForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    images = MultipleImageField(widget=MultipleImageInput(attrs={'multiple': True}))