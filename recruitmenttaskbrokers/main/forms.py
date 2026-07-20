from django import forms
from django.core.validators import RegexValidator, EmailValidator

from .models import Contact

phone_regex = RegexValidator(regex=r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}', message='Invalid phone number format.')


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
        phone_regex(phoneNumber)
        return phoneNumber