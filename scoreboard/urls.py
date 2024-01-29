from rest_framework.urls import path

from .views import Scoreboard


urlpatterns = [
    path("", Scoreboard.as_view()),
]
