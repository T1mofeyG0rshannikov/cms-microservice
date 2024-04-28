from rest_framework import serializers

from .get_block import get_block
from .get_custom_styles import get_custom_styles
from .models.common import Page, Template


class PageSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ("title", "blocks")

    def get_blocks(self, page):
        blocks = list(filter(lambda c: c is not None, [get_block(block.name) for block in page.blocks.all()]))

        for block in blocks:
            block.template.file = "blocks/" + block.template.file

        for i in range(len(blocks)):
            styles = get_custom_styles(blocks[i]).__dict__

            if styles["photo_darkness"] is not None:
                styles["photo_darkness"] = 100 - styles["photo_darkness"]

            blocks[i] = {"content": blocks[i], "styles": styles}

        return blocks


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ("name", "file")
