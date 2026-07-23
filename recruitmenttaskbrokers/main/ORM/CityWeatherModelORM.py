from datetime import timedelta

from django.utils import timezone

from recruitmenttaskbrokers.main.ThirdPartyAPI.OpenMeteoAPI import callOpenMeteoAPIByCityAndSave
from recruitmenttaskbrokers.main.models import City, CityWeather


def getWeatherForCity(city:City) -> CityWeather | None:
    """
    Gets weather data for City using OpenMeteoAPI
    Checks last saved weather data, if it doesnt exist or if it was saved over hour ago application sends another request to get fresh information
    :param city: City to get weather for
    :return: Weather object or None if there was issue getting data
    """
    recentWeather = city.weather

    if recentWeather is None:
        return callOpenMeteoAPIByCityAndSave(city)
    if recentWeather.createdAt < (timezone.now() - timedelta(hours=1)):
        #Most recent weather for this city check was over 1 hour ago, call the API again
        return callOpenMeteoAPIByCityAndSave(city)
    return recentWeather