from django.contrib import admin

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "joined_at")
    list_filter = ("id", "username", "email")
    search_fields = ("username", "email")
