import os
from shazamio import Shazam
import yt_dlp


class af_mixin:
    async def find_audio(self, url):
        fn = ""

        ops = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": "vdl/media/" + "%(title)s.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ops) as ydl:
            ydl.download(url)  # [1] = url

        for f in os.listdir("vdl/media/"):
            if ".mp3" in f:
                fn = f
                print("TEST :" + fn)

        shazam = Shazam()
        # print("vdl/media/" + fn)
        out = await shazam.recognize_song("vdl/media/" + fn)

        return out
