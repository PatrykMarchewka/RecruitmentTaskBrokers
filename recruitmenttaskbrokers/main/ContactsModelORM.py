from typing import Optional

from django.core.exceptions import ValidationError
from django.db.models import QuerySet, Q

from .CityModelORM import getCityByName
from .ContactRow import ContactRow
from .ContactStatusModelORM import getOrCreateStatusByName
from .models import Contact


def getSortedContacts(sort:Optional[str]=None, contacts:Optional[QuerySet[Contact]]=None) -> QuerySet:
    """
    Returns a list of all contacts sorted by the given sort
    :param sort: Optional string representing the sort field, accepts values ['lastName', 'createdAt'], defaults to 'lastName'
    :param contacts: Optional list of Contact objects, defaults to all contacts if not provided
    :return: Sorted list of Contact objects
    """
    if sort not in ['lastName', 'createdAt']:
        sort = 'lastName'

    if contacts is None:
        contacts = Contact.objects.all()

    return contacts.order_by(sort)

def getFilteredContacts(contactFilter:Optional[str]=None, contacts:Optional[QuerySet[Contact]]=None) -> QuerySet:
    """
    Returns a list of all contacts filtered by the given filter
    :param contactFilter: Optional string representing the filter field
    :param contacts: Optional list of Contact objects, defaults to all contacts if not provided
    :return: List of Contact objects filtered by the given filter applied to first name and last name rows
    """
    if contacts is None:
        contacts = Contact.objects.all()
    if contactFilter is None:
        return contacts

    return contacts.filter(
            Q(name__icontains=contactFilter) |
            Q(lastName__icontains=contactFilter)
        )

def addContact(contactInfo: ContactRow):
    """
    Adds a new contact to the database
    :param contactInfo: Information about contact
    :return: Nothing
    """
    status = getOrCreateStatusByName(contactInfo.status)
    city = getCityByName(contactInfo.city)
    contact = Contact(name=contactInfo.name, lastName=contactInfo.lastName, email=contactInfo.email,phone=contactInfo.phone, city=city, status=status)
    try:
        contact.full_clean()
        contact.save()
    except ValidationError as e:
        print("----------------------")
        print("Error importing contact", contact)
        print("Reason:", e)

def updateContact(contact: Contact, contactInfo: ContactRow):
    """
    Updates existing contact in a database
    :param contact: Contact to update
    :param contactInfo: Updated information about contact
    :return: Nothing
    """
    status = getOrCreateStatusByName(contactInfo.status)
    city = getCityByName(contactInfo.city)

    contact.name = contactInfo.name
    contact.lastName = contactInfo.lastName
    contact.email = contactInfo.email
    contact.phone = contactInfo.phone
    contact.status = status
    contact.city = city
    try:
        contact.full_clean()
        contact.save()
    except ValidationError as e:
        print("----------------------")
        print("Error updating contact", contact)
        print("Reason:", e)