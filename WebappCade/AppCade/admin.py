from django.contrib import admin
from .models import Document, CadeModel, CadeModelManager

# Register your models here.
admin.site.register(Document)
admin.site.register(CadeModel)
admin.site.register(CadeModelManager)
