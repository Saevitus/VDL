import disnake, os, random, string, ffmpeg, shutil
from disnake.ext import commands
from enum import Enum
from requests import Session

class format_converter_cog(commands.Cog):
    class choices(str, Enum):
        webm = 'webm'
        gif = 'gif'
    
    def __init__(self, bot):
        self.bot = bot  
  
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"loaded: {self.qualified_name}")
        
    @commands.slash_command(name="convert_format", description="Convert file formats")
    async def cmd(self, ctx: disnake.ApplicationCommandInteraction, choice: choices, att: disnake.Attachment = None, url: str = ""):    
        """
        Convert mp4 to gif/webm

        Parameters
        ----------
        choice: :class:`choices`
            File format to convert to
        att: :class:`disnake.Attachment`
            The attached file to be converted
        url: :class:`str`
            The url for the file to be converted
        """
        def convert(file):
            name, ext = os.path.splitext(file)
            out_name = name + "." + choice
            ffmpeg.input(file).output(out_name).run()
            print(f"Finished converting {file}")
                
        await ctx.response.defer(with_message=False)
            
        #file_type = ".mp3" if fd[3] == True else ".mp4"
            
        final_url = str(att) if att else url
        #print("first: " + final_url)
        #if url:
            #final_url = url
        #elif att:
            #final_url = str(att)
            
        #await self.download_media(ctx, final_url)
            
        converted_fn = ""
        session = Session()
            

        with session.get(final_url, stream=True) as r:
            # open the directory + file using our declared op_dir, as wb (writing the file as binary)
            with open("vdl/media/test.mp4", "wb") as f:
                # copies the raw contents of the downloaded video to the file we just created using open
                shutil.copyfileobj(r.raw, f)
                #retn_list.append(disnake.File(op_dir))
            
        for fn in os.listdir("vdl/media/"):
            print("test 312321")
            print("Found file: %s" % fn)
                
            if ".mp4" in fn:
                convert(os.path.join("vdl/media/", fn))
                os.remove(os.path.join("vdl/media/", fn))
                    
                converted_fn = "vdl/media/" + fn.split(".")[0] + "." + choice
                print("second: " + converted_fn)
                break
            
            if ".webm" in fn:
                convert(os.path.join("vdl/media/", fn))
                os.remove(os.path.join("vdl/media/", fn))
                    
                converted_fn = "vdl/media/" + fn.split(".")[0] + "." + choice
                print("third: " + converted_fn)
                break
                           
                    
        print("forth" + converted_fn)
        await ctx.followup.send(content = "Media converted.", file = disnake.File(converted_fn))
        os.remove(converted_fn)

def setup(bot):
    bot.add_cog(format_converter_cog(bot))  