from django.core.validators import RegexValidator
from django.db import models




#Regex taken from https://regex101.com/r/wZ4uU6/1
#Should work with any international phone format
phone_regex = RegexValidator(regex=r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}', message='Invalid phone number format.')

class City(models.Model):
    ID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f'{self.name} - {self.lat}lat {self.lon}lon'

class CityWeather(models.Model):
    ID = models.BigAutoField(primary_key=True)
    cityID = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField(),
    humidity = models.FloatField()
    windSpeed = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.city.name}: Temperature {self.temperature}C, Humidity {self.humidity}%, Wind speed {self.windSpeed}kmh'

class ContactStatus(models.Model):
    ID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    ID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200),
    lastName = models.CharField(max_length=200),
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, validators=[phone_regex], unique=True),
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True),
    status = models.ForeignKey(ContactStatus, on_delete=models.PROTECT)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.lastName} {self.email}'