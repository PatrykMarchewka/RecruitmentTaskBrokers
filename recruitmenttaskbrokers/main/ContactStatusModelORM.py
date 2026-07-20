from django.core.exceptions import ValidationError

from .models import ContactStatus
from .StringManipulator import stripPolishCharacters


def getOrCreateStatusByName(status:str) -> ContactStatus | None:
    """
    Returns status for a contact by its name if it exists, otherwise tries to create a new one and save in database
    :param status: Name of the status to search for
    :return: ContactStatus if was found or saved in database, None if status is None or couldnt be saved in database
    """
    if status is None:
        return None

    status = stripPolishCharacters(status)
    status = status.lower()

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
