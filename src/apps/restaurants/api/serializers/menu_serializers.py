from rest_framework import serializers

from apps.restaurants.models import Menu, MenuItem, Restaurant


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "price", "picture"]


class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)

    class Meta:
        model = Menu
        fields = ["id", "day", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        menu = Menu.objects.create(**validated_data)
        for item_data in items_data:
            MenuItem.objects.create(menu=menu, **item_data)
        return menu

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items")
        instance.day = validated_data.get("day", instance.day)
        instance.save()

        # Clear existing items and add new ones
        instance.items.all().delete()
        for item_data in items_data:
            MenuItem.objects.create(menu=instance, **item_data)
        return instance


class RestaurantMenuSerializer(serializers.Serializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    menus = MenuSerializer(many=True)

    def create(self, validated_data):
        restaurant = validated_data["restaurant"]
        menus_data = validated_data["menus"]
        for menu_data in menus_data:
            items_data = menu_data.pop("items")

            # Delete the old menu for the same day if it exists
            Menu.objects.filter(restaurant=restaurant, day=menu_data["day"]).delete()

            menu = Menu.objects.create(restaurant=restaurant, **menu_data)
            for item_data in items_data:
                MenuItem.objects.create(menu=menu, **item_data)
        return validated_data

    def to_representation(self, instance):
        restaurant = instance["restaurant"]
        menus = Menu.objects.filter(restaurant=restaurant)
        return {
            "restaurant": restaurant.id,
            "menus": [
                {
                    "id": menu.id,
                    "day": menu.day,
                    "items": MenuItemSerializer(menu.items.all(), many=True).data,
                }
                for menu in menus
            ],
        }
