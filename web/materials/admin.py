from django.contrib import admin

from infrastructure.persistence.models.materials import Document
from web.account.admin import DocumentAdmin

admin.site.register(Document, DocumentAdmin)
