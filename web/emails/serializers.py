from rest_framework import serializers

from infrastructure.persistence.repositories.domain_repository import (
    get_domain_repository,
)


class EmailLogoSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField()
    width = serializers.CharField()
    height = serializers.CharField()

    def get_image(self, obj, domain_repository=get_domain_repository()):
        return f"https://{domain_repository.get_domain_string()}" + obj.image.url
