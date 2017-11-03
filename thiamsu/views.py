from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .sample_data import songs, lyrics
from thiamsu.models.song import Song


def home(request):
    songs = Song.objects.order_by('original_title')
    paginator = Paginator(songs, settings.PAGINATION_MAX_ITMES_PER_PAGE)
    return render(request, 'thiamsu/song_list.html', {
        'songs': paginator.page(1),
    })


def search(request):
    query = request.GET.get('q', '')
    if query == '':
        return redirect('/')

    filtered_songs = (s for s in songs if (
        query in s['original_title'] or
        query in s['tailo_title'] or
        query in s['singer']
    ))

    return render(request, 'thiamsu/song_list.html', {
        'query': query,
        'songs': filtered_songs,
    })


def song_detail(request, id):
    matched_songs = [s for s in songs if (
        s['youtube_id'] == id
    )]
    song = matched_songs[0] if len(matched_songs) > 0 else None

    return render(request, 'thiamsu/song_detail.html', {
        'song': song,
        'lyrics': lyrics,
    })
