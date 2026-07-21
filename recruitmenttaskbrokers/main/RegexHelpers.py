from django.core.validators import RegexValidator

#Simplified regex, matching the E.164 standard
#Taken from https://stackoverflow.com/questions/6478875/regular-expression-matching-e-164-formatted-phone-numbers
phoneRegexValidator = RegexValidator(regex=r'^\+[1-9]\d{1,14}$', message='Invalid phone number format.')