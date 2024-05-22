import disnake, os, re, ffmpeg
from disnake.ext import commands
from enum import Enum
from requests import Session


class format_converter_cog(commands.Cog):
    class choices(str, Enum):
        mp4 = "mp4"
        webm = "webm"
        gif = "gif"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"loaded: {self.qualified_name}")

    @commands.slash_command(name="convert_format", description="Convert file formats")
    async def cmd(
        self,
        ctx: disnake.ApplicationCommandInteraction,
        choice: choices,
        att: disnake.Attachment = None,
    ):
        """
        Convert media files to gif/webm/mp4

        Parameters
        ----------
        choice: :class:`choices`
            File format to convert to
        att: :class:`disnake.Attachment`
            The attached file to be converted
        """

        def convert(file):
            name, ext = os.path.splitext(file)
            out_name = name + "." + choice
            ffmpeg.input(file).output(out_name).run()
            print(f"Finished converting {file}")

        await ctx.response.defer(with_message=False)

        # file_type = ".mp3" if fd[3] == True else ".mp4"

        final_url = str(att)  # if att else url

        converted_fn = ""
        session = Session()

        with session.get(final_url, stream=True, allow_redirects=True) as r:
            # open the directory + file using our declared op_dir, as wb (writing the file as binary)
            cd = r.headers.get("content-disposition")
            if cd == None:
                await ctx.followup.send(
                    content="Content Disposition not found.", delete_after=4
                )
                return

            fname = re.findall("filename=(.+)", cd)
            # print(fname[0].split(".")[1])

            if fname[0].split(".")[1] == choice:
                await ctx.followup.send(
                    content="Can't convert video to the same format.", delete_after=4
                )
                return

            open("vdl/media/" + fname[0], "wb").write(r.content)

        for fn in os.listdir("vdl/media/"):
            convert(os.path.join("vdl/media/", fn))
            os.remove(os.path.join("vdl/media/", fn))

            converted_fn = "vdl/media/" + fn.split(".")[0] + "." + choice
            break

        await ctx.followup.send(
            content="Media converted.", file=disnake.File(converted_fn)
        )
        os.remove(converted_fn)


def setup(bot):
    bot.add_cog(format_converter_cog(bot))
