from django.contrib import admin
from .models import TranslationRequest, InProgressRequest

class TranslationRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'status')
    list_filter = ('status','last_name')
    search_fields = ('first_name', 'last_name')
    actions = ['mark_as_in_progress']

    def mark_as_in_progress(self, request, queryset):
        for translation_request in queryset:
            in_progress_request = InProgressRequest.objects.create(request=translation_request)
            translation_request.status = TranslationRequest.IN_PROGRESS
            translation_request.save()

    mark_as_in_progress.short_description = 'Move selected requests to In Progress'

admin.site.register(TranslationRequest, TranslationRequestAdmin)
