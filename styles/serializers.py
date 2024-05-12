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
    margin_top = serializers.CharField()
    margin_bottom = serializers.CharField()

    background_color = serializers.CharField()
    photo_darkness = serializers.SerializerMethodField()

    header_size = serializers.CharField()
    header_size_mobile = serializers.CharField()
    header_thickness = serializers.CharField()
    header_thickness_mobile = serializers.CharField()
    header_color = serializers.CharField()

    subheader_size = serializers.CharField(required=False)
    subheader_size_mobile = serializers.CharField(required=False)
    subheader_thickness = serializers.CharField(required=False)
    subheader_thickness_mobile = serializers.CharField(required=False)
    subheader_color = serializers.CharField(required=False)

    main_text_size = serializers.CharField()
    main_text_size_mobile = serializers.CharField()
    main_text_thickness = serializers.CharField()
    main_text_thickness_mobile = serializers.CharField()
    main_text_color = serializers.CharField()

    explanation_text_size = serializers.CharField(required=False)
    explanation_text_size_mobile = serializers.CharField(required=False)
    explanation_text_thickness = serializers.CharField(required=False)
    explanation_text_thickness_mobile = serializers.CharField(required=False)
    explanation_text_color = serializers.CharField(required=False)

    columns = serializers.SerializerMethodField(required=False)
    icon_color = serializers.CharField(required=False)
    icon_background_color = serializers.CharField(required=False)

    background_image_darkness = serializers.SerializerMethodField(required=False)

    icon_width = serializers.CharField(required=False)
    icon_height = serializers.CharField(required=False)

    border_radius = serializers.CharField(required=False)

    button_color = serializers.CharField(required=False)

    def get_columns(self, obj):
        try:
            return " ".join(["1fr" for i in range(obj.columns)])
        except AttributeError:
            return None

    def get_background_image_darkness(self, obj):
        if obj.photo_darkness is None:
            return None

        return obj.photo_darkness / 100

    def get_photo_darkness(self, obj):
        photo_darkness = obj.photo_darkness
        if photo_darkness is not None:
            photo_darkness = 100 - photo_darkness

        return photo_darkness
