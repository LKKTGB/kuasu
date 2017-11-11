from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

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

    query_type = request.GET.get('type', '')
    if query_type not in ['song-title', 'performer']:
        return redirect('/')

    if query_type == 'song-title':
        filtered_songs = Song.objects.filter(
            Q(original_title__contains=query) |
            Q(hanzi_title__contains=query) |
            Q(tailo_title__contains=query))
    else:  # performer
        filtered_songs = Song.objects.filter(
            Q(performer__contains=query))

    paginator = Paginator(
        filtered_songs, settings.PAGINATION_MAX_ITMES_PER_PAGE)
    return render(request, 'thiamsu/song_list.html', {
        'query': query,
        'songs': paginator.page(1),
    })


def song_detail(request, id):
    try:
        song = Song.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect('/')

    return render(request, 'thiamsu/song_detail.html', {
        'song': song,
        'lyrics': [{
            'original': lyric,
            'translation': 'siâ-khì，si-tshàu，môo-sîn-á'
        } for lyric in song.original_lyrics.split('\n')],
    })
