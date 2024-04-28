from rest_framework import serializers

from styles.serializers import CustomStylesSerializer

from .get_block import get_block
from .get_custom_styles import get_custom_styles
from .models.common import Page, Template


class PageSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ("title", "blocks")

    def get_blocks(self, page):
        return BlockSerializer(page.blocks.all(), many=True).data


class BlockSerializer(serializers.Serializer):
    content = serializers.SerializerMethodField()
    styles = serializers.SerializerMethodField()

    def get_content(self, block):
        content = get_block(block.name)

        if content is not None:
            content.template.file = "blocks/" + content.template.file

        return content

    def get_styles(self, block):
        return CustomStylesSerializer(get_custom_styles(self.get_content(block))).data


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ("name", "file")
