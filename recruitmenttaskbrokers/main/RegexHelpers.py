from django.core.validators import RegexValidator

#Regex taken from https://regex101.com/r/wZ4uU6/1
#Should work with any international phone format
phoneRegexValidator = RegexValidator(regex=r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}', message='Invalid phone number format.')