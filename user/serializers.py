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

    class Meta:
        model = UserProduct
        fields = ["product", "connected", "gain", "end_promotion", "redirections", "fully_verified"]

    def get_end_promotion(self, user_product):
        return user_product.product.get_end_promotion.strftime("%d.%m.%Y")
