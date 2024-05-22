# %%
import disnake
from disnake.ext import commands


class vdl(commands.InteractionBot):
    def __init__(self, intents):
        commands.InteractionBot.__init__(self, intents=intents)

        self.add_commands()

    async def on_ready(self):
        print(f"{self.user} has activated")
        print(f"In {len(self.guilds)} guilds")

    def add_commands(self):
        self.load_extension("cogs.media_dl_cog.media_dl")
        self.load_extension("cogs.image_dl_cog.image_dl")
        self.load_extension("cogs.audio_finder_cog.audio_finder")
        self.load_extension("cogs.format_converter_cog.format_converter")


if __name__ == "__main__":
    intents = disnake.Intents.all()
    intents.message_content = True

    m = vdl(intents)
    m.run("BOT TOKEN HERE")
# %%
