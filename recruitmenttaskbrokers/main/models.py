from django.db import models

from .RegexHelpers import phoneRegexValidator

class CityWeather(models.Model):
    ID = models.BigAutoField(primary_key=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    windSpeed = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Temperature {self.temperature}C, Humidity {self.humidity}%, Wind speed {self.windSpeed}kmh'

class City(models.Model):
    ID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    lat = models.FloatField()
    lon = models.FloatField()
    weather = models.ForeignKey(CityWeather, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.name} - {self.lat}lat {self.lon}lon'

class ContactStatus(models.Model):
    ID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    ID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, validators=[phoneRegexValidator], unique=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(ContactStatus, on_delete=models.PROTECT)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.lastName} {self.email}'