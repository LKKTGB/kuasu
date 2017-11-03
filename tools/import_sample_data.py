#!/usr/bin/env python

# built-in
import os
import sys

# third-party
import django
import dotenv

# setup Django
sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
dotenv.read_dotenv()
django.setup()

# local
from thiamsu.models.song import Song
import sample_data


def import_sample_data():
    for song in sample_data.songs:
        Song.objects.create(
            original_title=song['original_title'],
            hanzi_title=song['original_title'],
            tailo_title=song['tailo_title'],
            hanlo_title=song['tailo_title'],
            singer=song['singer'],
            youtube_url=song['youtube_url'],
            original_lyrics='\n'.join(
                [lyric['original'] for lyric in sample_data.lyrics])
        )


if __name__ == '__main__':
    import_sample_data()
