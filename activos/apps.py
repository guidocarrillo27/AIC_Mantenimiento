from django.apps import AppConfig


class ActivosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'activos'

    def ready(self):
        import activos.signals  # Aquí estamos asegurándonos de que las señales se registren

