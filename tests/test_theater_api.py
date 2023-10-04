import tempfile
import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import (
    Genre,
    Actor,
    TheatreHall,
    Play,
    Performance,
    Reservation
)

from theatre.serializers import PlayListSerializer, PlayDetailSerializer


PLAY_URL = reverse("theatre:play-list")
PLAY_SESSION_URL = reverse("theatre:performance-list")


def sample_play(**params):
    defaults = {
        "title": "Sample play]",
        "description": "Sample description",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Drama",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "George", "last_name": "Clooney"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_performance(**params):
    theatre_hall = TheatreHall.objects.create(
        name="Blue", rows=20, seats_in_row=20
    )

    defaults = {
        "show_time": "2022-06-02 14:00:00",
        "play": None,
        "theatre_hall": theatre_hall,
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


def detail_url(play_id):
    return reverse("performance:play-detail", args=[play_id])


class UnauthenticatedPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_authenticate_required(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="tuser@test.ua",
            password="pwd12345"
        )
        self.client.force_authenticate(self.user)

    def test_plays_list_access(self):
        sample_play()
        play_with_genre = sample_play()
        genre = sample_genre()

        play_with_genre.genres.add(genre)

        res = self.client.get(PLAY_URL)
        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_play_list_filter_by_title(self):
        play1 = sample_play(title="Movie")
        play2 = sample_play(title="Movie2")
        play3 = sample_play(title="Movie22")

        res = self.client.get(PLAY_URL, {"title": "2"})

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)
        serializer3 = PlayListSerializer(play3)

        self.assertIn(serializer2.data, res.data)
        self.assertIn(serializer3.data, res.data)
        self.assertNotIn(serializer1.data, res.data)

    def test_play_list_filter_by_genres(self):
        play1 = sample_play(title="Movie")
        play2 = sample_play(title="Movie2")
        play3 = sample_play(title="Movie22")

        genre1 = sample_genre()
        genre2 = sample_genre(name="Comedy")

        play1.genres.add(genre1)
        play2.genres.add(genre2)

        res = self.client.get(PLAY_URL, {"genres": f"{genre1.id},{genre2.id}"})

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)
        serializer3 = PlayListSerializer(play3)

        self.assertIn(serializer2.data, res.data)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_play_list_filter_by_actors(self):
        play1 = sample_play(title="Movie")
        play2 = sample_play(title="Movie2")
        play3 = sample_play(title="Movie22")

        actor1 = sample_actor()
        actor2 = sample_actor(first_name="John")

        play1.actors.add(actor1)
        play3.actors.add(actor2)

        res = self.client.get(PLAY_URL, {"actors": f"{actor1.id},{actor2.id}"})

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)
        serializer3 = PlayListSerializer(play3)

        self.assertIn(serializer3.data, res.data)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_play_create_forbidden(self):
        payload = {
            "title": "Play",
            "description": "Play description",
        }
        res = self.client.post(PLAY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="admin@test.ua",
            password="pwd12345",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_play(self):
        actor = sample_actor()
        genre = sample_genre()
        payload = {
            "title": "Play",
            "description": "Play description",
            "genres": [genre.id],
            "actors": [actor.id]
        }
        res = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=res.data["id"])
        genres = play.genres.all()
        actors = play.actors.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(genre, genres)
        self.assertIn(actor, actors)
