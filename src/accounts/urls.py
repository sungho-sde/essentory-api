from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, FirebaseSignupView, FirebaseLoginView, CheckDuplicateUsernameView, CheckEmailVerificationView

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
    path("email-verification-status/<str:uid>",
         CheckEmailVerificationView.as_view(),
         name="email-verification-status"),
    path('', include(router.urls)),
]
