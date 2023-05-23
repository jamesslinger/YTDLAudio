from pytube import YouTube


# noinspection PyMethodMayBeStatic
class AudioStream:
    def __init__(self):
        self.artist = "<Artist>-"
        self.track_name = "<Track Name>"
        self.id = None
        self.duration = None
        self.bitrate = None
        self.filesize = None
        self.thumbnail = "static/images/music.png"
        self.source_url = None

    def fetch_streams(self, url):
        yt_data = YouTube(url)
        audio_streams = yt_data.streams.filter(only_audio=True)
        all_streams = []
        for stream in audio_streams:
            stream_item = AudioStream()
            stream_item.source_url = url
            stream_item.thumbnail = yt_data.thumbnail_url
            stream_item.artist = yt_data.author
            stream_item.track_name = yt_data.title
            duration_calc = str(yt_data.length / 60).split('.')
            stream_mins = int(duration_calc[0])
            stream_secs = int(float('0.' + duration_calc[1])*60)
            stream_item.duration = f"{stream_mins} mins {stream_secs} secs"
            stream_item.id = stream.itag
            stream_item.bitrate = stream.abr
            stream_item.filesize = f"{round(stream.filesize / 1000 / 1000)}MB"
            all_streams.append(stream_item)
        all_streams.sort(key=lambda x: x.filesize, reverse=False)
        return all_streams

    def download_track(self, url, track_id):
        yt_data = YouTube(url)
        dl_track = yt_data.streams.get_by_itag(track_id)
        return dl_track.download(filename=f"{dl_track.title}.mp3")
