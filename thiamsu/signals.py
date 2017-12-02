from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from thiamsu.models.translation import Translation


@receiver(post_save, sender=Translation)
def update_song_progress(sender, update_fields, instance, **kwargs):
    translation = instance

    translated_lines = (
        Translation.objects
        .filter(song=translation.song)
        .values('song', 'lang')
        .annotate(count=models.Count('line_no', distinct=True))
    )
    translated_count = sum([t['count'] for t in translated_lines])
    total_count = len([line for line in translation.song.original_lyrics.split('\n') if line.strip()])
    total_count = total_count * len(translated_lines)

    translation.song.progress = int(translated_count / total_count * 100)
    translation.song.save()
