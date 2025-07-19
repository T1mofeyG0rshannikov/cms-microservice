import json

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from infrastructure.persistence.models.settings import Font, UserFont
from infrastructure.persistence.models.styles.colors.colors import ColorStyles
from infrastructure.persistence.models.styles.other import IconSize, MarginBlock
from infrastructure.persistence.models.styles.texts.texts import (
    ExplanationText,
    HeaderText,
    MainText,
    SubheaderText,
)

from .serializers import (
    ColorsSerializer,
    FontSerializer,
    IconSizeSerializer,
    MarginBlockSerializer,
    TextSerializer,
)


class GetColorStyles(View):
    def get(self, request):
        color_styles = ColorStyles.objects.first()
        return JsonResponse(ColorsSerializer(color_styles).data)


class GetHeaderStyles(View):
    def get(self, request):
        header_styles = HeaderText.objects.first()
        return JsonResponse(TextSerializer(header_styles).data)


class GetMainTextStyles(View):
    def get(self, request):
        main_text_styles = MainText.objects.first()
        return JsonResponse(TextSerializer(main_text_styles).data)


class GetSubheaerStyles(View):
    def get(self, request):
        header_styles = SubheaderText.objects.first()
        return JsonResponse(TextSerializer(header_styles).data)


class GetExplanationTextStyles(View):
    def get(self, request):
        explanation_text_styles = ExplanationText.objects.first()
        return JsonResponse(TextSerializer(explanation_text_styles).data)


class GetMarginBlock(View):
    def get(self, request):
        margins = MarginBlock.objects.first()
        return JsonResponse(MarginBlockSerializer(margins).data)


class GetIconSize(View):
    def get(self, request):
        icon_size = IconSize.objects.first()
        return JsonResponse(IconSizeSerializer(icon_size).data)


class GetFonts(View):
    def get(self, request):
        fonts = Font.objects.exclude(link=None)
        user_fonts = UserFont.objects.exclude(link=None)

        all_fonts = [*fonts, *user_fonts]
        return HttpResponse(json.dumps(FontSerializer(all_fonts, many=True).data))


class GetStyles(View):
    def get(self, request):
        all_fonts = cache.get("fonts")
        if not all_fonts:
            fonts = Font.objects.exclude(link=None).values_list("link", flat=True)
            user_fonts = UserFont.objects.exclude(link=None).values_list("link", flat=True)
            all_fonts = [*fonts, *user_fonts]
            cache.set("fonts", all_fonts, timeout=60 * 15)

        margins = cache.get("margins")
        if not margins:
            margins = MarginBlock.objects.first()
            cache.set("margins", margins, timeout=60 * 15)

        color_styles = cache.get("color_styles")
        if not color_styles:
            color_styles = ColorStyles.objects.first()
            cache.set("color_styles", color_styles, timeout=60 * 15)

        header_styles = cache.get("header_styles")
        if not header_styles:
            header_styles = HeaderText.objects.select_related("font").first()
            cache.set("header_styles", header_styles, timeout=60 * 15)

        main_text_styles = cache.get("main_text_styles")
        if not main_text_styles:
            main_text_styles = MainText.objects.select_related("font").first()
            cache.set("main_text_styles", main_text_styles, timeout=60 * 15)

        explanation_text_styles = cache.get("explanation_text_styles")
        if not explanation_text_styles:
            explanation_text_styles = ExplanationText.objects.select_related("font").first()
            cache.set("explanation_text_styles", explanation_text_styles, timeout=60 * 15)

        icon_size = cache.get("icon_size")
        if not icon_size:
            icon_size = IconSize.objects.first()
            cache.set("icon_size", icon_size, timeout=60 * 15)

        return JsonResponse(
            {
                "fonts": all_fonts,
                "margin": MarginBlockSerializer(margins).data,
                "colors": ColorsSerializer(color_styles).data,
                "header": TextSerializer(header_styles).data,
                "maintext": TextSerializer(main_text_styles).data,
                "subheader": TextSerializer(header_styles).data,
                "explanationtext": TextSerializer(explanation_text_styles).data,
                "iconsize": IconSizeSerializer(icon_size).data,
            }
        )
