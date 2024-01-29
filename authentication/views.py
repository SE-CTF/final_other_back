from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from user.models import CustomUser
from user.serializers import CustomUserSerializer
from .serializers import LoginSerializer, SignupSerializer


class SignupView(APIView):
    def post(self, request):
        signup_serializer = SignupSerializer(data=request.data)
        if not signup_serializer.is_valid():
            return Response(
                signup_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_serializer = CustomUserSerializer(data=signup_serializer.data)
        if not user_serializer.is_valid():
            return Response(
                data=user_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = user_serializer.save()
        if user is None:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        access = AccessToken.for_user(user)
        response_user = CustomUserSerializer(instance=user)
        response = {
            "user": response_user.data,
            "access": str(access),
        }
        return Response(
            data=response,
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        if not login_serializer.is_valid():
            return Response(
                data=login_serializer.errors,
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            user = CustomUser.objects.get(email=login_serializer.data["email"])
        except CustomUser.DoesNotExist:
            return Response(
                data={"message": "Email or Password is wrong"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not CustomUser.check_password(user, login_serializer.data["password"]):
            return Response(
                data={"message": "Email or Password is wrong"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access = AccessToken.for_user(user)
        serialized_user = CustomUserSerializer(instance=user)
        response = {
            "user": serialized_user.data,
            "access": str(access),
        }
        return Response(data=response, status=status.HTTP_200_OK)
