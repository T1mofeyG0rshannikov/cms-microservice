from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from blocks.get_block import get_block
from blocks.models.common import Page, Template
from styles.serializers import CustomStylesSerializer


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
        try:
            return CustomStylesSerializer(self.get_content(block).styles).data
        except ObjectDoesNotExist:
            return None


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ("name", "file")
