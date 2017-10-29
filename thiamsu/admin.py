from django.contrib import admin

from thiamsu.models.song import Song
from thiamsu.models.translation import Translation


class SongAdmin(admin.ModelAdmin):
    list_display = ('original_title', 'singer')


class TranslationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Song, SongAdmin)
admin.site.register(Translation, TranslationAdmin)
