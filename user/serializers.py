from rest_framework import serializers

from catalog.serializers import ProductsSerializer
from common.serializers import DateFieldDot
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
    created_at = DateFieldDot()

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
            "created_at",
        ]

    def get_end_promotion(self, user_product):
        return user_product.product.get_end_promotion.strftime("%d.%m.%Y")


class IdeasSerializer(serializers.ModelSerializer):
    finishe_date = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    created_at = DateFieldDot()
    user_icon = serializers.SerializerMethodField()

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
            "user_id",
            "likes_count",
            "admin_answer",
            "liked",
            "user_icon",
        ]

    def get_user_icon(self, idea):
        if idea.user.profile_picture:
            return idea.user.profile_picture.url

        return None

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

    def get_likes_count(self, idea):
        return idea.likes_count
