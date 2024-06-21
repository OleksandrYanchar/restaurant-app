from django.urls import path
from apps.restaurants.api.views.restaurant_views import RestaurantCreateView, RestaurantEditView, AddEmployeeView, UpdateEmployeeRoleView

urlpatterns = [
    path('create/', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('edit/<int:pk>/', RestaurantEditView.as_view(), name='restaurant-edit'),
    path('<int:restaurant_id>/add-employee/', AddEmployeeView.as_view(), name='add-employee'),
    path('<int:restaurant_id>/update-employee-role/<uuid:employee_id>/', UpdateEmployeeRoleView.as_view(), name='update-employee-role'),
]
