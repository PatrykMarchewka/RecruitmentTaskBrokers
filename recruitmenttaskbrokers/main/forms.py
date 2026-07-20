from django import forms
from django.core.validators import EmailValidator

from .RegexHelpers import phoneRegexValidator
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'lastName', 'email', 'phoneNumber', 'city', 'status']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        EmailValidator()(email)
        return email

    def clean_phoneNumber(self):
        phoneNumber = self.cleaned_data.get('phoneNumber')
        phoneRegexValidator(phoneNumber)
        return phoneNumber