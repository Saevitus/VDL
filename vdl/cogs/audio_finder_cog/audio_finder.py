import disnake, os, yt_dlp
from disnake.ext import commands
from shazamio import Shazam

from vdl.cogs.image_dl_cog.img_dl_mixin import img_dl_mixin
#import backend.audio_finder as af
from .af_mixin import af_mixin
#import backend.lib as lib

#@lib.add_methods_from(fa)


class audio_finder_cog(commands.Cog, af_mixin, img_dl_mixin):
    def __init__(self, bot):
        self.bot = bot  
  
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"loaded: {self.qualified_name}")
              
    @commands.slash_command(name="find_audio", description="Download image(s) from URL")
    async def cmd(self, ctx: disnake.ApplicationCommandInteraction, url: str):    
        await ctx.response.defer(with_message=False)
    
        # get the shazam output json    
        out = await self.find_audio(url)
        if out is None:
            await ctx.followup.send(content = "No song found.", delete_after = 3)
            return
    
        # if there's no track key in the shazam json, no song is found & return
        if "track" not in out:
            await ctx.followup.send(content = "No song found.", delete_after = 3)
            return

            # if there was a track found within the json, 
            # we get the specific parts from the json that we need
        song_name = out["track"]["share"]["text"] 
        cover_url = out["track"]["images"]["coverarthq"]   
            
            #print(song_name)
            #print(cover_url)
             
            # download the album cover image & audio file to add into the message 
            # ngl the audio file part was a glitch that i never fixed bc i liked it
        self.media = await self.img_dl(url = cover_url, filename = song_name)
        
        
        # send the name of the song & both the album cover pic & the mp3
        await ctx.followup.send(content = song_name, files = self.media)

        # clean up & delete the album cover & mp3
        for fn in os.listdir("vdl/media/"):
            os.remove("vdl/media/" + fn)
        return

def setup(bot):
    bot.add_cog(audio_finder_cog(bot))  