from rest_framework import serializers

from domain.page_blocks.base_block import PageBlockInterface
from infrastructure.persistence.models.blocks.common import Page
from web.styles.serializers import CustomStylesSerializer


class BlockSerializer(serializers.Serializer):
    styles = CustomStylesSerializer()
    content = serializers.SerializerMethodField()

    def get_content(self, block: PageBlockInterface):
        return block.content


class PageSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True)

    class Meta:
        model = Page
        fields = ("title", "blocks")
