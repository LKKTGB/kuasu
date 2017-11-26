from collections import OrderedDict
import os

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.utils.translation import ugettext_lazy as _
from embed_video.admin import AdminVideoWidget, AdminVideoMixin
from embed_video.fields import EmbedVideoField
from social_django.models import Association, Nonce, UserSocialAuth

from thiamsu.forms import SongAdminForm
from thiamsu.models.headline import Headline
from thiamsu.models.new_word import NewWord
from thiamsu.models.song import Song
from thiamsu.models.translation import Translation


class HeadlineAdmin(admin.ModelAdmin):
    list_display = ('song', 'start_time', 'end_time')

    raw_id_fields = ('song',)
    autocomplete_lookup_fields = {
        'fk': ['song'],
    }


class NewWordInline(admin.StackedInline):
    model = NewWord

    extra = 0
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class AdminVideoTextInputWidget(AdminTextInputWidget, AdminVideoWidget):
    pass


class AdminVideoTextInputMixin(AdminVideoMixin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, EmbedVideoField):
            return db_field.formfield(widget=AdminVideoTextInputWidget)

        return super(AdminVideoMixin, self).formfield_for_dbfield(db_field, **kwargs)


class SongAdmin(AdminVideoTextInputMixin, admin.ModelAdmin):
    LYRIC_FIELD_LABEL_PREFIX = _('song_original_lyrics')
    LYRIC_FIELD_NAME_PREFIX = 'original_lyrics_line_'
    LYRIC_LINE_NO_TMPL = _('line no %d')
    LYRIC_MAX_LENGTH = 100

    list_display = ('original_title', 'performer')
    search_fields = ('original_title', 'performer')
    form = SongAdminForm
    inlines = [
        NewWordInline,
    ]
    exclude = ('title_alias', 'performer_alias')

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
                    label=label, max_length=self.LYRIC_MAX_LENGTH, initial=lyric,
                    required=bool(lyric),
                    widget=AdminVideoTextInputWidget)

            # update field value if added
            else:
                self.form.declared_fields[name].initial = lyric

            # disable blank line
            if not self.form.declared_fields[name].initial:
                self.form.declared_fields[name].initial = ''
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
    list_display = ('song', 'lang', 'content', 'original_lyric', 'created_at')


admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.register(Headline, HeadlineAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Translation, TranslationAdmin)
