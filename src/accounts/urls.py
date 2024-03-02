from django.urls import path
from .views import FirebaseSignupView, FirebaseLoginView

urlpatterns = [
    path("firebase/signup/", FirebaseSignupView.as_view(), name="firebase_signup"),
    path("firebase/login/", FirebaseLoginView.as_view(), name="firebase_login"),
    # Include other URLs as needed
]
