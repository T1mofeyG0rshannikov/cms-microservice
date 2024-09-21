from django.db import models

from web.settings.models import Messanger, SocialNetwork
from web.user.models.site import Site
from web.user.models.user import User


class UserSocialNetwork(models.Model):
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.SET_NULL, null=True, verbose_name="соц. сеть")
    adress = models.CharField(max_length=100, verbose_name="адресс")

    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, verbose_name="сайт", related_name="socials")

    class Meta:
        app_label = "account"
        verbose_name = "пользовательская соц. сеть"
        verbose_name_plural = "пользовательские соц. сети"


class UserMessanger(models.Model):
    user = models.OneToOneField(
        User, related_name="messanger", on_delete=models.CASCADE, verbose_name="Пользователь", null=True
    )
    messanger = models.ForeignKey(Messanger, on_delete=models.CASCADE, verbose_name="Соц. сеть", null=True)
    adress = models.CharField(verbose_name="адресс", max_length=100)

    class Meta:
        app_label = "account"
