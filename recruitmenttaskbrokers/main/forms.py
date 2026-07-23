from django import forms
from django.core.validators import EmailValidator

from .RegexHelpers import phoneRegexValidator, PHONE_REGEX_STRING
from .models import Contact

class ContactForm(forms.ModelForm):
    city = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    status = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Contact
        fields = ['name', 'lastName', 'email', 'phone'] #city and status omitted
        #Widget to validate phone in frontend using same regex as the one used in backend, rest added to make sure all fields look the same
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "lastName": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={
                "type": "text",
                "pattern": PHONE_REGEX_STRING,
                "title": "Phone number must start with + and contain only digits",
                "class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.TextInput(attrs={"class": "form-control"})
        }

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