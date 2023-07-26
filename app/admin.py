from django.contrib import admin
from .models import TranslationRequest

class TranslationRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'status')
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name')

admin.site.register(TranslationRequest, TranslationRequestAdmin)
