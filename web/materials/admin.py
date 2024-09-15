from account.admin import DocumentAdmin
from django.contrib import admin
from materials.models import Document

admin.site.register(Document, DocumentAdmin)
