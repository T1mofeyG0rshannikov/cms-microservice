from rest_framework import serializers

from .models.texts import HeaderText, MainText, SubheaderText, ExplanationText
from .models.other_styles import IconSize, MarginBlock
from .models.colors import ColorStyles


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderText
        fields = ("font", "fontSize", "fontSizeMobile", "fontWeight", "fontWeightMobile", "color", "fontColorInverted")
        
class SubheaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubheaderText
        fields = ("font", "fontSize", "fontSizeMobile", "fontWeight", "fontWeightMobile", "color", "fontColorInverted")
        
class MainTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainText
        fields = ("font", "fontSize", "fontSizeMobile", "fontWeight", "fontWeightMobile", "color", "fontColorInverted")
        
class ExplanationTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExplanationText
        fields = ("font", "fontSize", "fontSizeMobile", "fontWeight", "fontWeightMobile", "color", "fontColorInverted")

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