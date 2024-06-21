from django.urls import path
from apps.restaurants.api.views.menu_views import RestaurantMenuCreateView, TodayMenusView
from apps.restaurants.api.views.restaurant_views import RestaurantCreateView, RestaurantEditView




urlpatterns = [
    path('create/', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('edit/<int:pk>/', RestaurantEditView.as_view(), name='restaurant-edit'),
    path('menu/create/', RestaurantMenuCreateView.as_view(), name='restaurant-menu-create'),
    path('menus/today/', TodayMenusView.as_view(), name='today-menus'),

]
