from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from thiamsu.models.hanzi_hanlo_mapping import HanziHanloMapping
from thiamsu.models.translation import Translation


@receiver(post_save, sender=HanziHanloMapping)
def update_hanzi_hanlo_mapping_cache(sender, update_fields, instance, **kwargs):
    # pylint: disable=unused-argument
    HanziHanloMapping.dump(force=True)


@receiver(post_save, sender=Translation)
def update_song_progress(sender, update_fields, instance, **kwargs):
    # pylint: disable=unused-argument
    translation = instance

    translated_lines = (
        Translation.objects.filter(song=translation.song)
        .values("song", "lang")
        .annotate(count=models.Count("line_no", distinct=True))
    )
    translated_count = sum([t["count"] for t in translated_lines])
    total_count = len(
        [line for line in translation.song.original_lyrics.split("\n") if line.strip()]
    )
    total_count = total_count * (len(Translation.LANG_CHOICES) - 1)  # ignore hanlo

    translation.song.progress = int(translated_count / total_count * 100)
    translation.song.progress = min(100, max(0, translation.song.progress))
    translation.song.save()


@receiver(post_save, sender=Translation)
def update_user_contribution(sender, update_fields, instance, **kwargs):
    # pylint: disable=unused-argument
    translation = instance
    user = translation.contributor
    if user is None:
        return

    user.profile.contribution_of_songs = (
        Translation.objects.filter(contributor=user)
        .values("song")
        .annotate(count=models.Count("song"))
        .count()
    )
    user.profile.contribution_of_lines = (
        Translation.objects.filter(contributor=user)
        .values("song", "line_no")
        .annotate(count=models.Count("line_no"))
        .count()
    )
    user.profile.last_contribution_time = translation.created_at
    user.profile.save()
