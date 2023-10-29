from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework import status
import json
from .models import Account, Attraction, Comment, Review
from rest_framework.test import APIClient


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create(
            username="test",
            password=make_password("*Test123"),
            email="test@test.com",
            role="client"
        )

    print("test login successful")

    def test_login_successful(self):
        url = reverse('login')
        data = {'username': 'test', 'password': '*Test123'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    print("test login invalid password")

    def test_login_invalid_password(self):
        url = reverse('login')
        data = {'username': 'test', 'password': 'wrongpass'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    print("test login invalid username")

    def test_login_invalid_username(self):
        url = reverse('login')
        data = {'username': 'wronguser', 'password': '*Test123'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AttractionTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.attraction_data = {
            "name": "Test Attraction",
            "location": "Test Location",
            "category": "Test Category",
            "description": "Test Description",
            "path_to_file": "Test Path",
            "role": "Test Role",
            "average_review": 4.5
        }
        self.create_url = reverse('attractionApi')

    print("test add attraction")

    def test_create_attraction(self):
        response = self.client.post(
            self.create_url,
            data=json.dumps(self.attraction_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Attraction.objects.count(), 1)
        self.assertEqual(Attraction.objects.get().name, 'Test Attraction')


