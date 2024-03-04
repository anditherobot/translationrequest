from django.contrib import admin
from .models import TranslationRequest, ClientInfo, ClientFile

from .models import Scene, SceneImage, UserProfile, SceneRating

class TranslationRequestAdmin(admin.ModelAdmin):
    list_display = ['client', 'source_language', 'target_language', 'request_date', 'status']
    list_filter = ['source_language', 'target_language', 'status']
    search_fields = ['client__first_name', 'client__last_name', 'content'] 

    
class RatingInline(admin.TabularInline):
    model = SceneRating
    extra = 1
  
class SceneImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'scene', 'image_file')
    inlines = [RatingInline]

class SceneRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'scene_image', 'rating', 'created_at', 'updated_at')


admin.site.register(TranslationRequest, TranslationRequestAdmin)
admin.site.register(ClientInfo)
admin.site.register(ClientFile)


#Scenes
admin.site.register(Scene)
admin.site.register(SceneImage, SceneImageAdmin)
admin.site.register(UserProfile)
admin.site.register(SceneRating, SceneRatingAdmin)