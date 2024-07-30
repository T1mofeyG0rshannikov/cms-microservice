from rest_framework import serializers


class LogoSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField()
    width = serializers.CharField()
    width_mobile = serializers.CharField(required=False)
    height_mobile = serializers.CharField(required=False)
    height = serializers.CharField()

    def get_image(self, obj):
        return obj.image.url


class SettingsSerializer(serializers.Serializer):
    logo = serializers.SerializerMethodField()
    form_logo = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return LogoSerializer(obj.logo).data

    def get_form_logo(self, obj):
        return LogoSerializer(obj.form_logo).data

    def get_icon(self, obj):
        return obj.icon.image.url
