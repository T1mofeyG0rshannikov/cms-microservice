from django.db import models

from settings.models import Messanger, SocialNetwork


class UserSocialNetwork(models.Model):
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.SET_NULL, null=True, verbose_name="соц. сеть")
    adress = models.CharField(max_length=100, verbose_name="адресс")

    site = models.ForeignKey(
        "user.Site", on_delete=models.SET_NULL, null=True, verbose_name="сайт", related_name="socials"
    )

    class Meta:
        verbose_name = "пользовательская соц. сеть"
        verbose_name_plural = "пользовательские соц. сети"


class UserMessanger(models.Model):
    user = models.OneToOneField(
        "user.User", related_name="messanger", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    messanger = models.ForeignKey(Messanger, on_delete=models.CASCADE, verbose_name="Соц. сеть")
    adress = models.CharField(verbose_name="адресс", max_length=100)
