from datetime import datetime, timedelta

from .OpenMeteoAPI import callOpenMeteoAPIAndSave
from .models import City, CityWeather
from recruitmenttaskbrokers.main.models import City, CityWeather


def getWeatherForCity(city:City) -> CityWeather | None:
    recentWeather = CityWeather.objects.filter(ID=city.id).order_by('-createdAt').first()

    if recentWeather is None:
        return callOpenMeteoAPIAndSave(city)
    if recentWeather.createdAt < datetime.now() - timedelta(hours=1):
        #Most recent weather for this city check was over 1 hour ago, call the API again
        return callOpenMeteoAPIAndSave(city)
    return recentWeather