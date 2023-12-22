import os
import yt_dlp
from backend.utils import utils

class yt_dl_mixin: 
    async def yt_dl(self, file_details):
        '''
        file_details = [ctx[0], url[1], custom_file_name[2], audio_only[3]]
        '''
        file = [] # forward declare the return file
    
        #print("HELLO" + file_details[1])

        ''' 
        declare the options dict for yt-dlp, I just found these on the yt-dlp github
        we're downloading the best video, best audio and splicing them together 
        file_details[2] is the custom_file_name
        '''
        ops = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl':"vdl/media/" + f'{file_details[2]}.%(ext)s',
        }
    
        # if audio_only, set ops to download audio only 
        if file_details[3]:
            ops = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl':"vdl/media/" + f'{file_details[2]}.%(ext)s',
            }

        '''
        2nd part of friends code, we check the custom_file_name, if it has
        "title" in it, then we set audio_only to true, and edit the ops to
        download the audio, however this time we use the inbuilt yt-dlp
        feature of getting the original title of the video we're downloading
        '''
        if file_details[2] == "title":
            file_details[3] = True
            ops = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl':"vdl/media/" + '%(title)s.%(ext)s',
        }

        # download file using the declared options above
        with yt_dlp.YoutubeDL(ops) as ydl:
            #print(file_details[1])
            ydl.download(file_details[1]) # [1] = url
    
        ''' 
        some ghetto walk-around code because I'm lazy, I was having an issue
        where downloading the file for my friends server, it'd try to just upload "title.mp3"
        so now I just loop the downloaded files and get the accurate name and split at the period
        '''
        for fn in os.listdir("vdl/media/"):
            file_type = ".mp3" if file_details[3] == True else ".mp4"
            file_details[2] = fn.split(file_type)[0]
            #print(file_details[2])
    
        # append the new media file to the list, checking the size at the same time 
        file.append(utils.get_size(fd=file_details))

        return file