from datetime import datetime, timedelta

from recruitmenttaskbrokers.main import OpenMeteoAPI
from recruitmenttaskbrokers.main.models import City, CityWeather


def getWeatherForCity(city:City) -> CityWeather | None:
    recentWeather = CityWeather.objects.filter(ID=city.id).order_by('-createdAt').first()

    if recentWeather is None:
        return OpenMeteoAPI.callOpenMeteoAPIAndSave(city)
    if recentWeather.createdAt < datetime.now() - timedelta(hours=1):
        #Most recent weather for this city check was over 1 hour ago, call the API again
        return OpenMeteoAPI.callOpenMeteoAPIAndSave(city)
    return recentWeather