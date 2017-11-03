from django import forms

from thiamsu.utils import get_youtube_id_from_url


class SongAdminForm(forms.ModelForm):

    def clean_youtube_url(self):
        youtube_id = get_youtube_id_from_url(self.cleaned_data['youtube_url'])
        if not youtube_id:
            raise forms.ValidationError(
                'Invalid URL: %(url)s',
                code='invalid youtube url',
                params={'url': self.cleaned_data['youtube_url']},
            )
        return self.cleaned_data['youtube_url']
