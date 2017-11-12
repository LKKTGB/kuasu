from datetime import date, timedelta
import json
import os


class SampleDataGenerator:
    users = [{
        'model': 'auth.user',
        'pk': '1',
        'fields': {
            'first_name': '阿明',
            'last_name': '張',
            'username': 'ming',
            'password': '1234'
        }
    }, {
        'model': 'auth.user',
        'pk': '2',
        'fields': {
            'first_name': '阿花',
            'last_name': '陳',
            'username': 'flower',
            'password': '1234'
        }
    }]
    songs = []
    translations = []

    def __init__(self):
        self.root = os.path.abspath(os.path.join(__file__, '..'))
        self.load_songs()
        self.load_original_lyrics()
        self.load_translations('hanzi')
        self.load_translations('tailo')

    def load_songs(self):
        song_file = os.path.join(self.root, 'songs.json')
        with open(song_file) as fp:
            self.songs.extend(json.load(fp))

    def load_original_lyrics(self):
        for song in self.songs:
            title = song['fields']['hanzi_title']
            lyric_file = os.path.join(self.root, title, 'origin.txt')
            with open(lyric_file) as fp:
                song['fields']['original_lyrics'] = fp.read().strip()

    def load_translations(self, lang):
        today = date(2017, 10, 1)
        for song in self.songs:
            title = song['fields']['hanzi_title']
            lyric_file = os.path.join(self.root, title, '%s.txt' % lang)
            with open(lyric_file) as fp:
                translations = fp.read().strip().split('\n')
            for i, lyric in enumerate(song['fields']['original_lyrics'].split('\n')):
                if not lyric:
                    continue
                if not translations[i]:
                    continue
                self.translations.append({
                    'model': 'thiamsu.Translation',
                    'pk': str(len(self.translations) + 1),
                    'fields': {
                        'song': song['pk'],
                        'line_no': i,
                        'lang': lang,
                        'content': translations[i],
                        'contributor': self.users[i % 2]['pk'],
                        'created_at': (today - timedelta(hours=len(self.translations))).strftime('%Y-%m-%d %H:%M')
                    }
                })

    def dump_sample_data(self):
        path = os.path.join(self.root, 'sample_data.json')
        sample_data = self.users + self.songs + self.translations
        with open(path, 'w') as fp:
            fp.write(json.dumps(sample_data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    generator = SampleDataGenerator()
    generator.dump_sample_data()
