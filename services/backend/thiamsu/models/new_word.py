# third-party
from django.db import models
from django.utils.translation import gettext_lazy as _

# local
from thiamsu.models.song import Song


class NewWord(models.Model):
    song = models.ForeignKey(Song, verbose_name=_("song"), on_delete=models.CASCADE)
    content = models.CharField(_("new_word_content"), max_length=100)
    reference_url = models.CharField(_("new_word_reference_url"), max_length=1000)

    created_at = models.DateTimeField(_("new_word_created_at"), auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("new_word")
        verbose_name_plural = _("new_words")

        unique_together = ("song", "content", "reference_url")
