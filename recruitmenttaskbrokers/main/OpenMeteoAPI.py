import json
from urllib.request import urlopen

from recruitmenttaskbrokers.main.models import City, CityWeather


def _callOpenMeteoAPI(lat: float, lon: float) -> dict | None:
    """
    Calls OpenMeteo API and returns JSON response or None if error occurs
    :param lat: Latitude to use
    :param lon: Longitude to use
    :return: Dictionary with fields from JSON response or None if error occurred
    """
    #Note: OpenMeteo seems to round the lat/lon coordinates, most likely to nearest station?
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature,relative_humidity_2m,windspeed'
    with urlopen(url) as response:
        result =  json.load(response)[0]
    if not result:
        return None
    if result.get('error') is True:
        return None
    return result

def _parseOpenMeteoData(json: dict) -> tuple[float, float, float] | None:
    """
    Parses OpenMeteo API response into tuple of temperature, humidity, wind speed, or None if one or more fields are missing or can't be converted
    :param json:
    :return:
    """
    currentWeather = json.get('current')
    if not isinstance(currentWeather, dict):
        return None
    temperatureJSON = currentWeather.get('temperature')
    humidityJSON = currentWeather.get('relative_humidity_2m')
    windSpeedJSON = currentWeather.get('windspeed')

    if temperatureJSON is None or humidityJSON is None or windSpeedJSON is None:
        return None

    try:
        temperature = float(temperatureJSON)
        humidity = float(humidityJSON)
        windSpeed = float(windSpeedJSON)
    except (TypeError, ValueError):
        return None

    return temperature, humidity, windSpeed

def callOpenMeteoAPIAndSave(city: City) -> CityWeather | None:
    """
    Calls OpenMeteo API and in case of return saves it to database
    :param city: City to search weather for
    :return: CityWeather if it was found and saved, otherwise None
    """
    json = _callOpenMeteoAPI(city.lat, city.lon)
    if json is None:
        return None
    temperature, humidity, windSpeed = _parseOpenMeteoData(json)
    if temperature is None or humidity is None or windSpeed is None:
        return None
    cityWeather = CityWeather(cityID=City.ID, temperature=temperature, humidity=humidity, windspeed=windSpeed)
    cityWeather.save()
    return cityWeather