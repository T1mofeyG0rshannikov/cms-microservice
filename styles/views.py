import json

from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from .models.common import GlobalStyles
from .models.font import Font
from .serializers import (
    ColorsSerializer,
    ExplanationTextSerializer,
    FontSerializer,
    HeaderSerializer,
    IconSizeSerializer,
    MainTextSerializer,
    MarginBlockSerializer,
    SubheaderSerializer,
)


class GetColorStyles(View):
    def get(self, request):
        color_styles = GlobalStyles.objects.first().colorstyles_set.first()
        return JsonResponse(ColorsSerializer(color_styles).data)


class GetHeaderStyles(View):
    def get(self, request):
        header_styles = GlobalStyles.objects.first().headertext_set.first()
        return JsonResponse(HeaderSerializer(header_styles).data)


class GetMainTextStyles(View):
    def get(self, request):
        main_text_styles = GlobalStyles.objects.first().maintext_set.first()
        return JsonResponse(MainTextSerializer(main_text_styles).data)


class GetSubheaerStyles(View):
    def get(self, request):
        header_styles = GlobalStyles.objects.first().subheadertext_set.first()
        return JsonResponse(SubheaderSerializer(header_styles).data)


class GetExplanationTextStyles(View):
    def get(self, request):
        explanation_text_styles = GlobalStyles.objects.first().explanationtext_set.first()
        return JsonResponse(ExplanationTextSerializer(explanation_text_styles).data)


class GetMarginBlock(View):
    def get(self, request):
        margins = GlobalStyles.objects.first().marginblock_set.first()
        return JsonResponse(MarginBlockSerializer(margins).data)


class GetIconSize(View):
    def get(self, request):
        icon_size = GlobalStyles.objects.first().iconsize_set.first()
        return JsonResponse(IconSizeSerializer(icon_size).data)


class GetFonts(View):
    def get(self, request):
        fonts = Font.objects.all()
        return HttpResponse(json.dumps(FontSerializer(fonts, many=True).data))
