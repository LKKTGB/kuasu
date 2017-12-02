from collections import defaultdict, OrderedDict
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from thiamsu.forms import SongReadonlyForm, TranslationFormSet, UserFavoriteSongForm
from thiamsu.models.headline import Headline
from thiamsu.models.song import Song
from thiamsu.models.translation import Translation
from thiamsu.paginator import Paginator


def _sorted_songs(request, songs):
    sorting_type = request.GET.get('sort', 'original')

    if sorting_type == 'original':
        songs = songs.order_by('-original_title')
    elif sorting_type == 'tailo':
        songs = songs.order_by('tailo_title')
    else:  # progress
        pass  # TODO

    return songs


def _paginated_songs(request, songs):
    page = request.GET.get('page', 1)

    paginator = Paginator(songs, settings.PAGINATION_MAX_ITMES_PER_PAGE)
    try:
        songs = paginator.page(page)
    except PageNotAnInteger:
        songs = paginator.page(1)
    except EmptyPage:
        songs = paginator.page(paginator.num_pages)

    return songs


def home(request):
    songs = Song.objects

    now = datetime.now()
    try:
        headline = (
            Headline.objects
            .filter(start_time__lte=now, end_time__gte=now)
            .latest('start_time')
        )
    except ObjectDoesNotExist:
        headline = None

    songs = _sorted_songs(request, songs)
    songs = _paginated_songs(request, songs)

    return render(request, 'thiamsu/song_list.html', {
        'songs': songs,
        'headline': headline.song if headline else None,
    })


def search(request):
    query = request.GET.get('keyword', '')
    if query == '':
        return redirect('/')

    query_type = request.GET.get('type', '')
    if query_type not in ['song-title', 'performer']:
        return redirect('/')

    if query_type == 'song-title':
        songs = Song.search_title(query)
    else:  # performer
        songs = Song.search_performer(query)

    songs = _sorted_songs(request, songs)
    songs = _paginated_songs(request, songs)

    return render(request, 'thiamsu/song_list.html', {
        'query': query,
        'songs': songs,
    })


def api_user_favorite_song(request):
    if request.method != 'POST':
        return redirect('/')

    form = UserFavoriteSongForm(data=request.POST)

    if not form.is_valid():
        return redirect('/')

    method = form.cleaned_data['method']
    song_id = form.cleaned_data['song_id']
    if method == 'POST':
        request.user.profile.favorite_songs.add(song_id)
    elif method == 'DELETE':
        request.user.profile.favorite_songs.remove(song_id)
    return redirect('/song/%s' % song_id)


def update_song(request, id):
    if request.method != 'POST':
        return redirect('/')
    try:
        song = Song.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect('/')

    form = SongReadonlyForm(data=request.POST)

    if form.is_valid():
        song.readonly = form.cleaned_data['readonly']
        song.save()
        return redirect('/song/%s' % id)
    else:
        return redirect('/')


def song_detail(request, id):
    if request.method == 'POST':
        return update_song(request, id)
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

    is_favorite_song = request.user.profile.favorite_songs.filter(id=song.id).exists()
    return render(request, 'thiamsu/song_detail.html', {
        'song': song,
        'contributors': {
            'tailo': format_contributors(get_full_name(get_contributors('tailo'))),
            'hanzi': format_contributors(get_full_name(get_contributors('hanzi')))
        },
        'lyrics': song.get_lyrics_with_translations(),
        'new_words': song.get_new_words(),
        'readonly_form': SongReadonlyForm(initial={'readonly': song.readonly}),
        'is_favorite_song': is_favorite_song,
        'favorite_form': UserFavoriteSongForm(initial={
            'method': 'DELETE' if is_favorite_song else 'POST',
            'song_id': song.id
        })
    })


def song_edit(request, id):
    try:
        song = Song.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect('/')
    if song.readonly:
        return redirect('/song/%s' % id)

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


def get_top_song_contributors():
    # FIXME: improve performance
    contributors = (
        User.objects
        .annotate(count=models.Count('translation__song'))
        .order_by('-count')[:10]
    )
    contributors = [{
        'id': c.id,
        'username': c.get_full_name(),
        'avatar_url': c.profile.avatar_url,
        'count': c.count
    } for c in contributors]
    contributors = [c for c in contributors if c['username']]
    return contributors


def get_top_line_contributors():
    # FIXME: improve performance
    contributor_song_line_count = (
        Translation.objects
        .values('contributor', 'song')
        .annotate(count=models.Count('line_no'))
    )

    contributor_line_count = defaultdict(int)
    for c in contributor_song_line_count:
        contributor_line_count[c['contributor']] += c['count']

    contributors = []
    for contributor, count in contributor_line_count.items():
        if not contributor:
            continue
        user = User.objects.get(id=contributor)
        contributors.append({
            'id': user.id,
            'username': user.get_full_name(),
            'avatar_url': user.profile.avatar_url,
            'count': count})
    contributors = sorted(contributors, key=lambda c: c['count'], reverse=True)[:10]
    return contributors


def get_contribution_rank(user_id, contribution_type):
    assert contribution_type in ['songs', 'lines']
    contributors = {
        'songs': get_top_song_contributors,
        'lines': get_top_line_contributors
    }[contribution_type]()
    try:
        rank = [u['id'] for u in contributors if u['count'] > 0].index(user_id) + 1
    except ValueError:
        rank = 0
    return rank


def chart(request):
    return render(request, 'thiamsu/chart.html', {
        'top_song_contributors': get_top_song_contributors(),
        'top_line_contributors': get_top_line_contributors()
    })


def user_profile(request, id):
    def get_contributions(user):
        latest_translations = (
            Translation.objects
            .filter(contributor=user)
            .values('song')
            .annotate(contribute_at=models.Max('created_at'))
        )
        contribute_time = {t['song']: t['contribute_at'] for t in latest_translations}
        songs = list(Song.objects.filter(id__in=contribute_time.keys()))
        songs = sorted(songs, key=lambda s: contribute_time[s.id], reverse=True)
        return songs

    try:
        viewee = User.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect('/')

    favorites = viewee.profile.favorite_songs.all()
    contributions = get_contributions(viewee)

    kind = request.GET.get('kind', 'favs')
    if kind == 'favs':
        songs = favorites
    elif kind == 'contribs':
        songs = contributions
    else:
        return redirect(reverse(user_profile, kwargs={'id': viewee.id}))

    songs = _paginated_songs(request, songs)

    return render(request, 'thiamsu/user_profile.html', {
        'viewee': viewee,
        'kind': kind,
        'favorite_count': len(favorites),
        'contribution_count': len(contributions),
        'songs': songs,
        'rank_or_contributions_by_songs': get_contribution_rank(int(id), 'songs'),
        'rank_or_contributions_by_lines': get_contribution_rank(int(id), 'lines')
    })
