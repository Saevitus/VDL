import disnake, os, random, string, validators
from disnake.ext import commands

from vdl.backend.utils import utils
from .tt_dl_mixin import tt_dl_mixin
from .yt_dl_mixin import yt_dl_mixin


class media_dl_cog(commands.Cog, yt_dl_mixin, tt_dl_mixin):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"loaded: {self.qualified_name}")

    async def download_media(
        self, ctx, url: str, custom_file_name: str = "", audio_only: bool = False
    ):
        """
        Main media download function, it takes the discord bot context,
        url and optional paramaters custom_file_name and audio_only
        """

        if (
            len(str(custom_file_name)) <= 0
        ):  # if supplied a custom file name, skip creating a randomized one
            custom_file_name = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )

        is_tiktok = False
        if "tiktok.com" in url:
            is_tiktok = True

        is_twitter = False
        if "twitter.com" or "x.com" in url:
            is_twitter = True

        # forward declare variables for later use
        # give a list containing the file details to help reduce the amount of paramaters for a function
        file_details = {
            "ctx": ctx,
            "url": url,
            "is_tiktok": is_tiktok,
            "is_twitter": is_twitter,
            "custom_file_name": custom_file_name,
            "audio_only": audio_only,
        }

        """
        tiktok has hand-written code rather than using yt-dlp for it as the files uploaded to discord 
        don't embed, plus you can't download albums/images from tiktok using yt-dlp
        <<< NEEDS UPDATING >>>
        """
        if is_tiktok:
            self.media = await self.tt_dl(file_details)
        else:
            self.media = await self.yt_dl(
                file_details
            )  # if not tiktok, download using yt-dlp

    @commands.Cog.listener()
    async def on_message(self, ctx):
        """
        on_message listener, here with this code it enables us to just
        post links into chat and have them downloaded if you don't feel the need to
        customize the files with a custom filename, or audio only
        """

        # if the chat message length is 0 return (sounds kinda dumb, but it's for attachments)
        if len(ctx.content) <= 0:
            return

        if not validators.url(ctx.content):
            return

        # same server/channel check as above
        if ctx.guild:
            name = ctx.channel.name
            id = ctx.channel.id
            # 1st id = music channel, 2nd id = group general
            if not (
                id == 1081923842487877702
                or id == 1204994689988821022  # group channel is private server
                or "dl-channel" in name
                or "owna" in name
            ):
                # if not ("dl-channel" in name or "owna" in name or "general-reforged" in name) and ctx.channel.id != 1081923842487877702:
                return
        """
        custom code for friends server, checks the channel & 
        if videos are posted in said channel they will automatically be downloaded
        as .mp3s with the title of the video
        """
        if ctx.channel.id == 1081923842487877702:
            """
            force-feed the function the custom filename "title" which we check again later
            alongside setting audio_only to true
            """
            # from backend.yt_dl import _yt_dl
            await self.download_media(ctx, ctx.content, "title", True)
            # check for filesize to big, post in chat and delete after 3 secs
            if self.media[0].filename == "FSTB.png":
                await ctx.channel.send(
                    content="File size too big.", files=self.media, delete_after=3
                )
            else:  # we have to use channel.send here because there is no followup in a message listener
                await ctx.channel.send("Media downloaded.", files=self.media)

            for fn in os.listdir("vdl/media/"):
                os.remove("vdl/media/" + fn)
            return

        # get the media list
        # from backend.yt_dl import _yt_dl
        await self.download_media(ctx, ctx.content)

        # same placeholder code I commented as above
        if self.media[0].filename == "FSTB.png":
            await ctx.channel.send(
                content="File size too big.", files=self.media, delete_after=3
            )
            for fn in os.listdir("vdl/media/"):
                os.remove("vdl/media/" + fn)
            return

        # same tiktok code I commented as above
        if len(self.media) > 9:
            l = utils.split(self.media, 10)
            for i in l:
                await ctx.channel.send(content=f"Downloading image(s)", files=i)
        else:
            await ctx.channel.send(content="Media downloaded.", files=self.media)

        # del
        for fn in os.listdir("vdl/media/"):
            os.remove("vdl/media/" + fn)
        return

    @commands.slash_command(name="dl_media", description="Download video from URL")
    async def cmd(
        self,
        ctx: disnake.ApplicationCommandInteraction,
        url: str,
        custom_file_name: str = "",
        audio_only: bool = False,
    ):
        """
        /dl command, using ApplicationCommandInteraction, we can use slash commands with responses
        """
        # defer the response so the bot sits there thinking until all code has been executed & a followup has been sent
        await ctx.response.defer(with_message=False)

        if not validators.url(url):
            await ctx.followup.send(
                content="Invalid URL, please try again.", delete_after=3
            )
            return

        """
        if in server check + channel check combined in one.
        when you check "if guild", it'll return true or false based on
        if you're communicating with the bot in a server vs DMs
        we check the different channels which blanket bans all other channels from being used
        """
        if ctx.guild:
            name = ctx.channel.name
            id = ctx.channel.id
            if not (
                id == 1081923842487877702
                or id == 1164523892073836574
                or "dl-channel" in name
                or "owna" in name
            ):
                await ctx.followup.send(
                    content="Wrong channel, please use the correct channels for the bot",
                    delete_after=3,
                )
                return

        # get the media list
        # print(url)
        await self.download_media(ctx, url, custom_file_name, audio_only)

        """
        checking to see if the first index filename of the media is the placeholder, if it is, 
        we post the placeholder but delete after 3 seconds
        """
        if self.media[0].filename == "FSTB.png":
            await ctx.followup.send(
                content="File size too big.", files=self.media, delete_after=3
            )
            for fn in os.listdir("vdl/media/"):
                os.remove("vdl/media/" + fn)
            return

        # messy tiktok code specifically for the gallery/image tiktoks, if greater than 9 images, we split
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
        for fn in os.listdir("vdl/media/"):
            os.remove("vdl/media/" + fn)
        return


def setup(bot):
    bot.add_cog(media_dl_cog(bot))
