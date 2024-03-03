from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, FirebaseSignupView, FirebaseLoginView, CheckDuplicateUsernameView

router = DefaultRouter()
router.register("", AccountViewSet, basename='accounts')

urlpatterns = [
    path("firebase/signup/", FirebaseSignupView.as_view(), name="firebase_signup"),
    path("firebase/login/", FirebaseLoginView.as_view(), name="firebase_login"),
    path(
        "check-duplicate-username/",
        CheckDuplicateUsernameView.as_view(),
        name="check-username",
    ),
    path('', include(router.urls)),
]
