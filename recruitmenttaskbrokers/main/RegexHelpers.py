from django.core.validators import RegexValidator

#Simplified regex, matching the E.164 standard
#Taken from https://stackoverflow.com/questions/6478875/regular-expression-matching-e-164-formatted-phone-numbers
PHONE_REGEX_STRING = r'^\+[1-9]\d{1,14}$'
phoneRegexValidator = RegexValidator(regex=PHONE_REGEX_STRING, message='Invalid phone number format.')