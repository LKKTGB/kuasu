from django import forms
from django.forms import formset_factory
from django.forms.formsets import BaseFormSet
from django.forms.widgets import HiddenInput

from thiamsu.utils import get_youtube_id_from_url


class SongAdminForm(forms.ModelForm):
    def clean_youtube_url(self):
        youtube_id = get_youtube_id_from_url(self.cleaned_data["youtube_url"])
        if not youtube_id:
            raise forms.ValidationError(
                "Invalid URL: %(url)s",
                code="invalid youtube url",
                params={"url": self.cleaned_data["youtube_url"]},
            )
        return self.cleaned_data["youtube_url"]


class TranslationForm(forms.Form):
    line_no = forms.IntegerField(widget=forms.HiddenInput)
    lang = forms.CharField(max_length=5, widget=forms.HiddenInput)
    content = forms.CharField(max_length=1000, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["line_no"].widget.attrs["readonly"] = True
        self.fields["lang"].widget.attrs["readonly"] = True


class BaseTranslationFormSet(BaseFormSet):
    def __init__(self, original_lyrics=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set original lyric as label of each line
        if not original_lyrics or len(original_lyrics) != len(self.forms):
            return
        for i, form in enumerate(self.forms):
            form.fields["content"].label = original_lyrics[i]


TranslationFormSet = formset_factory(
    TranslationForm, formset=BaseTranslationFormSet, extra=0
)


class SongReadonlyForm(forms.Form):
    readonly = forms.BooleanField(required=False)


class UserFavoriteSongForm(forms.Form):
    method = forms.ChoiceField(choices=[(m, m) for m in ("POST", "DELETE")])
    song_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["method"].widget = HiddenInput()
        self.fields["song_id"].widget = HiddenInput()
