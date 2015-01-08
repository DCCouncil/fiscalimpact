from django.contrib import admin
from app.models import Document
import reversion

@admin.register(Document)
class DocumentAdmin(reversion.VersionAdmin):
    pass
