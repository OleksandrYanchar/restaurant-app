from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User

class Restaurant(models.Model):
    title = models.CharField(_("title"), max_length=128, blank=False, null=False)
    address = models.CharField(_("address"), max_length=256, blank=True, null=True)
    contact_phone = models.CharField(_("contact phone"), max_length=15, blank=True, null=True)
    email = models.EmailField(_("email"), blank=True, null=True)
    employees = models.ManyToManyField(User, through='Employee', related_name='work_restaurants')

    class Meta:
        db_table = "restaurants"
        verbose_name = _("restaurant")
        verbose_name_plural = _("restaurants")
        app_label = 'restaurants'
        
    def __str__(self):
        return f'title: {self.title}: address: {self.address}'

class Employee(models.Model):
    OWNER = 'owner'
    ADMIN = 'admin'
    MANAGER = 'manager'
    CHEF = 'chef'
    WAITER = 'waiter'
    CLEANER = 'cleaner'
    
    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (ADMIN, 'Administrator'),
        (MANAGER, 'Manager'),
        (CHEF, 'Chef'),
        (WAITER, 'Waiter'),
        (CLEANER, 'Cleaner'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    role = models.CharField(_("role"), max_length=20, choices=ROLE_CHOICES, default=WAITER)

    class Meta:
        unique_together = ('user', 'restaurant')
        db_table = "employees"
        verbose_name = _("employee")
        verbose_name_plural = _("employees")
        app_label = 'restaurants'

    def __str__(self):
        return f'user: {self.user.username}: restaurant: {self.restaurant.title}'
