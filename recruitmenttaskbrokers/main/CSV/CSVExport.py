import csv
import datetime
import os

from django.conf import settings

from recruitmenttaskbrokers.main.models import Contact

def exportCSV():
    """
    Exports all contacts into csv file
    :return: Number of written contacts
    """
    #Using strftime to get rid of invalid signs in windows
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fileName = f"ContactsExport-{now}.csv"

    path = os.path.join(settings.BASE_DIR, fileName)

    #File is overwritten if exists
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Last Name", "Email", "Phone Number", "City", "Status"])

        rows = 0
        for contact in Contact.objects.select_related("city", "status").iterator():
            try:
                writer.writerow([contact.name, contact.lastName, contact.email, contact.phone, contact.city.name, contact.status.name])
                rows += 1
            except Exception as e:
                print("----------------------")
                print("Error exporting contact", contact)
                print("Reason:", e)
        return rows