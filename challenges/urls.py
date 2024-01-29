from rest_framework.urls import path

from .views import ChallengeList, ChallengeDetail


urlpatterns = [
    path("", ChallengeList.as_view()),
    path("<int:pk>/", ChallengeDetail.as_view())
]
