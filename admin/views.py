from user.models import CustomUser
from challenges.models import Challenge
from user.serializers import CustomUserSerializer
from challenges.serializers import ChallengeSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ChallengeList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class ChallengeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
