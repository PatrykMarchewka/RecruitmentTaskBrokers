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

    def __init__(self, *args, **kwargs):
        contact = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if contact:
            self.fields['city'].initial = contact.city.name
            self.fields['status'].initial = contact.status.name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        EmailValidator()(email)
        return email

    def clean_phone(self):
        phoneNumber = self.cleaned_data.get('phone')
        phoneRegexValidator(phoneNumber)
        return phoneNumber