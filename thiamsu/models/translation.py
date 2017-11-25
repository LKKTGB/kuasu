# third-party
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local
from thiamsu.models.song import Song


class Translation(models.Model):
    LANG_CHOICES = (
        ('tailo', _('translation_lang_tailo')),
        ('hanzi', _('translation_lang_hanzi')),
    )

    song = models.ForeignKey(Song, verbose_name=_('song'))
    line_no = models.PositiveSmallIntegerField(_('translation_line_no'))
    lang = models.CharField(
        _('translation_lang'),
        max_length=5,
        choices=LANG_CHOICES)
    content = models.CharField(_('translation_content'), max_length=1000)
    contributor = models.ForeignKey(User, blank=True, null=True,
                                    verbose_name=_('translation_contributor'))

    created_at = models.DateTimeField(_('translation_created_at'), auto_now_add=True)

    class Meta:
        verbose_name = _('translation')
        verbose_name_plural = _('translations')
