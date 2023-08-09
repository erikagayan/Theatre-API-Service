from django.urls import path
from .views import play_list, play_detail

urlpatterns = [
    path("movies/", play_list, name="movie-list"),
    path("movies/<int:pk>/", play_detail, name="movie-detail"),
]

app_name = "theatre"
