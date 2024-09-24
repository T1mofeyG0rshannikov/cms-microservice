from django.db.models.signals import post_save

from infrastructure.persistence.models.site_tests import TestUserSet
from web.site_tests.user_generator.user_generator import get_user_generator


def create_test_user_set_handler(sender, instance, created, *args, **kwargs):
    if created:
        user_generator = get_user_generator(instance)
        user_generator.create_test_users(instance.users_count)


post_save.connect(create_test_user_set_handler, sender=TestUserSet)
