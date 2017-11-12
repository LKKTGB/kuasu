# third-party
from django.contrib.auth.models import User
from django.db import models

# local
from thiamsu.models.song import Song


class Translation(models.Model):
    LANG_CHOICES = (
        ('tailo', '全羅'),
        ('hanzi', '全漢'),
    )

    song = models.ForeignKey(Song)
    line_no = models.PositiveSmallIntegerField()
    lang = models.CharField(
        max_length=5,
        choices=LANG_CHOICES)
    content = models.CharField(max_length=1000)
    contributor = models.ForeignKey(User, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
