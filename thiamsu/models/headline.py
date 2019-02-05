# third-party
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local
from thiamsu.models.song import Song


class Headline(models.Model):
    song = models.ForeignKey(Song, verbose_name=_("song"), on_delete=models.CASCADE)
    start_time = models.DateTimeField(_("headline_start_time"))
    end_time = models.DateTimeField(_("headline_end_time"))

    class Meta:
        verbose_name = _("headline")
        verbose_name_plural = _("headlines")
