from rest_framework import serializers

from .get_block import get_block
from .models import Page, Template


class PageSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ("title", "blocks")

    def get_blocks(self, page):
        blocks = list(filter(lambda c: c is not None, [get_block(block.name) for block in page.blocks.all()]))

        for block in blocks:
            block.template.file = "cms/" + block.template.file

        return blocks


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ("name", "file")
