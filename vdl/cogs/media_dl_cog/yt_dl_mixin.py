import os
import yt_dlp
from backend.utils import utils


class yt_dl_mixin:
    async def yt_dl(self, file_details):
        """
        file_details = {"ctx": ctx, "url": url, "is_tiktok": is_tiktok, "custom_file_name": custom_file_name, "audio_only": audio_only}
        """
        file = []  # forward declare the return file

        ops = {
            "format": "bestvideo[width=1920][ext=mp4]+bestaudio[ext=m4a]/mp4",
            "outtmpl": "vdl/media/" + f'{file_details["custom_file_name"]}.%(ext)s',
        }

        # not needed right now
        """if (file_details["is_tiktok"]):
            ops = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl':"vdl/media/" + f'{file_details["custom_file_name"]}.%(ext)s',
                'extractor_args': 'tiktok:api_hostname=api16-normal-c-useast1a.tiktokv.com;app_info=7355728856979392262',
            }
        """

        if file_details["is_twitter"]:
            # print("twitter")
            # ops["cookies"] = "vdl/backend/placeholder/twittter_cookies.txt" - broken right now?
            ops["username"] = "USERNAME"
            ops["password"] = "PASSWORD"
            # print(ops)

        if file_details["audio_only"]:
            ops["format"] = "bestaudio/best"
            ops["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
            """ops = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl':"vdl/media/" + f'{file_details["custom_file_name"]}.%(ext)s',
            }"""

        if file_details["custom_file_name"] == "title":
            file_details["audio_only"] = True

            ops["format"] = "bestaudio/best"
            ops["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
            ops["outtmpl"] = "vdl/media/" + "%(title)s.%(ext)s"

            """ops = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl':"vdl/media/" + '%(title)s.%(ext)s',
            }"""

        with yt_dlp.YoutubeDL(ops) as ydl:
            ydl.download([file_details["url"]])

        for fn in os.listdir("vdl/media/"):
            file_type = ".mp3" if file_details["audio_only"] == True else ".mp4"
            file_details["custom_file_name"] = fn.split(file_type)[0]

        file.append(utils.get_size(file_details=file_details))

        return file
