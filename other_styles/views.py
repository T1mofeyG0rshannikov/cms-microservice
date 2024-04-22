from django.http import HttpResponse
from django.views.generic import View
from .models import MarginBlock, IconSize
import json


class GetMarginBlock(View):
    def get(self, request):
        margins = MarginBlock.objects.first()
        return HttpResponse(json.dumps({"top": margins.margin_top, "bottom": margins.margin_bottom}))

class GetIconSize(View):
    def get(self, request):
        icon_size = IconSize.objects.first()
        return HttpResponse(json.dumps({"height": icon_size.height, "width": icon_size.width}))