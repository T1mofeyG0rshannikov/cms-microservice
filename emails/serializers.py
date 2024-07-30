from rest_framework import serializers

from domens.models import Domain


class EmailLogoSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField()
    width = serializers.CharField()
    height = serializers.CharField()

    def get_image(self, obj):
        return f"http://{Domain.objects.values_list('domain').filter(is_partners=False).first()[0]}" + obj.image.url
