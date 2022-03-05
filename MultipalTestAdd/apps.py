from django.apps import AppConfig


class MultipaltestaddConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MultipalTestAdd'
    def ready(self):
        import MultipalTestAdd.signals
