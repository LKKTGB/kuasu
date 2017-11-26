from itertools import combinations

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from embed_video.fields import EmbedVideoField

from thiamsu.utils import get_youtube_id_from_url, translate_hanzi_to_hanlo
from unidecode import unidecode


def _to_alias(word):
    return unidecode(
        word
        .replace('-', ' ')
    )


def split_to_keyword_groups(keyword):
    segments = [k for k in keyword.split() if k.strip()]
    groups = []
    for n in range(len(segments) - 1, 1, -1):
        groups += tuple(combinations(segments, n))
    return [' '.join(g) for g in set(groups)]


class Song(models.Model):
    original_title = models.CharField(_('song_original_title'), max_length=100)
    hanzi_title = models.CharField(_('song_hanzi_title'), max_length=100)
    tailo_title = models.CharField(_('song_tailo_title'), max_length=100)
    hanlo_title = models.CharField(_('song_hanlo_title'), max_length=100)
    performer = models.CharField(_('song_performer'), max_length=100)
    hanlo_performer = models.CharField(_('song_hanlo_performer'), max_length=100)
    composer = models.CharField(_('song_composer'), max_length=100)
    lyricist = models.CharField(_('song_lyricist'), max_length=100)
    youtube_url = EmbedVideoField(_('song_youtube_url'))
    original_lyrics = models.TextField(_('song_original_lyrics'), default='')
    readonly = models.BooleanField(_('song_readonly'), default=False)

    title_alias = models.CharField(max_length=100, blank=True)
    performer_alias = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = _('song')
        verbose_name_plural = _('songs')

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'original_title__icontains',)

    def __str__(self):
        return u"%s (%s)" % (self.original_title, self.performer)

    def save(self, *args, **kwargs):
        self.title_alias = _to_alias(self.tailo_title)
        self.performer_alias = _to_alias(self.hanlo_performer)
        super().save(*args, **kwargs)

    @classmethod
    def search_title(cls, keyword):
        exact_match = cls.objects.filter(
            Q(original_title__icontains=keyword) |
            Q(hanzi_title__icontains=keyword) |
            Q(tailo_title__icontains=keyword) |
            Q(title_alias__icontains=_to_alias(keyword)))

        # 'a b c d' to ['a c d', 'a b c', 'b c d', 'a b d', 'b d', 'c d', 'a b', 'b c', 'a c', 'a d']
        keyword_groups = split_to_keyword_groups(keyword)
        multi_match = cls.objects.filter(
            Q(original_title__icontains=keyword_groups) |
            Q(hanzi_title__icontains=keyword_groups) |
            Q(tailo_title__icontains=keyword_groups) |
            Q(title_alias__icontains=[_to_alias(g) for g in keyword_groups]))

        # 'a b c' to ['a', 'b', 'c']
        single_match = cls.objects.filter(
            Q(original_title__icontains=keyword.split()) |
            Q(hanzi_title__icontains=keyword.split()) |
            Q(tailo_title__icontains=keyword.split()) |
            Q(title_alias__icontains=_to_alias(keyword).split()))
        return (exact_match | multi_match | single_match).distinct()

    @classmethod
    def search_performer(cls, keyword):
        exact_match = cls.objects.filter(
            Q(performer__icontains=keyword) |
            Q(hanlo_performer__icontains=keyword) |
            Q(performer_alias__icontains=_to_alias(keyword)))

        # 'a b c d' to ['a c d', 'a b c', 'b c d', 'a b d', 'b d', 'c d', 'a b', 'b c', 'a c', 'a d']
        keyword_groups = split_to_keyword_groups(keyword)
        multi_match = cls.objects.filter(
            Q(performer__icontains=keyword_groups) |
            Q(hanlo_performer__icontains=keyword_groups) |
            Q(performer_alias__icontains=[_to_alias(g) for g in keyword_groups]))

        # 'a b c' to ['a', 'b', 'c']
        single_match = cls.objects.filter(
            Q(performer__icontains=keyword.split()) |
            Q(hanlo_performer__icontains=keyword.split()) |
            Q(performer_alias__icontains=_to_alias(keyword).split()))
        return (exact_match | multi_match | single_match).distinct()

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
