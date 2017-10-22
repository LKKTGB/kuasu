from django.contrib import admin

from thiamsu.models.song import Song


class SongAdmin(admin.ModelAdmin):
    list_display = ('original_title', 'singer')


admin.site.register(Song, SongAdmin)
