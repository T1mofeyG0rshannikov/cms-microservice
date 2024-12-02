from django.contrib import admin

from infrastructure.persistence.models.materials import Document, DocumentFormatPattern
from web.common.admin import BaseInline


class DocumentFormatterPatternAdmin(BaseInline):
    model = DocumentFormatPattern


class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [DocumentFormatterPatternAdmin]
    
    def get_fieldsets(self, request, obj):
        fieldsets = (
            (
                None,
                {
                    "fields": (
                        "image",
                        "title",
                        "text",
                        "name",
                        "slug"   
                    ),
                    "description": """
                        Доступны следующие подстановочные шаблоны:<br>
                        [SITENAME] - название сайта<br>
                        [SITEADRESS] - url адресс сайта<br>
                        [SITECREATED] - дата создания сайта<br>
                        [SITEOWNER] - владелец сайта<br>
                        [SITECONTACTINFO] - контактная информация<br>
                    """,
                },
            ),
        )
        return fieldsets


admin.site.register(Document, DocumentAdmin)
