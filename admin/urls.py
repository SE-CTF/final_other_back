from rest_framework.urls import path

from .views import UserList, UserDetail, ChallengeList, ChallengeDetail


urlpatterns = [
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
    path("challenges/", ChallengeList.as_view()),
    path("challenges/<int:pk>/", ChallengeDetail.as_view()),
]
