from rest_framework import serializers

from domens.get_domain import get_domain_string


class EmailLogoSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField()
    width = serializers.CharField()
    height = serializers.CharField()

    def get_image(self, obj):
        return f"http://{get_domain_string()}" + obj.image.url
