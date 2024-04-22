from django.http import HttpResponse
from django.views.generic import View
from .models.colors import BackgroundColor, MainColor, SecondaryColor
import json


class GetBackgroundColor(View):
    def get(self, request):
        color = BackgroundColor.objects.first()
        return HttpResponse(json.dumps(color.color))
    
class GetMainColor(View):
    def get(self, request):
        color = MainColor.objects.first()
        return HttpResponse(json.dumps(color.color))
    
class GetSecondaryColor(View):
    def get(self, request):
        color = SecondaryColor.objects.first()
        return HttpResponse(json.dumps(color.color))
