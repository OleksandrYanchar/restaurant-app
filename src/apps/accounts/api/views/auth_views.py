import logging
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.api.serializers.auth_serializers import (
    ChangePasswordSerializer, CheckResetUserPasswordEmailSerializer, MyTokenObtainPairSerializer, PasswordResetConfirmSerializer, UserAuthSerializer)
from apps.accounts.models import User
from apps.accounts.services.email import _send_password_reset_email, _send_verification_email
from apps.accounts.services.generate_token import create_jwt_pair_for_user
from django.utils.encoding import  force_str
from django.utils.http import  urlsafe_base64_decode

from apps.accounts.services.tokens import EmailTokenGenerator


class UserLoginView(APIView):
    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        
        if user is not None:
            _send_verification_email(request, user)
            return Response(
                data={
                    "user_id": str(user.id),
                    "tokens": create_jwt_pair_for_user(user=user),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={
                    "message": "Invalid email or password combination",
                    "status": status.HTTP_401_UNAUTHORIZED,
                },
            )


class UserRegistrationView(APIView):
    def post(self, request):
        data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password1": request.data.get("password_1"),
            "password2": request.data.get("password_2"),
        }

        serializer = UserAuthSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            _send_verification_email(request, user)


            return Response(
                data={
                    "user_id": str(user.id),
                    "tokens": create_jwt_pair_for_user(user=user),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            data={"message": serializer.errors, "status": status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"message": "Password updated", "status": status.HTTP_200_OK},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(
            {"message": "User successfully deleted."}, status=status.HTTP_200_OK
        )


class ActivateView(APIView):
    def get(self, request, uidb64, token):
        try:
            unique_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=unique_id)

            if user and EmailTokenGenerator().check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Account activated", "status": status.HTTP_200_OK})
        except User.DoesNotExist:
            return Response({"message": "User does not exist", "status": status.HTTP_404_NOT_FOUND})
        except Exception as e:
            return Response({"message": str(e), "status": status.HTTP_400_BAD_REQUEST})

        return Response({"message": "Account activation failed", "status": status.HTTP_400_BAD_REQUEST})
    
class CheckResetUserPasswordEmailView(UpdateAPIView):
    serializer_class = CheckResetUserPasswordEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            if email:
                user = get_object_or_404(User, email=email)
                _send_password_reset_email(request, user)
                return Response({'message': 'Reset password email was sent successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'Email not provided'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
logger = logging.getLogger(__name__)

class PasswordResetView(APIView):
    serializer_class = PasswordResetConfirmSerializer
    
    def get_user(self, uidb64):
            try:
                unique_id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=unique_id)
                return user
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return None
    
    def post(self, request, uidb64, token):
        
        user = self.get_user(uidb64)
        
        request_data = {
            'new_password1': request.data.get('new_password_1', ''),
            'new_password2': request.data.get('new_password_2', '')
        }
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password1']


            if user and EmailTokenGenerator().check_token(user, token):
                logger.info(f"Password reset for user: {user.email}, {new_password}")
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
