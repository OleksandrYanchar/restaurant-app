from apps.restaurants.models import Menu, MenuItem


class MenuRepository:
    @staticmethod
    def create_menu(restaurant, day, items_data):
        """
        Create a new menu.

        :param restaurant: The restaurant instance.
        :param day: The day of the week.
        :param items_data: The menu items data.
        :return: The created menu instance.
        """
        menu = Menu(restaurant=restaurant, day=day)
        menu.save()

        items = []
        for item_data in items_data:
            item = MenuItem(menu=menu, name=item_data["name"], price=item_data["price"])
            item.save()
            items.append(item)

        menu.items.set(items)
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
        Edit an existing menu and its items.

        :param menu_id: The ID of the menu to edit.
        :param kwargs: The fields to update including 'items' which is a list of item data.
        :return: The updated menu instance, or None if not found.
        """
        try:
            menu = Menu.objects.get(id=menu_id)
            items_data = kwargs.pop("items", None)
            for key, value in kwargs.items():
                if value is not None:
                    setattr(menu, key, value)
            menu.save()

            if items_data is not None:
                # Update or create menu items
                for item_data in items_data:
                    item_id = item_data.get("id")
                    if item_id:
                        try:
                            item = MenuItem.objects.get(id=item_id, menu=menu)
                            for key, value in item_data.items():
                                if key != "id" and value is not None:
                                    setattr(item, key, value)
                            item.save()
                        except MenuItem.DoesNotExist:
                            MenuItem.objects.create(menu=menu, **item_data)
                    else:
                        MenuItem.objects.create(menu=menu, **item_data)

            return menu
        except Menu.DoesNotExist:
            return None

    @staticmethod
    def get_menu_items(menu_id):
        """
        Get all items for a specific menu.

        :param menu_id: The ID of the menu.
        :return: A queryset of menu items.
        """
        return MenuItem.objects.filter(menu_id=menu_id)
