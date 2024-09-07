from rest_framework import serializers

from catalog.serializers import ProductsSerializer
from user.models.idea import Idea, Like
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
        fields = [
            "id",
            "product",
            "comment",
            "connected",
            "gain",
            "end_promotion",
            "redirections",
            "fully_verified",
            "created",
        ]

    def get_end_promotion(self, user_product):
        return user_product.product.get_end_promotion.strftime("%d.%m.%Y")

    def get_created(self, user_product):
        return user_product.created_at.strftime("%d.%m.%Y")


class IdeasSerializer(serializers.ModelSerializer):
    finishe_date = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Idea
        fields = [
            "id",
            "category",
            "title",
            "description",
            "created_at",
            "status",
            "finishe_date",
            "user",
            "likes",
            "liked",
        ]

    def get_created_at(self, idea):
        return idea.created_at.strftime("%d.%m.%Y")

    def get_liked(self, idea):
        user = self.context["user"]
        if not user:
            return False

        return Like.objects.filter(idea=idea, user=user).exists()

    def get_user(self, idea):
        return idea.user.full_name

    def get_status(self, idea):
        return dict(idea.STATUSES).get(idea.status)

    def get_finishe_date(self, idea):
        if idea.finishe_date:
            return idea.finishe_date.strftime("%d.%m.%Y")

        return "---"

    def get_likes(self, idea):
        return idea.likes.count()
