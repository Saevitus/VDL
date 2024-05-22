import disnake, random, string, validators
from disnake.ext import commands
from pathlib import Path

from .img_dl_mixin import img_dl_mixin
from backend.utils import utils


class image_dl_cog(commands.Cog, img_dl_mixin):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"loaded: {self.qualified_name}")

    @commands.slash_command(name="dl_img", description="Download image(s) from URL")
    async def cmd(
        self,
        ctx: disnake.ApplicationCommandInteraction,
        url: str,
        custom_file_name: str = "",
    ):
        await ctx.response.defer(with_message=False)

        if not validators.url(url):
            await ctx.followup.send(
                content="Invalid URL, please try again.", delete_after=3
            )
            return

        if (
            len(custom_file_name) <= 0
        ):  # if supplied a custom file name, skip creating a randomized one
            custom_file_name = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )

        self.media = await self.img_dl(url, custom_file_name)

        if len(self.media) > 9:
            l = utils.split(
                self.media, 10
            )  # split into chunks of 10 and store in a new list
            for i in l:
                # loop and send all images
                await ctx.followup.send(content=f"Downloading image(s)", files=i)
        else:
            # otherwise if it's <=9 images we just post them all in one go
            await ctx.followup.send(content="Media downloaded.", files=self.media)

        # remove all files
        for fn in Path("vdl/media/").iterdir():
            fn.unlink()
        return


def setup(bot):
    bot.add_cog(image_dl_cog(bot))
