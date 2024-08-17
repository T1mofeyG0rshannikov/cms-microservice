from datetime import datetime

from django.db.models import Q
from rest_framework import serializers

from user.models import User
from utils.date_russian import get_date_in_russian


def get_referrals_count(level, referral) -> int:
    count = 0
    for i in range(level):
        field = "sponsor__" * i + "sponsor_id"
        count += User.objects.filter(Q(**{field: referral.id})).count()

    return count


class ReferralsSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()
    first_level_referrals = serializers.SerializerMethodField()
    channel = serializers.SerializerMethodField()
    level = serializers.IntegerField()
    redirections = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "second_name",
            "created_at",
            "profile_picture",
            "referrals",
            "channel",
            "full_name",
            "level",
            "redirections",
            "sponsor",
            "first_level_referrals",
        ]

    def get_first_level_referrals(self, referral):
        return get_referrals_count(1, referral)

    def get_referrals(self, referral):
        first_level_referrals = get_referrals_count(1, referral)

        all_referrals = first_level_referrals + get_referrals_count(2, referral) + get_referrals_count(3, referral)

        return f"{first_level_referrals}({all_referrals})"

    def get_redirections(self, referral):
        return 0

    def get_channel(self, referral):
        return "Телеграм"

    def get_created_at(self, referral):
        return datetime.strftime(referral.created_at, "%d.%m.%Y")


class ReferralSerializer(serializers.ModelSerializer):
    site_created = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()
    sponsor = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "full_name",
            "level",
            "site_created",
            "links",
            "active",
            "activities",
            "last_login",
            "sponsor",
            "created_at",
            "sponsor_id",
        ]

    def get_created_at(self, referral):
        return get_date_in_russian(referral.created_at)

    def get_sponsor(self, referral):
        if referral.level == 1:
            return "Телеграм"

        return referral.sponsor.full_name

    def get_level(self, referral):
        return f"Уровень {referral.level}"

    def get_last_login(self, referral):
        if referral.last_login:
            return get_date_in_russian(referral.last_login)

        return None

    def get_links(self, referral):
        return "9 (31)"

    def get_active(self, referral):
        return "Умеренная (5/10)"

    def get_activities(self, referral):
        return [{"date": "12.02.24", "content": "Зарегистрировался"}]

    def get_site_created(self, referral):
        if hasattr(referral, "site"):
            date = referral.site.created_at
            if date:
                return get_date_in_russian(date)

        return None
