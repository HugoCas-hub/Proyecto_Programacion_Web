from django.apps import AppConfig

class GestionClientesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_clientes'

    def ready(self):
        # Esta línea es la "llave" que activa las Signals del models.py
        import gestion_clientes.models
        import gestion_clientes.signals