from __future__ import annotations
from requests import Session
from warnings import simplefilter
from moviepy.editor import *
from backend.utils import utils
import os, shutil
import disnake
simplefilter('ignore')

# global variables for ease of access
# using 3rd party website to download tiktoks as it's far easier
BASE_URL = "https://www.tikwm.com" 
session = None

class tt_dl_mixin:
    async def tt_dl(self, file_details):
        '''download tiktok video/images by scraping the HTML and getting source url from tikwm'''
        '''file_details = [ctx[0], url[1], custom_file_name[2], audio_only[3]]'''
        global BASE_URL, session # access our global variables
        session = Session() # create new session
        # forward declare the filename and return_list variables
        fn = "" 
        retn_list = []
        it = 0
        
        # use session to send a post request to the website using it's API
        # I stole this from someone but I can't remember who
        req = session.post(BASE_URL + "/api/", data=dict(url=file_details[1], count=12, cursor=0, web=1, hd=1))
        res = req.json() # get the JSON out of the post request
        
        # if response code is 0 (succeeded) do rest of code
        if res["code"] == 0:
            if(file_details[3]): # audio_only
                # if the url for the audio is stored within the json object data:music
                audio = res["data"]["music"]
                
                # if the custom filename has contents, set fn to the full filename with extension
                if file_details[2]:
                    fn = file_details[2] if ".mp3" in file_details[2] else file_details[2] + ".mp3"
                op_dir = os.path.join("vdl/media/", fn)
                
                # download the tiktok audio, same downloading code as for the video, won't comment any more
                with session.get(BASE_URL + audio, stream=True) as r:
                    with open(op_dir, "wb") as f:
                        shutil.copyfileobj(r.raw, f)
                        retn_list.append(disnake.File(op_dir))
                        return retn_list
            
            # check if images is contained within the data element in the response json
            if "images" in res["data"]:
                # for each image stored in the data:images object, there can be a very large amount
                for image in res["data"]["images"]:
                    '''
                    same name code as above except we add an iterator to it
                    to increment the filenames for each image within a gallary
                    '''
                    if file_details[2]:
                        fn = file_details[2] + str(it) if ".jpeg" in file_details[2] else file_details[2] + str(it) + ".jpeg"
                        it += 1
                    op_dir = os.path.join("vdl/media/", fn)
        
                    # same download code as for the video, won't comment any more
                    with session.get(image, stream=True) as r:
                        with open(op_dir, "wb") as f:
                            shutil.copyfileobj(r.raw, f)
                            retn_list.append(disnake.File(op_dir))
                return retn_list
            
            # get the video object from the json data, it's stored within data:play
            video_object = res["data"].get("play", res["data"]["play"])
            
            # if the custom filename has contents, set fn to the full filename with extension
            if file_details[2]:
                fn = file_details[2] if ".mp4" in file_details[2] else file_details[2] + ".mp4"
            # set the operational directory to vdl/media/ + fn that we just set
            op_dir = os.path.join("vdl/media/", fn)
        
            # download the tiktok video
            with session.get(BASE_URL + video_object, stream=True) as r:
                # open the directory + file using our declared op_dir, as wb (writing the file as binary)
                with open(op_dir, "wb") as f:
                    # copies the raw contents of the downloaded video to the file we just created using open
                    shutil.copyfileobj(r.raw, f)
                    
                    # if audio_only
                    if(file_details[3]):
                        # use videofileclip with the supplied op_dir to convert the .mp4 to .mp3
                        VideoFileClip(op_dir).audio.write_audiofile("vdl/media/" + file_details[2] + ".mp3")
                        
                        # append and return from here so that you skip appending the .mp4 if you've chosen audio_only
                        retn_list.append(disnake.File("vdl/media/" + file_details[2] + ".mp3"))
                        return retn_list
                    
                    # append and return
                    retn_list.append(utils.get_size(fd=file_details))
            return retn_list
    
#download_image("https://vt.tiktok.com/ZSLnNHeoA/", "dwadwa")