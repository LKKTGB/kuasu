from django.shortcuts import render, redirect

songs = [
    {'original_title': '鬼扮仙',
     'tailo_title': 'kuí pān-sian',
     'singer': '濁水溪公社',
     'youtube_id': '6nfRTnCSL-E'},
    {'original_title': '人生',
     'tailo_title': 'Jîn-sing',
     'singer': '黃妃',
     'youtube_id': 'hrExrKOqu6U'},
    {'original_title': '中壇元帥',
     'tailo_title': 'Tiong-tuânn guân-suè',
     'singer': '濁水溪公社',
     'youtube_id': 'pSRVX808K0Y'},
    {'original_title': '晚安台灣',
     'tailo_title': 'àm-an Tâi-uân',
     'singer': '濁水溪公社',
     'youtube_id': '9CqHgzYv4nw'},
    {'original_title': '寂寞的島',
     'tailo_title': 'siok-bo̍k ê tó',
     'singer': '王昭華',
     'youtube_id': 'mZGB5cE7EMw'},
    {'original_title': '暮沉武德殿',
     'tailo_title': 'Bōo-tîm Bú-tik-tiān',
     'singer': '閃靈',
     'youtube_id':'NVzmek3PqNs'},
    {'original_title': '向前走',
     'tailo_title': 'Hiòng-tsiân Kiânn',
     'singer': '林強',
     'youtube_id': 'gD14iiXq7Xw'},
    {'original_title': '無詞的歌',
     'tailo_title': 'Bô-sû ê Kua',
     'singer': '秀蘭瑪雅 ',
     'youtube_id': 'OHjPWMS216Q'},
    {'original_title': '釘子花',
     'tailo_title': 'Ting-á-hue',
     'singer': '伍佰 & China Blue',
     'youtube_id': '3MHVNxd130E'},
    {'original_title': '島嶼天光',
     'tailo_title': 'tó-sū thinn-kng',
     'singer': '滅火器',
     'youtube_id': 'iV8JDbtXZm4'},
]

for song in songs:
    song['youtube_url'] = 'https://www.youtube.com/watch?v={id}'.format(
        id=song['youtube_id']
    )
    song['cover_url'] = 'https://img.youtube.com/vi/{id}/hqdefault.jpg'.format(
        id=song['youtube_id']
    )
songs[0]['progress'] = 85.1


def home(request):
    return render(request, 'thiamsu/home.html', {
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

    return render(request, 'thiamsu/search_result.html', {
        'query': query,
        'songs': filtered_songs,
    })
