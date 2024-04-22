from django.http import HttpResponse
from django.views.generic import View
from .models.texts import HeaderText, MainText, SubheaderText, ExplanationText
from .serializers import HeaderSerializer, SubheaderSerializer, MainTextSerializer, ExplanationTextSerializer
import json

    
class GetHeaderStyles(View):
    def get(self, request):
        header_styles = HeaderText.objects.first()
        return HttpResponse(json.dumps(HeaderSerializer(header_styles).data))
    
class GetMainTextStyles(View):
    def get(self, request):
        main_text_styles = MainText.objects.first()
        return HttpResponse(json.dumps(MainTextSerializer(main_text_styles).data))
    
class GetSubheaerStyles(View):
    def get(self, request):
        header_styles = SubheaderText.objects.first()
        return HttpResponse(json.dumps(SubheaderSerializer(header_styles).data))

class GetExplanationTextStyles(View):
    def get(self, request):
        explanation_text_styles = ExplanationText.objects.first()
        return HttpResponse(json.dumps(ExplanationTextSerializer(explanation_text_styles).data))
