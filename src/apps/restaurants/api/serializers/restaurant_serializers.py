from rest_framework import serializers

from apps.restaurants.models import Menu, MenuItem, Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['title', 'address', 'contact_phone', 'email']

class RestaurantEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['title', 'address', 'contact_phone', 'email']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
