# RecruitmentTaskBrokers
## Tech stack
### Backend:
- Python 3.14
- Django 6.0.7
- Django REST Framework 3.17.1
- SQLite

### Frontend:
- HTML
- Bootstrap 5 (CDN)

## Requirements:
- Python (Tested on Python 3.14)

Python libraries:
- asgiref (3.12.1)
- Django (6.0.7)
- djangorestframework (3.17.1)
- sqlparse (0.5.5)
- typing_extensions (4.16.0)
- tzdata (2026.3)

## Run the application
Python:

Run `python manage.py runserver`

Docker

Build `docker build -t recruitmenttaskbrokers .`

Run `docker run -p 127.0.0.1:8000:8000 recruitmenttaskbrokers`

>Application is set to auto migrate database using command in apps.py