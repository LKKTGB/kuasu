from rest_framework import generics, routers

from .models.song import Song
from .serializers import SongSerializer


class SongList(generics.ListAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = Song.objects.all()
        progress = self.request.query_params.get("progress")
        if progress is not None:
            queryset = queryset.filter(progress=progress)
        return queryset
