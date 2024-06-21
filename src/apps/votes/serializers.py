from datetime import datetime
from rest_framework import serializers
from apps.restaurants.api.serializers.menu_serializers import MenuItemSerializer
from apps.restaurants.models import Menu
from apps.votes.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["user", "menu"]

    def create(self, validated_data):
        vote, created = Vote.objects.update_or_create(
            user=validated_data["user"],
            menu=validated_data["menu"],
            defaults={"voted_at": datetime.now()},
        )
        return vote


class MenuWithVotesSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["id", "day", "items", "votes_count"]

    def get_votes_count(self, obj):
        return Vote.objects.filter(menu=obj).count()
