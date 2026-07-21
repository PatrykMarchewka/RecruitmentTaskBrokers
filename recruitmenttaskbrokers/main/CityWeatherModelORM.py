from datetime import datetime, timedelta

from django.utils import timezone

from .OpenMeteoAPI import callOpenMeteoAPIAndSave, callOpenMeteoAPIByCityAndSave
from recruitmenttaskbrokers.main.models import City, CityWeather


def getWeatherForCity(city:City) -> CityWeather | None:
    recentWeather = city.weather

    if recentWeather is None:
        return callOpenMeteoAPIByCityAndSave(city)
    if recentWeather.createdAt < (timezone.now() - timedelta(hours=1)):
        #Most recent weather for this city check was over 1 hour ago, call the API again
        return callOpenMeteoAPIByCityAndSave(city)
    return recentWeather