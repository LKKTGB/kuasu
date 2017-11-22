# third-party
from django.db import models

# local
from thiamsu.models.song import Song


class Headline(models.Model):
    song = models.ForeignKey(Song)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
