from collections import OrderedDict
import os

from django import forms
from django.contrib import admin

from thiamsu.forms import SongAdminForm
from thiamsu.models.approved_translation import ApprovedTranslation
from thiamsu.models.new_word import NewWord
from thiamsu.models.song import Song
from thiamsu.models.translation import Translation


class NewWordInline(admin.StackedInline):
    model = NewWord


class SongAdmin(admin.ModelAdmin):
    LYRIC_FIELD_LABEL_PREFIX = 'Original lyrics line '
    LYRIC_FIELD_NAME_PREFIX = 'original_lyrics_line_'
    LYRIC_LINE_NO_TMPL = '%0004d'
    LYRIC_MAX_LENGTH = 100

    list_display = ('original_title', 'performer')
    form = SongAdminForm
    inlines = [
        NewWordInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            self.exclude = ()
        else:
            self.exclude = ('original_lyrics',)

        # reset declared_fields
        self.form.declared_fields = OrderedDict()
        return super().get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:  # add song
            return fields

        # change song
        for i, lyric in enumerate(obj.original_lyrics.split(os.linesep), start=1):
            label = self.LYRIC_FIELD_LABEL_PREFIX + (self.LYRIC_LINE_NO_TMPL % i)
            name = self.LYRIC_FIELD_NAME_PREFIX + (self.LYRIC_LINE_NO_TMPL % i)
            lyric = lyric.strip()

            # append to fields if not added
            if name not in fields:
                fields.append(name)

            # add to form declared fields if not added
            if name not in self.form.declared_fields:
                self.form.declared_fields[name] = forms.CharField(
                    label=label, max_length=self.LYRIC_MAX_LENGTH, initial=lyric)

            # update field value if added
            else:
                self.form.declared_fields[name].initial = lyric

            # disable blank line
            if not self.form.declared_fields[name].initial:
                self.form.declared_fields[name].initial = '--'
                self.form.declared_fields[name].disabled = True

        return fields

    def save_changed_original_lyrics(self, request, obj, form, change):
        def lyrics_changed(form):
            for c in form.changed_data:
                if c.startswith(self.LYRIC_FIELD_NAME_PREFIX):
                    return True
            return False

        if lyrics_changed(form):
            lyric_fields = [f for f in form.cleaned_data if f.startswith(self.LYRIC_FIELD_NAME_PREFIX)]
            lyrics = os.linesep.join([form.cleaned_data[f] for f in sorted(lyric_fields)])
            obj.original_lyrics = lyrics
        obj.save()

    def save_model(self, request, obj, form, change):
        self.save_changed_original_lyrics(request, obj, form, change)
        return super().save_model(request, obj, form, change)


class TranslationAdmin(admin.ModelAdmin):
    pass


class ApprovedTranslationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Song, SongAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(ApprovedTranslation, ApprovedTranslationAdmin)
