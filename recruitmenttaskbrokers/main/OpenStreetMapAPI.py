import json
from urllib.request import urlopen

from recruitmenttaskbrokers.main.helpers import _stripPolishCharacters
from recruitmenttaskbrokers.main.models import City


def _callOpenStreetMapAPI(cityName: str) -> dict | None:
    """
    Calls OpenStreetMap API and returns JSON response
    :param cityName: Name of the city to find
    :return: Dictionary with all fields from JSON response or None if result is empty
    """
    url = f"https://nominatim.openstreetmap.org/search?q={cityName}&format=json&limit=1"
    with urlopen(url) as response:
        result =  json.load(response)[0]
    if not result:
        return None
    return result[0]

def _parseOpenStreetMapData(json: dict) -> tuple[str, float, float] | None:
    """
    Parses OpenStreetMap API response into tuple of city, lat, lon, or None if one or more fields are missing or can't be converted
    :param json: OpenStreetMap API response
    :return: Tuple of city, lat, lon or None if one or more fields are missing or can't be converted
    """
    cityJSON = json.get('city')
    latJSON = json.get('lat')
    lonJSON = json.get('lon')
    if cityJSON is None or latJSON is None or lonJSON is None:
        return None

    try:
        cityParsed = _stripPolishCharacters(str(cityJSON))
        lat = float(latJSON)
        lon = float(lonJSON)
    except (TypeError, ValueError):
        return None
    return cityParsed, lat, lon

def callOpenStreetMapAPIAndSave(cityName: str) -> City | None:
    """
    Calls OpenStreetMap API and in case of correct return saves it to database
    :param cityName: Name of the city to find
    :return: City if it was found and saved, otherwise None
    """
    json = _callOpenStreetMapAPI(cityName)
    if json is None:
        return None
    cityName, latitude, longitude = _parseOpenStreetMapData(json)

    if cityName is None or latitude is None or longitude is None:
        return None

    city = City(name=cityName, lat=latitude, lon=longitude)
    city.save()
    return city