from django.contrib import admin

from web.account.admin import DocumentAdmin
from web.materials.models import Document

admin.site.register(Document, DocumentAdmin)
