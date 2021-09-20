import os
from collections import OrderedDict

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.utils.translation import ugettext_lazy as _
from embed_video.admin import AdminVideoMixin, AdminVideoWidget
from embed_video.fields import EmbedVideoField
from social_django.models import Association, Nonce, UserSocialAuth
from solo.admin import SingletonModelAdmin

from thiamsu.forms import SongAdminForm
from thiamsu.models.hanzi_hanlo_mapping import HanziHanloMapping
from thiamsu.models.headline import Headline
from thiamsu.models.new_word import NewWord
from thiamsu.models.privacy_policy import PrivacyPolicy
from thiamsu.models.song import Song
from thiamsu.models.translation import Translation


class HanziHanloMappingAdmin(admin.ModelAdmin):
    list_display = ("hanzi", "hanlo")
    search_fields = ("hanzi",)


class HeadlineAdmin(admin.ModelAdmin):
    list_display = ("song", "start_time", "end_time")

    raw_id_fields = ("song",)
    autocomplete_lookup_fields = {"fk": ["song"]}


class NewWordInline(admin.StackedInline):
    model = NewWord

    extra = 0
    classes = ("grp-collapse grp-open",)
    inline_classes = ("grp-collapse grp-open",)


class AdminVideoTextInputWidget(AdminTextInputWidget, AdminVideoWidget):
    pass


class AdminVideoTextInputMixin(AdminVideoMixin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, EmbedVideoField):
            return db_field.formfield(widget=AdminVideoTextInputWidget)

        return super(AdminVideoMixin, self).formfield_for_dbfield(db_field, **kwargs)


class PrivacyPolicyAdmin(SingletonModelAdmin):
    class Media:
        js = ["thiamsu/js/tinymce/tinymce.min.js", "thiamsu/js/tinymce_settings.js"]


class SongAdmin(AdminVideoTextInputMixin, admin.ModelAdmin):
    LYRIC_FIELD_NAME_PREFIX = "original_lyrics_line_"

    list_display = ("original_title", "performer", "progress", "created_at")
    search_fields = ("original_title", "performer")
    form = SongAdminForm
    inlines = [NewWordInline]

    def generate_separated_lyric_fields(self, obj):
        fields = OrderedDict()
        for i, lyric in enumerate(obj.original_lyrics.split(os.linesep), start=1):
            label = f"{_('song_original_lyrics')}{_('line no %d') % i}"
            name = f"{self.LYRIC_FIELD_NAME_PREFIX}{i:04d}"
            lyric = lyric.strip()

            fields[name] = forms.CharField(
                label=label,
                max_length=100,
                initial=lyric,
                required=bool(lyric),
                widget=AdminVideoTextInputWidget,
            )

            # disable blank line
            if not fields[name].initial:
                fields[name].initial = ""
                fields[name].disabled = True

        return fields

    def get_form(self, request, obj=None, change=False, **kwargs):
        '''
        Note:

        get_form will be called twice in the followed order
        1. get_fields: the argument "change" is always "False".
        2. form rendering: the value of argument "change" depends on it's an add_view or change_view.

        So, we check object existence to decide to add separated lyric fields or not.
        '''
        if not obj: # object does not exist, reset declared_fields
            self.exclude = ("progress", "title_alias", "performer_alias")
            self.form.declared_fields = OrderedDict()
        else: # object exists, add separated lyric fields
            self.exclude = (
                "progress",
                "title_alias",
                "performer_alias",
                "original_lyrics",
            )
            lyrics_fields = self.generate_separated_lyric_fields(obj)
            self.form.declared_fields.update(lyrics_fields)
        return super().get_form(request, obj, **kwargs)

    def save_changed_original_lyrics(self, request, obj, form, change):
        def lyrics_changed(form):
            for c in form.changed_data:
                if c.startswith(self.LYRIC_FIELD_NAME_PREFIX):
                    return True
            return False

        if lyrics_changed(form):
            lyric_fields = [
                f
                for f in form.cleaned_data
                if f.startswith(self.LYRIC_FIELD_NAME_PREFIX)
            ]
            lyrics = os.linesep.join(
                [form.cleaned_data[f] for f in sorted(lyric_fields)]
            )
            obj.original_lyrics = lyrics
        obj.save()

    def save_model(self, request, obj, form, change):
        self.save_changed_original_lyrics(request, obj, form, change)
        return super().save_model(request, obj, form, change)


class TranslationAdmin(admin.ModelAdmin):
    list_display = (
        "song",
        "line_no",
        "content",
        "original_lyric",
        "lang",
        "created_at",
    )

    search_fields = ("song__original_title",)

    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"
    list_filter = ("lang",)


admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.register(HanziHanloMapping, HanziHanloMappingAdmin)
admin.site.register(Headline, HeadlineAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Translation, TranslationAdmin)
