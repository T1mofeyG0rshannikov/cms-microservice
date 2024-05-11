from django.views.generic import View
from django.http import JsonResponse
from .models import Logo
from .serializers import SettingsSerializer


class GetSettings(View):
    def get(self, request):
        logo = Logo.objects.first()
        
        settings = SettingsSerializer(
            logo=logo
        ).data
        
        return JsonResponse(settings)