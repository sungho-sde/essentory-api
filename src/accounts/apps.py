from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        cred = credentials.Certificate("path/to/your/firebase-adminsdk.json")
        firebase_admin.initialize_app(cred)
