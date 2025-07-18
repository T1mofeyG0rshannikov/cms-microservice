from rest_framework import serializers

from infrastructure.persistence.models.blocks.common import Page
from web.styles.serializers import CustomStylesSerializer
from dataclasses import asdict

class BlockSerializer(serializers.Serializer):
    styles = CustomStylesSerializer(required=False)
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        try:
            return asdict(obj.content)
        except:
            return obj.content

class PageSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True)

    class Meta:
        model = Page
        fields = ("title", "blocks")
