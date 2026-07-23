from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .ORM import CityWeatherModelORM, ContactsModelORM
from recruitmenttaskbrokers.main.CSV.CSVImport import importCSV
from recruitmenttaskbrokers.main.CSV.CSVExport import exportCSV
from .ContactRow import parseContactsRow
from .forms import ContactForm
from .models import Contact


def ContactListGet(request):
    sort = request.GET.get('sort', 'lastName')
    search = request.GET.get('search', None)

    #Filtering by name and last name
    contacts = ContactsModelORM.getFilteredContacts(search, None)
    contacts = ContactsModelORM.getSortedContacts(sort, contacts)

    #Checking if whether has to be refreshed to ensure correct weather
    for contact in contacts:
        contact.city.weather = CityWeatherModelORM.getWeatherForCity(contact.city)
        contact.city.save()


    return render(request, 'contacts/contactList.html', {'contacts': contacts})

def ContactListDelete(request, contactID):
    contact = get_object_or_404(Contact,ID=contactID)
    contact.delete()
    messages.success(request, 'Contact Deleted Successfully')
    return redirect('contactList')

def ContactCreate(request):
    #Sending filled form
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form_CLEANED = form.cleaned_data
            contact = parseContactsRow(form_CLEANED)
            addedContact = ContactsModelORM.addContact(contact)
            if addedContact is not None:
                messages.success(request, 'Contact Created Successfully')
                #Clear form to allow adding multiple people back to back
                form = ContactForm()
            else:
                messages.error(request, 'Failed to create contact')
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, f'{error}')
    #Getting empty form
    else:
        form = ContactForm()
    return render(request, 'contacts/contactEdit.html', {'form': form})

def ContactEdit(request, contactID):
    contact = get_object_or_404(Contact,ID=contactID)

    #Sending edited form
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form_CLEANED = form.cleaned_data
            contactRow = parseContactsRow(form_CLEANED)
            ContactsModelORM.updateContact(contact, contactRow)
            messages.success(request, 'Contact Updated Successfully')
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, f'{error}')
    #Getting form for contact
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contacts/contactEdit.html', {'form': form})

def ContactImport(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if file is None:
            messages.error(request, "No file uploaded")

        if not file.name.endswith(".csv"):
            messages.error(request, "File must have .csv extension")
            return redirect('contactImport')

        count = importCSV(file)
        messages.success(request, f"Imported {count} rows")
        return redirect('contactImport')

    return render(request, "contacts/contactImport.html")

def ContactExport(request):
    rows = exportCSV()
    messages.success(request, f"Exported {rows} rows")
    return redirect('contactImport')
