# third-party
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _


class HanziHanloMapping(models.Model):
    hanzi = models.CharField(
        _("hanzi_hanlo_mapping_hanzi"), max_length=100, unique=True
    )
    hanlo = models.CharField(_("hanzi_hanlo_mapping_hanlo"), max_length=100)

    def __str__(self):
        return "%s -> %s" % (self.hanzi, self.hanlo)

    class Meta:
        verbose_name = _("hanzi_hanlo_mapping")
        verbose_name_plural = _("hanzi_hanlo_mappings")

    @classmethod
    def dump(cls, force=False):
        if force or "hanzi_hanlo_mapping" not in cache:
            mapping = {obj.hanzi: obj.hanlo for obj in cls.objects.all()}
            cache.set("hanzi_hanlo_mapping", mapping)
        return cache.get("hanzi_hanlo_mapping")
