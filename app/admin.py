from django.contrib import admin
from .models import TranslationRequest

class TranslationRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'status')
    list_filter = ('status','last_name')
    search_fields = ('first_name', 'last_name')
    actions = ['mark_as_in_progress']

   


admin.site.register(TranslationRequest, TranslationRequestAdmin)
