from django.db import models

from common.models import BaseFont, SocialNetwork


class UserFont(BaseFont):
    class Meta:
        verbose_name = "пользовательский шрифт"
        verbose_name_plural = "пользовательские шрифты"


class UserSocialNetwork(models.Model):
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.SET_NULL, null=True, verbose_name="соц. сеть")
    adress = models.CharField(max_length=100, verbose_name="адресс")

    site = models.ForeignKey(
        "domens.Site", on_delete=models.SET_NULL, null=True, verbose_name="сайт", related_name="socials"
    )

    class Meta:
        verbose_name = "пользовательская соц. сеть"
        verbose_name_plural = "пользовательские соц. сети"
