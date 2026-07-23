from collections import namedtuple

ContactRow = namedtuple("ContactRow", ["name", "lastName", "email", "phone", "city", "status"])

def parseContactsRow(row: dict) -> ContactRow:
    """
    Converts raw dictionary object with Contact data into ContactRow object
    :param row: dictionary object with Contact data, requires fields "name", "lastName", "email", "phone", "city", "status
    :return:
    """
    name = row["name"]
    lastName = row["lastName"]
    email = row["email"]
    phoneNumber = row["phone"]
    city = row["city"]
    status = row["status"]
    return ContactRow(name, lastName, email, phoneNumber, city, status)