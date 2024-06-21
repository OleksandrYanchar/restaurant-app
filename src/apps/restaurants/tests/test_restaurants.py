from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant
from apps.restaurants.api.serializers.restaurant_serializers import RestaurantSerializer

User = get_user_model()

class RestaurantTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.restaurant = Restaurant.objects.create(title="Test Restaurant", address="123 Test St", owner=self.user)

    def test_create_restaurant(self):
        url = reverse('restaurant-create')
        data = {
            "title": "New Restaurant",
            "address": "456 New St",
            "contact_phone": "123-456-7890",
            "email": "newrestaurant@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)
        self.assertEqual(Restaurant.objects.get(title="New Restaurant").address, "456 New St")

    def test_update_restaurant(self):
        url = reverse('restaurant-edit', kwargs={'pk': self.restaurant.pk})
        data = {
            "title": "Updated Test Restaurant",
            "address": "789 Updated St",
            "contact_phone": "987-654-3210",
            "email": "updated@example.com"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.title, "Updated Test Restaurant")
        self.assertEqual(self.restaurant.address, "789 Updated St")
        self.assertEqual(self.restaurant.contact_phone, "987-654-3210")
        self.assertEqual(self.restaurant.email, "updated@example.com")
