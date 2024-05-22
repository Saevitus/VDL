# Import necessary libraries
from __future__ import annotations
from requests import Session
from warnings import simplefilter
from moviepy.editor import *
from backend.utils import utils
import os, shutil
import disnake

# Ignore warnings
simplefilter("ignore")

# Define base URL for TikTok
BASE_URL = "https://www.tikwm.com"
# Initialize session variable
session = None

# Define a class tt_dl_mixin
class tt_dl_mixin:
    # Define an asynchronous function tt_dl
    async def tt_dl(self, file_details):
        # Access global variables BASE_URL and session
        global BASE_URL, session
        # Create a new session
        session = Session()

        # Send a POST request to the website using its API
        req = session.post(
            BASE_URL + "/api/",
            data=dict(url=file_details["url"], count=12, cursor=0, web=1, hd=1),
        )
        # Get the JSON response from the POST request
        res = req.json()

        # If the response code is 0 (success), proceed
        if res["code"] == 0:
            # If audio_only flag is set, download the audio
            if file_details["audio_only"]:
                audio = res["data"]["music"]
                fn = self.get_filename(file_details, ".mp3")
                retn_list.append(self.download_file(BASE_URL + audio, fn))
                return retn_list

            # If images are present in the response, download them
            if "images" in res["data"]:
                for image in res["data"]["images"]:
                    fn = self.get_filename(file_details, ".jpeg", it)
                    it += 1
                    retn_list.append(self.download_file(image, fn))
                return retn_list

            # Download the video
            video_object = res["data"].get("play", res["data"]["play"])
            fn = self.get_filename(file_details, ".mp4")
            self.download_file(BASE_URL + video_object, fn)