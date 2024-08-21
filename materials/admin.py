from django.contrib import admin

from account.admin import DocumentAdmin
from materials.models import Document

admin.site.register(Document, DocumentAdmin)
