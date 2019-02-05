from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def add_to_default_group(sender, **kwargs):
    # pylint: disable=unused-argument
    if kwargs["created"]:
        group = Group.objects.get(name="advance_user")
        user = kwargs["instance"]
        user.groups.add(group)
