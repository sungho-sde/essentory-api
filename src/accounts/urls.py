from django.urls import path
from .views import FirebaseLogin

urlpatterns = [
    path("firebase/login/", FirebaseLogin.as_view(), name="firebase_login"),
]
