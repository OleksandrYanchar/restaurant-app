from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class Restaurant(models.Model):
    title = models.CharField(_("title"), max_length=128, blank=False, null=False)
    address = models.CharField(_("address"), max_length=256, blank=True, null=True)
    contact_phone = models.CharField(
        _("contact phone"), max_length=15, blank=True, null=True
    )
    email = models.EmailField(_("email"), blank=True, null=True)
    owner = models.ForeignKey(
        User, related_name="restaurant_owner", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "restaurants"
        verbose_name = _("restaurant")
        verbose_name_plural = _("restaurants")
        app_label = "restaurants"

    def __str__(self):
        return f"{self.title}: {self.address}"


class Menu(models.Model):
    DAYS_OF_WEEK = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]

    restaurant = models.ForeignKey(
        Restaurant, related_name="menus", on_delete=models.CASCADE
    )
    day = models.CharField(
        _("day"), max_length=9, choices=DAYS_OF_WEEK, blank=False, null=False
    )

    class Meta:
        db_table = "menus"
        verbose_name = _("menu")
        verbose_name_plural = _("menus")
        unique_together = ("restaurant", "day")
        app_label = "restaurants"

    def __str__(self):
        return f"Menu for {self.restaurant.title} on {self.day}"


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=128, blank=False, null=False)
    price = models.DecimalField(
        _("price"), max_digits=6, decimal_places=2, blank=False, null=False
    )
    picture = models.ImageField(
        _("picture"), upload_to="menu_pictures/", blank=True, null=True
    )

    class Meta:
        db_table = "menu_items"
        verbose_name = _("menu item")
        verbose_name_plural = _("menu items")
        app_label = "restaurants"

    def __str__(self):
        return f"{self.name} - {self.price}"
