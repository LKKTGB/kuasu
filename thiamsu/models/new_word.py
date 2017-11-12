# third-party
from django.db import models

# local
from thiamsu.models.song import Song


class NewWord(models.Model):
    song = models.ForeignKey(Song)
    content = models.CharField(max_length=100, help_text='生難詞')
    reference_url = models.CharField(max_length=100, help_text='參考網址')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('song', 'content', 'reference_url')
