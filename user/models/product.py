from django.db import models
from django.db.models.signals import pre_save

from catalog.models.products import Product
from user.exceptions import UserProductAlreadyExists
from user.models.user import User


def user_directory_path(instance, filename):
    return f"images/{instance.user_id}/{filename}"


class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    connected = models.DateField(null=True)
    profit = models.DateField(null=True)
    got = models.DateField(null=True)
    connected_with_link = models.BooleanField(null=True)
    redirections = models.PositiveIntegerField(default=0)
    screen = models.ImageField(upload_to=user_directory_path, null=True)
    comment = models.CharField(null=True, max_length=1000)

    link = models.CharField(null=True, max_length=1000)
    gain = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Пользовательские продукты"
        verbose_name_plural = "Пользовательские продукты"

    def __str__(self):
        return f"{self.user.full_name} - {self.product}"


def create_user_product_handler(sender, instance, *args, **kwargs):
    if not instance.id:
        if UserProduct.objects.filter(user=instance.user, product=instance.product).exists():
            raise UserProductAlreadyExists()


pre_save.connect(create_user_product_handler, sender=UserProduct)
