from rest_framework import serializers

from .models.colors.colors import ColorStyles
from .models.other import IconSize, MarginBlock
from .models.texts.font import Font


class FontSerializer(serializers.ModelSerializer):
    link = serializers.CharField(required=False)

    class Meta:
        model = Font
        fields = ("name", "link")


class TextSerializer(serializers.Serializer):
    font = FontSerializer()
    fontSize = serializers.CharField()
    fontSizeMobile = serializers.CharField()
    fontWeight = serializers.CharField()
    fontWeightMobile = serializers.CharField()
    color = serializers.CharField()
    fontColorInverted = serializers.CharField()


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorStyles
        fields = ("background_color", "main_color", "secondary_color", "second_background_color")


class IconSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IconSize
        fields = ("width", "height")


class MarginBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarginBlock
        fields = ("margin_top", "margin_bottom")


class CustomStylesSerializer(serializers.Serializer):
    background_color = serializers.CharField()
    photo_darkness = serializers.SerializerMethodField()

    header_size = serializers.CharField()
    header_size_mobile = serializers.CharField()
    header_thickness = serializers.CharField()
    header_thickness_mobile = serializers.CharField()
    header_color = serializers.CharField()

    main_text_size = serializers.CharField()
    main_text_size_mobile = serializers.CharField()
    main_text_thickness = serializers.CharField()
    main_text_thickness_mobile = serializers.CharField()
    main_text_color = serializers.CharField()

    columns = serializers.CharField(required=False)

    def get_photo_darkness(self, obj):
        photo_darkness = obj.photo_darkness
        if photo_darkness is not None:
            photo_darkness = 100 - photo_darkness

        return photo_darkness
