import firebase_admin.auth as firebase_auth
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from firebase_admin.exceptions import FirebaseError
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Device, User
from .serializers import (
    DeviceSerializer,
    EmailVerificationStatusSerializer,
    FirebaseLoginRequestSerializer,
    FirebaseSignoutRequestSerializer,
    FirebaseSignupRequestSerializer,
    UsernameQuerySerializer,
    UserSerializer,
)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "uid"


class FirebaseSignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_serializer(self, *args, **kwargs):
        return FirebaseSignupRequestSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_serializer = FirebaseSignupRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            uid = request_serializer.validated_data.get("uid")
        else:
            return Response(
                request_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        if not uid:
            return Response(
                {"error": "Firebase UID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            firebase_user = firebase_auth.get_user(uid)
            # Check if user exists to prevent duplicate signups
            if User.objects.filter(email=firebase_user.email).exists():
                return Response(
                    {"error": "User with the same email already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user_data = {
                "uid": firebase_user.uid,
                "email": firebase_user.email,
                "username": request.data.get(
                    "username", firebase_user.email.split("@")[0]
                ),  # Default username to part of email if not provided
            }

            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FirebaseError as e:
            return Response(
                {"error": "Invalid Firebase UID or Firebase Error: " + str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class FirebaseLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_serializer(self, *args, **kwargs):
        return FirebaseLoginRequestSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_serializer = FirebaseLoginRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            uid = request_serializer.validated_data.get("uid")
        else:
            return Response(
                request_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        uid = request.data.get("uid")
        device_id = request.data.get("device_id", None)  # Optional
        push_token = request.data.get("push_token", None)  # Optional

        if not uid:
            return Response(
                {"error": "Firebase UID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            firebase_user = firebase_auth.get_user(uid)
            user = User.objects.get(uid=firebase_user.uid)

            response_data = {"user": UserSerializer(user).data}

            # Only proceed with device handling if device_id is provided
            if device_id:
                device_data = {"device_id": device_id, "push_token": push_token}
                device_serializer = DeviceSerializer(
                    data=device_data, context={"request": request}
                )

                if device_serializer.is_valid():
                    device = device_serializer.save(
                        user=user
                    )  # Pass user to save method
                    response_data["device"] = device_serializer.data
                else:
                    return Response(
                        device_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        except FirebaseError:
            return Response(
                {"error": "Invalid Firebase UID"}, status=status.HTTP_400_BAD_REQUEST
            )


class FirebaseSignoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_serializer(self, *args, **kwargs):
        return FirebaseSignoutRequestSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_serializer = FirebaseSignoutRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            uid = request_serializer.validated_data.get("uid")
            device_id = request_serializer.validated_data.get(
                "device_id", None
            )  # Device ID is optional
        else:
            return Response(
                request_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        if not uid:
            return Response(
                {"error": "Firebase UID is required for signout."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if device_id:
            try:
                # Find the device associated with the user's UID and device ID, if provided
                device = Device.objects.get(user__uid=uid, device_id=device_id)
                device.push_token = None  # Optionally clear the push token
                device.save()  # Save the changes to the device

                return Response(
                    {"success": "User successfully signed out from the device."},
                    status=status.HTTP_200_OK,
                )
            except ObjectDoesNotExist:
                return Response(
                    {"error": "Device not found."}, status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                # Log the error for debugging purposes
                print(f"Error during signout with device ID: {e}")
                return Response(
                    {"error": "An error occurred during signout."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            # If no device ID is provided, simply acknowledge the sign-out request
            return Response(
                {"success": "Signout request acknowledged."}, status=status.HTTP_200_OK
            )


class PushTokenUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        device_id = request.data.get("device_id")
        push_token = request.data.get("push_token")

        if not push_token or not device_id:
            return Response(
                {"error": "Both push token and device ID are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            device, created = Device.objects.get_or_create(
                user=request.user, device_id=device_id
            )
            device.push_token = push_token
            device.save()
            return Response({"message": "Push token updated successfully."})
        except Device.DoesNotExist:
            return Response(
                {"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CheckDuplicateUsernameView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_serializer(self, *args, **kwargs):
        return UsernameQuerySerializer(*args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="username",
                description="Username to check for duplicates",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
            )
        ],
        responses={200: OpenApiResponse(description="Description of the response")},
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")

        if not username:
            return Response(
                {"error": "Username parameter is missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # try:
        #     # Validate username
        #     User.objects.validate_username(username)
        # except ValidationError as e:
        #     return Response(
        #         {"valid": False, "error": str(e)}, status=status.HTTP_200_OK
        #     )

        exists = User.objects.filter(username=username).exists()
        if exists:
            return Response(
                {"valid": False, "error": "This username is already taken."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"valid": True, "message": "This username is available."},
                status=status.HTTP_200_OK,
            )


class CheckEmailVerificationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        return EmailVerificationStatusSerializer

    def get(self, request, uid):
        try:
            user = firebase_auth.get_user(uid)
            data = {"uid": uid, "email_verified": user.email_verified}
            serializer = EmailVerificationStatusSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
        except firebase_auth.UserNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
