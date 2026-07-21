from django import forms
from django.core.validators import EmailValidator

from .RegexHelpers import phoneRegexValidator
from .models import Contact

class ContactForm(forms.ModelForm):
    city = forms.CharField()
    status = forms.CharField()
    class Meta:
        model = Contact
        fields = ['name', 'lastName', 'email', 'phone'] #city and status omitted

    def clean_email(self):
        email = self.cleaned_data.get('email')
        EmailValidator()(email)
        return email

    def clean_phoneNumber(self):
        phoneNumber = self.cleaned_data.get('phone')
        phoneRegexValidator(phoneNumber)
        return phoneNumber