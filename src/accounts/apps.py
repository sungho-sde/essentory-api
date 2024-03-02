from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials
import os
import base64
import json

# Get the encoded string from environment variable
encoded_json = os.getenv("FIREBASE_ADMIN_SDK_JSON_BASE64")

# Decode the Base64 string
decoded_json = base64.b64decode(encoded_json)

# Convert to a Python dictionary
firebase_admin_sdk_json = json.loads(decoded_json)


class FirebaseAccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        cred = credentials.Certificate(firebase_admin_sdk_json)
        firebase_admin.initialize_app(cred)
