from django.db import models
from django.utils.translation import ugettext_lazy as _

from thiamsu.utils import get_youtube_id_from_url, translate_hanzi_to_hanlo


class Song(models.Model):
    original_title = models.CharField(_('song_original_title'), max_length=100)
    hanzi_title = models.CharField(_('song_hanzi_title'), max_length=100)
    tailo_title = models.CharField(_('song_tailo_title'), max_length=100)
    hanlo_title = models.CharField(_('song_hanlo_title'), max_length=100)
    performer = models.CharField(_('song_performer'), max_length=100)
    hanlo_performer = models.CharField(_('song_hanlo_performer'), max_length=100)
    composer = models.CharField(_('song_composer'), max_length=100)
    lyricist = models.CharField(_('song_lyricist'), max_length=100)
    youtube_url = models.CharField(_('song_youtube_url'), max_length=100)
    original_lyrics = models.TextField(_('song_original_lyrics'), default='')
    readonly = models.BooleanField(_('song_readonly'), default=False)

    class Meta:
        verbose_name = _('song')
        verbose_name_plural = _('songs')

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'original_title__icontains',)

    def __str__(self):
        return u"%s (%s)" % (self.original_title, self.performer)

    @property
    def youtube_id(self):
        return get_youtube_id_from_url(self.youtube_url)

    @property
    def cover_url(self):
        return 'https://img.youtube.com/vi/{id}/hqdefault.jpg'.format(
            id=self.youtube_id
        )

    @property
    def progress(self):
        from thiamsu.models.translation import Translation

        translated_lines = (
            Translation.objects
            .filter(song=self.id)
            .values('song', 'lang')
            .annotate(count=models.Count('line_no', distinct=True))
        )

        translated_count = sum([t['count'] for t in translated_lines])
        total_count = len([line for line in self.original_lyrics.split('\n') if line.strip()])
        total_count = total_count * len(translated_lines)
        return int(translated_count / total_count * 100)

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
