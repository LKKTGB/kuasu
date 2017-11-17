from collections import defaultdict

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from thiamsu.forms import TranslationFormSet
from thiamsu.models.song import Song
from thiamsu.models.translation import Translation


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

    def get_contributors(lang):
        contributors = (
            Translation.objects
            .filter(song=song)
            .filter(lang=lang)
            .values('contributor')
            .annotate(count=models.Count('contributor'))
        )
        return sorted(contributors, key=lambda c: c['count'], reverse=True)

    def get_full_name(contributors):
        contributors_with_full_name = [{
            'username': User.objects.get(id=c['contributor']).get_full_name(),
            'count':c['count']
        } for c in contributors if c['contributor']]
        return contributors_with_full_name

    def format_contributors(contributors):
        return ' '.join(['{username} ({count})'.format(**c) for c in contributors])

    return render(request, 'thiamsu/song_detail.html', {
        'song': song,
        'contributors': {
            'tailo': format_contributors(get_full_name(get_contributors('tailo'))),
            'hanzi': format_contributors(get_full_name(get_contributors('hanzi')))
        },
        'lyrics': song.get_lyrics_with_translations(),
        'new_words': song.get_new_words()
    })


def song_edit(request, id):
    try:
        song = Song.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect('/')

    lyrics = song.get_lyrics_with_translations()

    forms = {}
    for lang in ['tailo', 'hanzi']:
        forms[lang] = TranslationFormSet(
            original_lyrics=[lyric['original'] for lyric in lyrics if lyric['original']],
            initial=[{
                'line_no': line_no,
                'lang': lang,
                'content': lyric[lang]
            } for line_no, lyric in enumerate(lyrics) if lyric['original']])

    return render(request, 'thiamsu/song_edit.html', {
        'song': song,
        'forms': forms
    })


def song_translation_post(request, id):
    if request.method != 'POST':
        return redirect('/')
    try:
        song = Song.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect('/')

    formset = TranslationFormSet(data=request.POST)
    for form in formset:
        # validate data
        if not form.is_valid():
            continue
        if not form.cleaned_data['content']:
            continue

        # compare with current
        update_translation = False
        try:
            current_translation = (
                Translation.objects
                .filter(song=song)
                .filter(line_no=form.cleaned_data['line_no'])
                .filter(lang=form.cleaned_data['lang'])
                .latest('created_at')
            )
        except ObjectDoesNotExist:
            update_translation = True
        else:
            if form.cleaned_data['content'] != current_translation.content:
                update_translation = True

        # update
        if update_translation is True:
            new_translation = Translation(
                song=song,
                line_no=form.cleaned_data['line_no'],
                lang=form.cleaned_data['lang'],
                content=form.cleaned_data['content'],
                contributor=request.user if request.user.is_authenticated() else None
            )
            new_translation.save()

    return HttpResponseRedirect(reverse('song_edit', kwargs={'id': id}))


def chart(request):
    # FIXME: improve performance

    # get top song contributors
    top_song_contributors = (
        User.objects
        .annotate(song_count=models.Count('translation__song'))
        .order_by('-song_count')[:10]
    )

    # get top line contributors
    top_line_contributors_per_song = (
        Translation.objects
        .values('contributor', 'song')
        .annotate(line_count_per_song=models.Count('line_no'))
    )

    contributors = defaultdict(int)
    for top_line_contributor_per_song in top_line_contributors_per_song:
        contributor = top_line_contributor_per_song['contributor']
        contributors[contributor] += top_line_contributor_per_song['line_count_per_song']

    top_line_contributors = [{
        'username': User.objects.get(id=contributor).username,
        'contributor': contributor,
        'line_count': line_count
    } for contributor, line_count in contributors.items() if contributor]
    top_line_contributors = sorted(top_line_contributors, key=lambda c: c['line_count'], reverse=True)[:10]

    return render(request, 'thiamsu/chart.html', {
        'top_song_contributors': top_song_contributors,
        'top_line_contributors': top_line_contributors
    })
