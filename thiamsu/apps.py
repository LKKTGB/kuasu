from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ThiamsuConfig(AppConfig):
    name = "thiamsu"
    verbose_name = _("app_thiamsu")

    def ready(self):
        # pylint: disable=unused-import
        from thiamsu import signals
