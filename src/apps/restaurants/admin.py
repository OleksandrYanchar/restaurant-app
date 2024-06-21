# apps/restaurants/admin.py

from django.contrib import admin
from .models import Restaurant, Menu, MenuItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1  # Number of extra blank menu items to display

class MenuInline(admin.TabularInline):
    model = Menu
    extra = 1  # Number of extra blank menus to display
    show_change_link = True

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'contact_phone', 'email', 'owner')
    search_fields = ('title', 'address', 'owner__username')
    list_filter = ('owner',)
    inlines = [MenuInline]

class MenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'day')
    list_filter = ('restaurant', 'day')
    search_fields = ('restaurant__title', 'day')
    inlines = [MenuItemInline]

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('menu', 'name', 'price')
    search_fields = ('menu__restaurant__title', 'name')
    list_filter = ('menu__restaurant', 'menu__day')

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
