from django.shortcuts import render, redirect

from .sample_data import songs, lyrics


def home(request):
    return render(request, 'thiamsu/song_list.html', {
        'songs': songs,
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
