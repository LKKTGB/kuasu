from django.core.management.base import BaseCommand
from django.db import models

from thiamsu.models.translation import Translation


class Command(BaseCommand):
    help = "Load ptt data from csv file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-id", default=None, help="Target user to switch translations"
        )
        parser.add_argument(
            "--song-id", default=None, help="Target song to switch translations"
        )
        parser.add_argument("--dryrun", action="store_true")

    def get_latest_translations(self, lang, user_id=None, song_id=None):
        """
        Return map {(song_id, line_no): latest_translation} of given contributor and language
        """
        q_statement = models.Q(lang__exact=lang)
        if user_id:
            q_statement &= models.Q(contributor__exact=user_id)
        if song_id:
            q_statement &= models.Q(song__exact=song_id)

        translations = Translation.objects.filter(q_statement).all()

        latest_translations = {}
        for t in translations:
            k = (t.song.id, t.line_no)
            curr = latest_translations.get(k)
            if not curr or curr.created_at < t.created_at:
                latest_translations[k] = t
        return latest_translations

    def handle(self, *args, **options):
        hanzi_translations = self.get_latest_translations(
            lang="hanzi", user_id=options["user_id"], song_id=options["song_id"]
        )
        tailo_translations = self.get_latest_translations(
            lang="tailo", user_id=options["user_id"], song_id=options["song_id"]
        )

        for song_id, line_no in sorted(hanzi_translations.keys()):
            k = (song_id, line_no)
            song = hanzi_translations[k].song
            contributor = hanzi_translations[k].contributor
            if k not in tailo_translations:
                continue
            if options["dryrun"]:
                print(
                    "switch",
                    song.id,
                    line_no,
                    hanzi_translations[k].content,
                    tailo_translations[k].content,
                    "(dryrun)",
                )
            else:
                # save hanzi as new tailo
                Translation(
                    song=song,
                    line_no=line_no,
                    lang="tailo",
                    content=hanzi_translations[k].content,
                    contributor=contributor,
                ).save()

                # save tailo as new hanzi
                Translation(
                    song=song,
                    line_no=line_no,
                    lang="hanzi",
                    content=tailo_translations[k].content,
                    contributor=contributor,
                ).save()

                # log
                print(
                    "switch",
                    song.id,
                    line_no,
                    hanzi_translations[k].content,
                    tailo_translations[k].content,
                )
