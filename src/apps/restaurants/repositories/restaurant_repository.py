from apps.accounts.models import User
from apps.restaurants.models import Employee, Restaurant


class RestaurantRepository:
    @staticmethod
    def create_restaurant(title, owner, address=None, contact_phone=None, email=None):
        restaurant = Restaurant(title=title, address=address, contact_phone=contact_phone, email=email)
        restaurant.save()
        Employee.objects.create(user=owner, restaurant=restaurant, role=Employee.OWNER)
        return restaurant

    @staticmethod
    def edit_restaurant(restaurant_id, **kwargs):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            for key, value in kwargs.items():
                if value is not None:
                    setattr(restaurant, key, value)
            restaurant.save()
            return restaurant
        except Restaurant.DoesNotExist:
            return None

    @staticmethod
    def add_employee(restaurant_id, user_id, role):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            user = User.objects.get(id=user_id)
            employee = Employee.objects.create(user=user, restaurant=restaurant, role=role)
            return employee
        except (Restaurant.DoesNotExist, User.DoesNotExist):
            return None

    @staticmethod
    def remove_employee(restaurant_id, user_id):
        try:
            employee = Employee.objects.get(restaurant_id=restaurant_id, user_id=user_id)
            employee.delete()
            return True
        except Employee.DoesNotExist:
            return False

    @staticmethod
    def get_restaurant(restaurant_id):
        try:
            return Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return None

    @staticmethod
    def get_all_restaurants():
        return Restaurant.objects.all()

