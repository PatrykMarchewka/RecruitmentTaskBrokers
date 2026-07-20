from django.core.exceptions import ValidationError

from .models import ContactStatus
from .StringManipulator import stripPolishCharacters


def getOrCreateStatusByName(status:str) -> ContactStatus:
    status = stripPolishCharacters(status)
    statusFromDB = ContactStatus.objects.filter(name=status).first()
    if statusFromDB is None:
        statusFromDB = ContactStatus(name=status)
        try:
            statusFromDB.full_clean()
            statusFromDB.save()
        except ValidationError as e:
            print("----------------------")
            print("Error saving status", statusFromDB)
            print("Reason:", e)
            return None
    return statusFromDB
