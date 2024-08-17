from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save

from site_tests.user_generator.user_generator import get_user_generator


class TestUserSet(models.Model):
    users_count = models.PositiveSmallIntegerField(verbose_name="Количество пользователей")

    def __str__(self):
        return f"Тестовый набор пользователей №{self.id}"


def create_test_user_set_handler(sender, instance, created, *args, **kwargs):
    if created:
        user_generator = get_user_generator(instance)
        user_generator.create_test_users(instance.users_count)


post_save.connect(create_test_user_set_handler, sender=TestUserSet)
