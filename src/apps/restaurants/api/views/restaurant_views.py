from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.restaurants.api.serializers.restaurant_serializers import (
    RestaurantEditSerializer,
    RestaurantSerializer,
)
from apps.restaurants.models import Restaurant
from apps.restaurants.permissions import IsOwner
from apps.restaurants.repositories.restaurant_repository import RestaurantRepository


class RestaurantCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = RestaurantSerializer(data=request.data)
        try:
            if serializer.is_valid():
                data = serializer.validated_data
                restaurant = RestaurantRepository.create_restaurant(
                    title=data.get("title"),
                    owner=request.user,
                    address=data.get("address"),
                    contact_phone=data.get("contact_phone"),
                    email=data.get("email"),
                )
                return Response(
                    RestaurantSerializer(restaurant).data,
                    status=status.HTTP_201_CREATED,
                )
        except IntegrityError:
            return Response(
                {"details": "restaurant already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"details": "error creating restaurant"}, status=status.HTTP_400_BAD_REQUEST
        )


class RestaurantEditView(generics.UpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantEditSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
