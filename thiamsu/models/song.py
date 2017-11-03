from django.db import models

from thiamsu.utils import get_youtube_id_from_url


class Song(models.Model):
    original_title = models.CharField(max_length=100, help_text='原文歌名')
    hanzi_title = models.CharField(max_length=100, help_text='全漢歌名')
    tailo_title = models.CharField(max_length=100, help_text='全羅歌名')
    hanlo_title = models.CharField(max_length=100, help_text='漢羅歌名')
    singer = models.CharField(max_length=100, help_text='演唱人')
    youtube_url = models.CharField(max_length=100, help_text='Youtube 網址')
    original_lyrics = models.TextField(default='', help_text='原文歌詞')

    @property
    def youtube_id(self):
        return get_youtube_id_from_url(self.youtube_url)

    @property
    def cover_url(self):
        return 'https://img.youtube.com/vi/{id}/hqdefault.jpg'.format(
            id=self.youtube_id
        )
