import json
from urllib.parse import urlencode
from urllib.request import urlopen, Request

from django.core.exceptions import ValidationError

from recruitmenttaskbrokers.main.ThirdPartyAPI import OpenMeteoAPI
from recruitmenttaskbrokers.main.StringManipulator import stripPolishCharacters
from recruitmenttaskbrokers.main.models import City


useragent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0"}

def _callOpenStreetMapAPI(cityName: str) -> dict | None:
    """
    Calls OpenStreetMap API and returns JSON response
    :param cityName: Name of the city to find
    :return: Dictionary with all fields from JSON response or None if result is empty
    """
    params = urlencode({
        "q": cityName,
        "format": "json",
        "limit": 1,
    })
    url = f"https://nominatim.openstreetmap.org/search?{params}"

    req = Request(url=url, headers=useragent)
    with urlopen(req) as response:
        result =  json.load(response)
    if not result:
        return None
    return result[0]

def _parseOpenStreetMapData(json: dict) -> tuple[str, float, float] | None:
    """
    Parses OpenStreetMap API response into tuple of city, lat, lon, or None if one or more fields are missing or can't be converted
    :param json: OpenStreetMap API response
    :return: Tuple of city, lat, lon or None if one or more fields are missing or can't be converted
    """
    cityJSON = json.get('display_name')
    latJSON = json.get('lat')
    lonJSON = json.get('lon')
    if cityJSON is None or latJSON is None or lonJSON is None:
        return None

    try:
        cityParsed = stripPolishCharacters(str(cityJSON))
        lat = float(latJSON)
        lon = float(lonJSON)
    except (TypeError, ValueError):
        return None
    return cityParsed, lat, lon

def callOpenStreetMapAPIAndSave(cityName: str) -> City | None:
    """
    Calls OpenStreetMap API and in case of correct return saves it to database if it doesn't exist there. If city didn't exist in database then additional call to OpenMeteo API is done to get current weather
    :param cityName: Name of the city to find
    :return: City if it was found and saved, otherwise None
    """
    returnJSON = _callOpenStreetMapAPI(cityName)
    if returnJSON is None:
        return None
    cityName, latitude, longitude = _parseOpenStreetMapData(returnJSON)

    if cityName is None or latitude is None or longitude is None:
        return None
    #Checking if City already exists in database because saved name is from OpenStreetMapAPI and OpenStreetMap returns city incase of partial match of form
    city = City.objects.filter(name=cityName).first()
    if city is None:
        weather = OpenMeteoAPI.callOpenMeteoAPIAndSave(lat=latitude, lon=longitude)
        city = City(name=cityName, lat=latitude, lon=longitude, weather=weather)
        try:
            city.full_clean()
            city.save()
        except ValidationError as e:
            print("----------------------")
            print("Error saving city", city)
            print("Reason:", e)
    return city