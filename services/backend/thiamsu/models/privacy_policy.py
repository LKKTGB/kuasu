from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from tinymce.models import HTMLField


class PrivacyPolicy(SingletonModel):
    title = models.CharField(_("privacy_policy_title"), max_length=100)
    body = HTMLField(_("privacy_policy_content"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("privacy_policy_verbose_name")
