from rest_framework import serializers

from infrastructure.persistence.models.blocks.common import Page
from web.styles.serializers import CustomStylesSerializer


class BlockSerializer(serializers.Serializer):
    styles = CustomStylesSerializer(required=False)
    content = serializers.JSONField()


class PageSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True)

    class Meta:
        model = Page
        fields = ("title", "blocks")
