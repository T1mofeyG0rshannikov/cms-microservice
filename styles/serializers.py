from rest_framework import serializers

from .models.colors import ColorStyles
from .models.common import Font
from .models.other_styles import IconSize, MarginBlock
from .models.texts import ExplanationText, HeaderText, MainText, SubheaderText


class FontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Font
        fields = ("name", "link")


class HeaderSerializer(serializers.ModelSerializer):
    font = serializers.SerializerMethodField()

    class Meta:
        model = HeaderText
        fields = ("font", "fontSize", "fontSizeMobile", "fontWeight", "fontWeightMobile", "color", "fontColorInverted")

    def get_font(self, header_serializer):
        return FontSerializer(header_serializer.font).data


class SubheaderSerializer(serializers.ModelSerializer):
    font = serializers.SerializerMethodField()

    class Meta:
        model = SubheaderText
        fields = ("font", "fontSize", "fontSizeMobile", "fontWeight", "fontWeightMobile", "color", "fontColorInverted")

    def get_font(self, header_serializer):
        return FontSerializer(header_serializer.font).data


class MainTextSerializer(serializers.ModelSerializer):
    font = serializers.SerializerMethodField()

    class Meta:
        model = MainText
        fields = ("font", "fontSize", "fontSizeMobile", "fontWeight", "fontWeightMobile", "color", "fontColorInverted")

    def get_font(self, header_serializer):
        return FontSerializer(header_serializer.font).data


class ExplanationTextSerializer(serializers.ModelSerializer):
    font = serializers.SerializerMethodField()

    class Meta:
        model = ExplanationText
        fields = ("font", "fontSize", "fontSizeMobile", "fontWeight", "fontWeightMobile", "color", "fontColorInverted")

    def get_font(self, header_serializer):
        return FontSerializer(header_serializer.font).data


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorStyles
        fields = ("background_color", "main_color", "secondary_color")


class IconSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IconSize
        fields = ("width", "height")


class MarginBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarginBlock
        fields = ("margin_top", "margin_bottom")
