import csv
from collections import namedtuple
from io import TextIOWrapper

from django.core.exceptions import ValidationError

from ContactStatusModelORM import getOrCreateStatusByName
from CityModelORM import getCityByName
from .models import Contact


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
        status = getOrCreateStatusByName(contactInfo.status)
        city = getCityByName(contactInfo.city)
        contact = Contact(name=contactInfo.name, lastName=contactInfo.lastName, email=contactInfo.email, phone=contactInfo.phoneNumber, city=city, status=status)
        try:
            contact.full_clean()
            contact.save()
            rows += 1
        except ValidationError as e:
            print("----------------------")
            print("Error importing contact", contact)
            print("Reason:", e)
    return rows