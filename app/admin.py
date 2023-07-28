from django.contrib import admin
from .models import TranslationRequest

class TranslationRequestAdmin(admin.ModelAdmin):
    list_display = ['client', 'source_language', 'target_language', 'request_date', 'status']
    list_filter = ['source_language', 'target_language', 'status']
    search_fields = ['client__first_name', 'client__last_name', 'content'] 
   


admin.site.register(TranslationRequest, TranslationRequestAdmin)
