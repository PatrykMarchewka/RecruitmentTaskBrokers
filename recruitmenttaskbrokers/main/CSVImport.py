import csv
from collections import namedtuple
from io import TextIOWrapper

from recruitmenttaskbrokers.main import ContactStatusModelORM, CityModelORM
from recruitmenttaskbrokers.main.models import Contact


ContactRow = namedtuple("ContactRow", ["name", "lastName", "email", "phoneNumber", "city", "status"])

def _parseContactsRow(row: dict) -> ContactRow:
    name = row["Name"]
    lastName = row["Last Name"]
    email = row["Email"]
    phoneNumber = row["Phone Number"]
    city = row["City"]
    status = row["Status"]
    return name, lastName, email, phoneNumber, city, status


def importCSV(file) -> int:

    wrapper = TextIOWrapper(file, encoding="utf-8")
    reader = csv.DictReader(wrapper)

    rows = 0
    for row in reader:
        contactInfo = _parseContactsRow(row)
        status = ContactStatusModelORM.getOrCreateStatusByName(contactInfo.status)
        city = CityModelORM.getCityByName(contactInfo.city)
        contact = Contact(name=contactInfo.name, lastName=contactInfo.lastName, email=contactInfo.email, phone=contactInfo.phoneNumber, city=city, status=status)
        contact.save()
        rows+=1
    return rows