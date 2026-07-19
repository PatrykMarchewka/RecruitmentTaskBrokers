from recruitmenttaskbrokers.main.models import ContactStatus
from recruitmenttaskbrokers.main.helpers import stripPolishCharacters


def getOrCreateStatusByName(status:str) -> ContactStatus:
    status = stripPolishCharacters(status)
    statusFromDB = ContactStatus.objects.filter(name=status).first()
    if statusFromDB is None:
        statusFromDB = ContactStatus(name=status)
        statusFromDB.save()
    return statusFromDB
