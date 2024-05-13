from rest_framework import serializers

from .models import Logo


class LogoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Logo
        fields = ("image", "width", "height", "width_mobile", "height_mobile")

    def get_image(self, obj):
        return obj.image.url


class SettingsSerializer(serializers.Serializer):
    logo = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return LogoSerializer(obj.logo).data

    def get_icon(self, obj):
        return obj.icon.image.url
