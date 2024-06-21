from django.contrib import admin
from .models import Restaurant, Employee

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'contact_phone', 'email')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'role')
