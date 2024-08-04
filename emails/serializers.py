from rest_framework import serializers

from domens.domain_service.domain_service import DomainService


class EmailLogoSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField()
    width = serializers.CharField()
    height = serializers.CharField()

    def get_image(self, obj):
        return f"http://{DomainService.get_domain_string()}" + obj.image.url
