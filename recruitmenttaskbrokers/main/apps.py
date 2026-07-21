from django.apps import AppConfig
from django.core.management import call_command

class MainConfig(AppConfig):
    name = 'recruitmenttaskbrokers.main'

    def ready(self):
        try:
            call_command("makemigrations","main", interactive=False)
            call_command("migrate", interactive=False)
        except Exception:
            pass
