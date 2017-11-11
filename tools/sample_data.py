
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


def prepare_songs():
    for song in songs:
        song['youtube_url'] = 'https://www.youtube.com/watch?v={id}'.format(
            id=song['youtube_id']
        )
        song['cover_url'] = 'https://img.youtube.com/vi/{id}/hqdefault.jpg'.format(
            id=song['youtube_id']
        )
    songs[0]['progress'] = 85.1


prepare_songs()


raw_lyrics = [
    ('厝崩 橋㽎 眾生掣', 'tshù pang，kiô sìm，tsiòng-sing tshuah'),
    ('霆雷 爍爁 天烏陰', 'tân-luî，sih-nah，thinn oo-im'),
    ('砲火 銃聲 獨裁者', 'phàu-hué，tshìng-siann，to̍k-tshâi-tsiá'),
    ('邪氣 屍臭 魔神仔', 'siâ-khì，si-tshàu，môo-sîn-á'),
    ('昨暝夢中 輕聲細說是誰人', 'tsâng-mê bāng-tiong，khin-siann sè-sueh sī siánn lâng'),
    ('今日亂世 改朝換代是佗一冬', 'kin-ji̍t luān-sè，kái tiâu uānn tāi sī tó tsi̍t tang'),
    ('武德殿外 敵我不明對誰來效忠', 'bú-tik-tiān guā，ti̍k gónn put bîng tuì siánn lâi hāu tiong'),
    ('醒靈寺內 鬼神難分 向誰來詛誓', 'tshénn-lîng-sī lāi，kuí-sîn lân hun hiòng siánn lâi tsiù-tsuā'),
    ('厝崩 橋㽎 眾生掣', 'tshù pang，kiô sìm，tsiòng-sing tshuah'),
    ('霆雷 爍爁 天烏陰', 'tân-luî，sih-nah，thinn oo-im'),
    ('砲火 銃聲 獨裁者', 'phàu-hué，tshìng-siann，to̍k-tshâi-tsiá'),
    ('邪氣 屍臭 魔神仔', 'siâ-khì，si-tshàu，môo-sîn-á'),
    ('昨暝夢中 輕聲細說是誰人 (敢是我)', 'tsâng-mê bāng-tiong，khin-siann sè-sueh sī siánn lâng (kám sī guá)'),
    ('今日亂世 改朝換代是佗一冬 (敢是夢)', 'kin-ji̍t luān-sè，kái tiâu uānn tāi sī tó tsi̍t tang (kám sī bāng)'),
    ('武德殿外 敵我不明對誰來效忠 (佮誰參詳)', 'bú-tik-tiān guā，ti̍k gónn put bîng tuì siánn lâi hāu tiong (kap siánn tsham-siông)'),
    ('醒靈寺內 鬼神難分 向誰來詛誓', 'tshénn-lîng-sī lāi，kuí-sîn lân hun hiòng siánn lâi tsiù-tsuā'),
    ('向誰詛誓 等誰宣判', 'hiòng siánn tsiù-tsuā，tán siánn suan-phuànn'),
    ('向誰詛誓 等誰宣判', 'hiòng siánn tsiù-tsuā，tán siánn suan-phuànn'),
    ('孽鏡台 鑿目光 火薰中 愈來愈明', 'gi̍k kiànn-tâi，tsha̍k-ba̍k kng，hué-hun tiong，lú-lâi-lú bîng'),
    ('跤鐐手銬 拖磨聲 迷亂中 愈來愈清', 'kha-liâu tshiú-khàu，thua-buâ siann，bê-luān tiong，lú-lâi-lú tshing'),
    ('萬劫不復', 'bān kiap put ho̍k'),
    ('萬劫不復', 'bān kiap put ho̍k'),
    ('萬劫不復', 'bān kiap put ho̍k'),
    ('萬劫不復', 'bān kiap put ho̍k'),
    ('數百年 戰袂煞 我輩武德', 'sòo pah nî，tsiàn bē suah，ngóo-puē bú-tik'),
    ('千萬人 拚袂退 勇者無敵', 'tshian-bān lâng，piànn bē thè，ióng-tsiá bû-tik'),
    ('數百年 戰袂煞 我輩武德', 'sòo pah nî，tsiàn bē suah，ngóo-puē bú-tik'),
    ('千萬人 拚袂退 勇者無敵', 'tshian-bān lâng，piànn bē thè，ióng-tsiá bû-tik'),
    ('千年也萬年', 'tshian nî iā bān nî'),
    ('我孤魂已束縛佇遮 千年也萬年', 'guá koo-hûn í sok-pa̍k tī tsia，tshian nî iā bān nî'),
    ('生死簿的名字', 'sing-sí-phōo ê miâ-jī'),
    ('目睭前一逝一逝 生死簿的名字', 'ba̍k-tsiu tsîng tsi̍t tsuā tsi̍t tsuā，sing-sí-phōo ê miâ-jī'),
    ('千年也萬年', 'tshian-nî iā bān-nî'),
    ('生死簿的名字', 'sing-sí-phōo ê miâ-jī'),
    ('數百年 戰袂煞 我輩武德', 'sòo pah nî，tsiàn bē suah，ngóo puē bú-tik'),
    ('千萬人 拚袂退 勇者無敵', 'tshian bān lâng piànn bē thè ióng tsiá bû tik'),
    ('數百年 戰袂煞 我輩武德', 'sòo pah nî，tsiàn bē suah，ngóo puē bú-tik'),
    ('千萬人 拚袂退 勇者無敵', 'tshian bān lâng，piànn bē thè，ióng tsiá bû tik'),
    ('千年也萬年', 'tshian-nî iā bān-nî'),
    ('生死簿的名字', 'sing-sí-phōo ê miâ-jī'),
    ('千年也萬年', 'tshian-nî iā bān-nî'),
]

lyrics = list(map(lambda l: {'original': l[0], 'translation': l[1]}, raw_lyrics))
