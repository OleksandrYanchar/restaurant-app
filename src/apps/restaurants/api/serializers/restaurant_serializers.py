from rest_framework import serializers

from apps.restaurants.models import Employee, Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['title', 'address', 'contact_phone', 'email']

class RestaurantEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['title', 'address', 'contact_phone', 'email']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['user', 'role']
