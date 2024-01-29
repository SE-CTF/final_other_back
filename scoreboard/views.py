from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status


from user.models import CustomUser


class Scoreboard(APIView):
    def get(self, request):
        try:
            user_scores = CustomUser.objects.annotate(
                score=Coalesce(Sum('challenges__score'), Value(0))
            ).values('username', 'score')

            return Response(data=user_scores, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
