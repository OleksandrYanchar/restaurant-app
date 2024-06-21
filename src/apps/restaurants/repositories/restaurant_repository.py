from apps.accounts.models import User
from apps.restaurants.models import Restaurant, Menu

class RestaurantRepository:
    @staticmethod
    def create_restaurant(title, user, address, contact_phone, email):
        """
        Create a new restaurant.

        :param title: The title of the restaurant.
        :param user: The owner of the restaurant.
        :param address: The address of the restaurant.
        :param contact_phone: The contact phone of the restaurant.
        :param email: The email of the restaurant.
        :return: The created restaurant instance.
        """
        restaurant = Restaurant(
            title=title,
            address=address,
            contact_phone=contact_phone,
            email=email,
            owner=user
        )
        restaurant.save()
        return restaurant

    @staticmethod
    def edit_restaurant(restaurant_id, **kwargs):
        """
        Edit an existing restaurant.

        :param restaurant_id: The ID of the restaurant to edit.
        :param kwargs: The fields to update.
        :return: The updated restaurant instance, or None if not found.
        """
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            for key, value in kwargs.items():
                if value is not None:
                    setattr(restaurant, key, value)
            restaurant.save()
            return restaurant
        except Restaurant.DoesNotExist:
            return None

class MenuRepository:
    @staticmethod
    def create_menu(restaurant, day, items):
        """
        Create a new menu.

        :param restaurant: The restaurant instance.
        :param day: The day of the week.
        :param items: The menu items.
        :return: The created menu instance.
        """
        menu = Menu(restaurant=restaurant, day=day, items=items)
        menu.save()
        return menu

    @staticmethod
    def get_menu_by_day(restaurant, day):
        """
        Get the menu for a specific day.

        :param restaurant: The restaurant instance.
        :param day: The day of the week.
        :return: The menu instance, or None if not found.
        """
        try:
            return Menu.objects.get(restaurant=restaurant, day=day)
        except Menu.DoesNotExist:
            return None

    @staticmethod
    def edit_menu(menu_id, **kwargs):
        """
        Edit an existing menu.

        :param menu_id: The ID of the menu to edit.
        :param kwargs: The fields to update.
        :return: The updated menu instance, or None if not found.
        """
        try:
            menu = Menu.objects.get(id=menu_id)
            for key, value in kwargs.items():
                if value is not None:
                    setattr(menu, key, value)
            menu.save()
            return menu
        except Menu.DoesNotExist:
            return None
