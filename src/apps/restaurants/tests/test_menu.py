from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant, Menu, MenuItem

User = get_user_model()


class MenuCreationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.restaurant = Restaurant.objects.create(
            title="Test Restaurant", address="123 Test St", owner=self.user
        )

    def test_create_menu(self):
        url = reverse("restaurant-menu-create")
        data = {
            "restaurant": self.restaurant.id,
            "menus": [
                {
                    "day": "Monday",
                    "items": [
                        {"name": "Salad", "price": 23.43},
                        {"name": "Cola", "price": 232.43},
                    ],
                },
                {
                    "day": "Wednesday",
                    "items": [
                        {"name": "Pizza", "price": 99.99},
                        {"name": "Water", "price": 10.00},
                    ],
                },
            ],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(MenuItem.objects.count(), 4)
