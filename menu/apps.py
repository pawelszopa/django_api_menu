from django.apps import AppConfig
import os

app_name = 'menu'

class MenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu'

    if os.environ.get('RUN_MAIN', None) != 'true':
        from menu.jobs import start_scheduler
        start_scheduler()
