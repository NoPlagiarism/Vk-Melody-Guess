from pydub import AudioSegment
import requests as r


def download(url, path, name="full.mp3"):
    res = r.get(url, allow_redirects=True)
    with open(path+name, 'wb') as f:
        f.write(res.content)


def execute_segment(start, end, path, in_file="full.mp3", out_file="short.mp3"):
    song = AudioSegment.from_mp3(path+in_file)
    extract = song[start:end]
    extract.export(path+out_file, format='mp3')
