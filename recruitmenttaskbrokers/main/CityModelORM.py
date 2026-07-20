from .StringManipulator import  stripPolishCharacters
from .OpenStreetMapAPI import  callOpenStreetMapAPIAndSave
from recruitmenttaskbrokers.main.models import City


def getCityByName(cityName:str) -> City | None:
    """
    Returns a City object by its name, if it doesnt exist try to find it using OpenStreetMap API
    :param cityName: Name of city
    :return: City object if found, None if city is not in database and couldn't be found using OpenStreetMap API or provided None as cityName
    """
    if cityName is None:
        return None
    cityName = stripPolishCharacters(cityName)
    cityName = cityName.lower()

    city = City.objects.filter(name=cityName).first()
    if city is None:
        return callOpenStreetMapAPIAndSave(cityName)
    return city