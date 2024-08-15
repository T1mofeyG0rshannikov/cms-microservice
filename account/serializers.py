from datetime import datetime

from rest_framework import serializers

from user.models import User


class ReferralSerializer(serializers.ModelSerializer):
    referrals = serializers.CharField()
    first_level_referrals = serializers.CharField()
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
            "level",
            "redirections",
            "first_level_referrals",
        ]

    def get_redirections(self, referral):
        return 0

    def get_channel(self, referral):
        return ""

    def get_created_at(self, referral):
        return datetime.strftime(referral.created_at, "%d.%m.%Y")
