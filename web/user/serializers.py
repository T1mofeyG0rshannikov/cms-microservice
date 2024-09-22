from rest_framework import serializers

from infrastructure.persistence.models.user.idea import Idea, Like
from infrastructure.persistence.models.user.product import UserOffer, UserProduct
from infrastructure.persistence.models.user.user import User
from web.catalog.serializers import ProductsSerializer
from web.common.serializers import DateFieldDot


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
    link = serializers.SerializerMethodField()

    class Meta:
        model = UserProduct
        fields = [
            "id",
            "product",
            "comment",
            "connected",
            "link",
            "gain",
            "end_promotion",
            "redirections",
            "fully_verified",
            "created_at",
        ]

    def get_link(self, user_product):
        user_offer = UserOffer.objects.filter(offer__product=user_product.product, user=user_product.user).first()
        if user_offer:
            return user_offer.link

        return ""

    def get_end_promotion(self, user_product):
        offer = user_product.product.offers.filter(partner_program="Пригласи друга").first()

        if offer:
            return offer.get_end_promotion.strftime("%d.%m.%Y")

        for offer in user_product.product.offers.all():
            if offer.end_promotion:
                return offer.get_end_promotion.strftime("%d.%m.%Y")

        return "Бессрочно"


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
