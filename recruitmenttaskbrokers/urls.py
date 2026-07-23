"""
URL configuration for recruitmenttaskbrokers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from recruitmenttaskbrokers.main.views import *
from recruitmenttaskbrokers.main.RestAPI.views import *

urlpatterns = [
    path('contacts/contactList/', ContactListGet, name='contactList'),
    path('contacts/contactEdit/', ContactCreate, name='contactCreate'),
    path('contacts/contactEdit/<int:contactID>', ContactEdit, name='contactEdit'),
    path('contacts/contactDelete/<int:contactID>/', ContactListDelete, name='contactDelete'),
    path('contacts/contactImport/', ContactImport, name='contactImport'),
    path('contacts/contactExport/', ContactExport, name='contactExport'),
    #REST API
    path("api/contacts/", ContactsView.as_view()),
    path("api/contacts/<int:ID>/", ContactsView.as_view())

]
