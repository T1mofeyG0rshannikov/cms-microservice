from django.contrib import admin
from django.contrib.admin.decorators import register
from .models.colors import BackgroundColor, BackgroundColorSecond, MainColor, SecondaryColor


class ColorAdmin(admin.ModelAdmin):
    list_display = ["color"]
    
@register(BackgroundColor)
class BackgroundColorAdmin(ColorAdmin):
    pass

@register(BackgroundColorSecond)
class BackgroundColorSecondAdmin(ColorAdmin):
    pass

@register(MainColor)
class MainColorAdmin(ColorAdmin):
    pass

@register(SecondaryColor)
class SecondaryColorAdmin(ColorAdmin):
    pass
