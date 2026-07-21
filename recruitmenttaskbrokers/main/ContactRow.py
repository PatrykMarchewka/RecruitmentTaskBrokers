from collections import namedtuple

ContactRow = namedtuple("ContactRow", ["name", "lastName", "email", "phone", "city", "status"])

def parseContactsRow(row: dict) -> ContactRow:
    name = row["name"]
    lastName = row["lastName"]
    email = row["email"]
    phoneNumber = row["phone"]
    city = row["city"]
    status = row["status"]
    return ContactRow(name, lastName, email, phoneNumber, city, status)