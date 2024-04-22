from rest_framework import serializers

from .models.texts import HeaderText, MainText, SubheaderText, ExplanationText


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
