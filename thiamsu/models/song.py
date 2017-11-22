from django.db import models

from thiamsu.utils import get_youtube_id_from_url, translate_hanzi_to_hanlo


class Song(models.Model):
    original_title = models.CharField(max_length=100, help_text='原文歌名')
    hanzi_title = models.CharField(max_length=100, help_text='全漢歌名')
    tailo_title = models.CharField(max_length=100, help_text='全羅歌名')
    hanlo_title = models.CharField(max_length=100, help_text='漢羅歌名')
    performer = models.CharField(max_length=100, help_text='演唱人')
    hanlo_performer = models.CharField(max_length=100, help_text='演唱人（台文）')
    composer = models.CharField(max_length=100, help_text='作曲人')
    lyricist = models.CharField(max_length=100, help_text='作詞人')
    youtube_url = models.CharField(max_length=100, help_text='Youtube 網址')
    original_lyrics = models.TextField(default='', help_text='原文歌詞')
    readonly = models.BooleanField(default=False, help_text='鎖定編修')

    @property
    def youtube_id(self):
        return get_youtube_id_from_url(self.youtube_url)

    @property
    def cover_url(self):
        return 'https://img.youtube.com/vi/{id}/hqdefault.jpg'.format(
            id=self.youtube_id
        )

    def get_lyrics_with_translations(self):
        from thiamsu.models.translation import Translation

        def query_translations(lang):
            latest_translation_times = (
                Translation.objects
                .filter(song=self.id)
                .filter(lang=lang)
                .values('line_no')
                .annotate(models.Max('created_at'))
                .order_by()
            )

            q_statement = models.Q()
            for pair in latest_translation_times:
                q_statement |= (models.Q(line_no__exact=pair['line_no']) &
                                models.Q(created_at__exact=pair['created_at__max']))
            translations = (
                Translation.objects
                .filter(song=self.id)
                .filter(lang=lang)
                .filter(q_statement)
            )
            return {t.line_no: t.content for t in translations}

        hanzi_lyrics = query_translations('hanzi')
        tailo_lyrics = query_translations('tailo')

        lyrics_with_translations = []
        for i, lyric in enumerate(self.original_lyrics.split('\n')):
            lyrics_with_translations.append({
                'original': lyric,
                'hanzi': hanzi_lyrics.get(i),
                'tailo': tailo_lyrics.get(i),
                'hanlo': translate_hanzi_to_hanlo(hanzi_lyrics.get(i))
            })
        return lyrics_with_translations

    def get_new_words(self):
        from thiamsu.models.new_word import NewWord
        return NewWord.objects.filter(song=self)
