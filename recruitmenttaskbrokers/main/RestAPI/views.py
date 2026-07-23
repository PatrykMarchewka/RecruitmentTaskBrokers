from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from recruitmenttaskbrokers.main.ContactRow import parseContactsRow
from recruitmenttaskbrokers.main.ORM.ContactsModelORM import addContact, updateContact
from recruitmenttaskbrokers.main.models import Contact
from recruitmenttaskbrokers.main.RestAPI.APISerializers import ContactSerializer

class ContactsView(APIView):
    """
    API endpoint that allows contacts to be viewed or edited
    """

    def get(self, request):
        query = Contact.objects.select_related("city", "status").all()
        return Response(ContactSerializer(query, many=True).data)


    def post(self, request):
        contactRow = parseContactsRow(request.data)
        contact = Contact.objects.filter(email=contactRow.email).first()
        if contact is None:
            addContact(contactRow)
            return Response(ContactSerializer(contact).data, status=status.HTTP_201_CREATED)
        else:
            return Response("Failed to create contact", status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def put(self, request, ID):
        contact = get_object_or_404(Contact, ID=ID)
        contactRow = parseContactsRow(request.data)
        updateContact(contact, contactRow)
        return Response(ContactSerializer(contact).data, status=status.HTTP_200_OK)

    def delete(self, request, ID):
        contact = get_object_or_404(Contact, ID=ID)
        contact.delete()
        return Response("Deleted contact", status=status.HTTP_200_OK)