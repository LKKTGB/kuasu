from django.db import models


class Song(models.Model):
    original_title = models.CharField(max_length=100, help_text='原文歌名')
    hanzi_title = models.CharField(max_length=100, help_text='全漢歌名')
    tailo_title = models.CharField(max_length=100, help_text='全羅歌名')
    hanlo_title = models.CharField(max_length=100, help_text='漢羅歌名')
    singer = models.CharField(max_length=100, help_text='演唱人')
    youtube_url = models.CharField(max_length=100, help_text='Youtube 網址')
