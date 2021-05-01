import logging
from configparser import ConfigParser
from discord.ext import commands
from cogs.cog_hello import Greetings
from cogs.cog_reddit_trends import RedditTrends


logging.basicConfig(format="%(asctime)s | %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")
config_object = ConfigParser()
config_object.read("resources/config.ini")
bot_config = config_object["BOT"]


class MyClient(commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        self.guild = ""
        self.channel = ""

    async def on_ready(self):
        logging.warning(f"Logged on as {self.user}!")
        for guild in client.guilds:
            if guild.name == bot_config["server_name"]:
                self.guild = guild
        for channel in self.guild.channels:
            if channel.name == bot_config["channel_name"]:
                self.channel = channel
        logging.warning(f"Connected to {self.channel} in {self.guild}")
        self.add_cog(Greetings(client))
        self.add_cog(RedditTrends(client))


client = MyClient(command_prefix="$")


client.run(bot_config["token"])
