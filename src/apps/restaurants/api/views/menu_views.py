from datetime import datetime
from rest_framework import views, permissions, status, generics
from rest_framework.response import Response

from apps.restaurants.api.serializers.menu_serializers import MenuSerializer, RestaurantMenuSerializer
from apps.restaurants.models import Menu


class RestaurantMenuCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = RestaurantMenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TodayMenusView(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        today = datetime.today().strftime('%A')  # Get the current day of the week
        return Menu.objects.filter(day=today)