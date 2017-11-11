from django.contrib import admin

from thiamsu.forms import SongAdminForm
from thiamsu.models.approved_translation import ApprovedTranslation
from thiamsu.models.song import Song
from thiamsu.models.translation import Translation


class SongAdmin(admin.ModelAdmin):
    list_display = ('original_title', 'performer')
    form = SongAdminForm


class TranslationAdmin(admin.ModelAdmin):
    pass


class ApprovedTranslationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Song, SongAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(ApprovedTranslation, ApprovedTranslationAdmin)
