from django.db import models
from django.db.models.signals import pre_save

from domain.user.exceptions import UserProductAlreadyExists
from infrastructure.persistence.models.catalog.products import Offer, Product
from infrastructure.persistence.models.user.user import User


def user_directory_path(instance, filename):
    return f"images/{instance.user_id}/{filename}"


class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products", verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="user_products", verbose_name="Продукт")
    connected = models.DateField(null=True, verbose_name="Подключен")
    profit = models.DateField(null=True, verbose_name="Бонус")
    got = models.DateField(null=True, verbose_name="Получен")
    connected_with_link = models.BooleanField(null=True, verbose_name="Подключен по ссылке")
    redirections = models.PositiveIntegerField(default=0, verbose_name="Переходы")
    screen = models.ImageField(upload_to=user_directory_path, null=True, verbose_name="скриншот")
    comment = models.CharField(null=True, max_length=1000, verbose_name="Комментарий")

    gain = models.PositiveIntegerField(default=0, verbose_name="Доход")

    fully_verified = models.BooleanField(default=False, verbose_name="Полностью подтверждён")

    created_at = models.DateField(auto_now_add=True, null=True)
    deleted = models.BooleanField(default=False, verbose_name="Удален")

    class Meta:
        app_label = "user"
        verbose_name = "Пользовательские продукты"
        verbose_name_plural = "Пользовательские продукты"

    def __str__(self):
        return f"{self.user.full_name} - {self.product}"


class UserOffer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers", verbose_name="Пользователь")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, verbose_name="оффер")
    link = models.CharField(max_length=1000, verbose_name="Ссылка")

    class Meta:
        app_label = "user"


def create_user_product_handler(sender, instance, *args, **kwargs):
    if not instance.id:
        if UserProduct.objects.filter(user=instance.user, product=instance.product).exists():
            raise UserProductAlreadyExists(f'Вы уже добавили себе продукт "{instance.product}"')


pre_save.connect(create_user_product_handler, sender=UserProduct)
