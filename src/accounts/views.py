from django.contrib.auth import get_user_model
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from firebase_admin import auth
from .models import User
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class FirebaseLogin(views.APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get("token")  # Token obtained from the client
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get("uid")
            user, created = User.objects.get_or_create(username=uid)

            # Optionally update user details here
            if created:
                pass

            return Response(
                {"status": "success", "created": created}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
