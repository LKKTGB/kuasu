# third-party
from django.db import models
from django.utils.translation import ugettext_lazy as _


class HanziHanloMapping(models.Model):
    hanzi = models.CharField(_('hanzi_hanlo_mapping_hanzi'), max_length=100, unique=True)
    hanlo = models.CharField(_('hanzi_hanlo_mapping_hanlo'), max_length=100)

    def __str__(self):
        return '%s -> %s' % (self.hanzi, self.hanlo)

    class Meta:
        verbose_name = _('hanzi_hanlo_mapping')
        verbose_name_plural = _('hanzi_hanlo_mappings')
