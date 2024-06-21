import logging
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.votes.models import Menu, Vote
from apps.votes.serializers import MenuWithVotesSerializer, VoteSerializer
from datetime import datetime


class VoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        today = datetime.today().strftime("%A")
        logging.info(f"Today's day: {today}")
        menu_id = request.data.get("menu_id")
        logging.info(f"Received menu_id: {menu_id}")

        try:
            menu = Menu.objects.get(id=menu_id, day=today)
        except Menu.DoesNotExist:
            logging.error(f"Menu with id {menu_id} not found for today ({today}).")
            return Response(
                {"detail": "Menu not found for today."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = {"user": request.user.id, "menu": menu.id}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodayMenusWithVotesView(generics.ListAPIView):
    serializer_class = MenuWithVotesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = datetime.today().strftime("%A")
        return Menu.objects.filter(day=today)
