# third-party
from django.contrib.auth.models import User
from django.db import models

# local
from meta.models.song import Song
from meta.models.translation import Translation


class ApprovedTranslation(models.Model):
    song = models.ForeignKey(Song)
    line_no = models.PositiveSmallIntegerField()
    lang = models.CharField(
        max_length=2,
        choices=Translation.LANG_CHOICES)
    translation = models.ForeignKey(Translation)
    reviewer = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('song', 'line_no', 'lang')
