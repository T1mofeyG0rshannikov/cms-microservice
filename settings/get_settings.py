from .models import Logo, Icon
from .serializers import SettingsSerializer


def get_settings():
    logo = Logo.objects.first()
    icon = Icon.objects.first()
        
    settings = {
        "logo": logo,
        "icon": icon
    }
    
    settings = SettingsSerializer(settings).data
    
    return settings