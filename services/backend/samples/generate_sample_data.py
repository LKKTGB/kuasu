import json
import os
import sys

import arrow

try:
    NUM_OF_USERS = int(sys.argv[1])
except:
    NUM_OF_USERS = 10

try:
    NUM_OF_SONGS = int(int(sys.argv[2]) / 10)
except:
    NUM_OF_SONGS = 100


class SampleDataGenerator:
    users = [
        {
            "model": "auth.user",
            "pk": i,
            "fields": {
                "first_name": "台語%d" % i,
                "last_name": "愛%d" % i,
                "username": "itaigi%d" % i,
                "password": "itaigi%d" % i,
            },
        }
        for i in range(1, NUM_OF_USERS + 1)
    ]
    songs = []
    translations = []

    def __init__(self):
        self.root = os.path.abspath(os.path.join(__file__, ".."))
        self.load_songs()
        self.load_original_lyrics()
        self.load_translations("hanzi")
        self.load_translations("tailo")

    def load_songs(self):
        today = arrow.get("2017-10-01T00:00:00.000+08:00")
        song_file = os.path.join(self.root, "songs.json")
        with open(song_file) as fp:
            sample_songs = json.load(fp)
        for i in range(NUM_OF_SONGS):
            base = i * 10
            self.songs.extend(
                [
                    {
                        "model": s["model"],
                        "pk": base + s["pk"],
                        "fields": {
                            "original_title": s["fields"]["original_title"]
                            + str(base + s["pk"]),
                            "tailo_title": s["fields"]["tailo_title"],
                            "performer": s["fields"]["performer"],
                            "hanlo_performer": s["fields"]["hanlo_performer"],
                            "lyricist": s["fields"]["lyricist"],
                            "composer": s["fields"]["composer"],
                            "hanzi_title": s["fields"]["hanzi_title"],
                            "hanlo_title": s["fields"]["hanlo_title"],
                            "youtube_url": s["fields"]["youtube_url"],
                            "readonly": s["fields"]["readonly"],
                            "created_at": (today.shift(hours=-i)).format(
                                "YYYY-MM-DD HH:mmZZ"
                            ),
                        },
                    }
                    for s in sample_songs
                ]
            )

    def load_original_lyrics(self):
        for song in self.songs:
            title = song["fields"]["hanzi_title"]
            lyric_file = os.path.join(self.root, title, "origin.txt")
            with open(lyric_file) as fp:
                song["fields"]["original_lyrics"] = fp.read().strip()

    def load_translations(self, lang):
        today = arrow.get("2017-10-01T00:00:00.000+08:00")
        for song in self.songs:
            title = song["fields"]["hanzi_title"]
            lyric_file = os.path.join(self.root, title, "%s.txt" % lang)
            with open(lyric_file) as fp:
                translations = fp.read().strip().split("\n")
            for i, lyric in enumerate(song["fields"]["original_lyrics"].split("\n")):
                if not lyric:
                    continue
                if not translations[i]:
                    continue
                self.translations.append(
                    {
                        "model": "thiamsu.Translation",
                        "pk": len(self.translations) + 1,
                        "fields": {
                            "song": song["pk"],
                            "line_no": i,
                            "lang": lang,
                            "content": translations[i],
                            "contributor": self.users[i % len(self.users)]["pk"],
                            "created_at": (today.shift(minutes=-i)).format(
                                "YYYY-MM-DD HH:mmZZ"
                            ),
                        },
                    }
                )

    def dump_sample_data(self):
        path = os.path.join(self.root, "sample_data.json")
        sample_data = self.users + self.songs + self.translations
        with open(path, "w") as fp:
            fp.write(json.dumps(sample_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    generator = SampleDataGenerator()
    generator.dump_sample_data()
