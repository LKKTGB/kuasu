from django.urls.base import reverse
from rest_framework import serializers

from .models.song import Song


class SongSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = [
            "original_title",
            "hanzi_title",
            "tailo_title",
            "hanlo_title",
            "performer",
            "hanlo_performer",
            "composer",
            "lyricist",
            "youtube_url",
            "progress",
            "url",
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        path = reverse(viewname="song_detail", kwargs={"id": obj.id})
        return request.build_absolute_uri(path)
