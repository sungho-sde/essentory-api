from django.urls import path
from .views import FirebaseSignupView, FirebaseLoginView, CheckDuplicateUsernameView

urlpatterns = [
    path("firebase/signup/", FirebaseSignupView.as_view(), name="firebase_signup"),
    path("firebase/login/", FirebaseLoginView.as_view(), name="firebase_login"),
    path(
        "check-duplicate-username/",
        CheckDuplicateUsernameView.as_view(),
        name="check-username",
    ),
]
