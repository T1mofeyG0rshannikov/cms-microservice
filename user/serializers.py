from rest_framework import serializers

from catalog.serializers import ProductsSerializer
from user.models.product import UserProduct
from user.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "second_name",
            "email",
            "phone",
            "phone_is_confirmed",
            "email_is_confirmed",
            "profile_picture",
        ]


class UserProductsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    end_promotion = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = UserProduct
        fields = ["id", "product", "connected", "gain", "end_promotion", "redirections", "fully_verified", "created"]

    def get_end_promotion(self, user_product):
        return user_product.product.get_end_promotion.strftime("%d.%m.%Y")

    def get_created(self, user_product):
        return user_product.created_at.strftime("%d.%m.%Y")
