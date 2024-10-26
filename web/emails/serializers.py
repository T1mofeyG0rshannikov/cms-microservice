from rest_framework import serializers

from application.services.domains.service import get_domain_service


class EmailLogoSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField()
    width = serializers.CharField()
    height = serializers.CharField()

    def get_image(self, obj, domain_service=get_domain_service()):
        return f"https://{domain_service.get_domain_string()}" + obj.image.url
