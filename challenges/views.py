from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .serializers import ChallengeListSerializer, ChallengeDetailSerializer, SubmitFlagSerializer
from .models import Challenge


class ChallengeList(APIView):
    def get(self, request):
        try:
            challenges = Challenge.objects.all()
            challenges_serializer = ChallengeListSerializer(
                challenges, many=True)
            return Response(data=challenges_serializer.data, status=status.HTTP_200_OK)
        except Challenge.DoesNotExist:
            return Response(data={'error': 'Challenges not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChallengeDetail(APIView):

    def get(self, request, pk):
        try:
            challenge = Challenge.objects.get(pk=pk)
            challenge_serializer = ChallengeDetailSerializer(challenge)
            return Response(data=challenge_serializer.data, status=status.HTTP_200_OK)
        except Challenge.DoesNotExist:
            return Response(data={'error': 'Challenge not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response(data={'error': 'Authentication required.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if request.user.challenges.filter(id=pk).exists():
            return Response(data={'error': 'Already solved'}, status=status.HTTP_400_BAD_REQUEST)

        flag_serializer = SubmitFlagSerializer(data=request.data)
        if not flag_serializer.is_valid():
            return Response(
                data=flag_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        flag = flag_serializer.data['flag']
        try:
            challenge = Challenge.objects.get(pk=pk)
        except Challenge.DoesNotExist:
            return Response(data={'error': 'Challenge not found.'}, status=status.HTTP_404_NOT_FOUND)

        if challenge.flag == flag:
            user = request.user
            user.challenges.add(challenge)
            user.save()
            user_score = user.challenges.aggregate(
                score=Sum('score'))['score']
            return Response(data={'success': 'Flag submitted successfully.',
                                  'score': user_score}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': 'Incorrect flag.'},
                            status=status.HTTP_400_BAD_REQUEST)
