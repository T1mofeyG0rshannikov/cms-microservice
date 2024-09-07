from rest_framework import serializers

from domens.domain_service.domain_service import get_domain_service


class EmailLogoSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField()
    width = serializers.CharField()
    height = serializers.CharField()

    def get_image(self, obj):
        domain_service = get_domain_service()
        return f"http://{domain_service.get_domain_string()}" + obj.image.url
