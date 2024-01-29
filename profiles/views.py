from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from user.serializers import CustomUserSerializer
from user.models import CustomUser


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_serializer = CustomUserSerializer(request.user)
            return Response(data=user_serializer.data, status=status.HTTP_200_OK)
        except request.user.DoesNotExist:
            return Response(data={'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            user = request.user
        except request.user.DoesNotExist:
            return Response(data={'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user_serializer = CustomUserSerializer(
            user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data=user_serializer.data, status=status.HTTP_200_OK)

        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
