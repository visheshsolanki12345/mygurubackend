from django.apps import AppConfig

class CareermanagementsystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CareerManagementSystem'
    def ready(self):
        import CareerManagementSystem.signals
