from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from thiamsu.models.song import Song


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.CharField(max_length=100, blank=True)
    favorite_songs = models.ManyToManyField(Song, related_name='+')

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return self.user.last_name + self.user.first_name

    def avatar(self):
        return '<img src="%s" />' % self.avatar_url
    avatar.short_description = _('avatar')
    avatar.allow_tags = True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
