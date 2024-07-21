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


class Messanger(models.Model):
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE, verbose_name="Соц. сеть")

    class Meta:
        verbose_name = "Мессенджер"
        verbose_name_plural = "Мессенджеры"

    def __str__(self):
        return str(self.social_network)


class UserMessanger(models.Model):
    user = models.OneToOneField(
        "user.User", related_name="messanger", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    messanger = models.ForeignKey(Messanger, on_delete=models.CASCADE, verbose_name="Соц. сеть")
    adress = models.CharField(verbose_name="адресс", max_length=100)
