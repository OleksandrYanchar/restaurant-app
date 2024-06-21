from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.restaurants.models import Menu


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "votes"
        verbose_name = _("vote")
        verbose_name_plural = _("votes")
        unique_together = ("user", "menu")
        app_label = "votes"
