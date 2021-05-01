from discord.ext import commands, tasks
from tasks.reddit_scraper import get_reddit_crypto_trends
import json
from datetime import date


class RedditTrends(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = bot.channel
        self.reddit_trending_cryptos_task.start()
        with open("resources/currency_board.json") as f:
            self.currency_board = json.load(f)

    def cog_unload(self):
        self.reddit_trending_cryptos_task.cancel()

    @tasks.loop(hours=24.0)
    async def reddit_trending_cryptos_task(self):
        await self.reddit_trending_cryptos(self.channel)

    @commands.command()
    async def reddittrends(self, ctx):
        await ctx.send("Getting reddit trends...")
        await self.reddit_trending_cryptos(ctx)

    async def reddit_trending_cryptos(self, ctx_channel):
        crypto_trends = await get_reddit_crypto_trends()
        new_currency_board = [coin[1] for coin in crypto_trends]
        alt_crypto_trends = [
            coin for coin in crypto_trends if coin[1] not in ("BTC", "ETH")
        ]
        count = 1
        message = "__Top 20 trending alt-coins in r/CryptoCurrency today:__\n\n"
        for coin in alt_crypto_trends[:20]:
            message = (
                message
                + f"{count}. **{coin[1]}** ({coin[0]}) - **{coin[2]}** mentions."
            )
            if self.currency_board:
                message = message + self.currency_difference_string(
                    new_currency_board, coin[1]
                )
            else:
                message = message + "\n"
            count = count + 1
        with open("resources/currency_board.json", "w") as file:
            json.dump(new_currency_board, file)
        with open(
            f"resources/currency_board_history/"
            f"{date.today().strftime('%d-%m-%Y')}.json",
            "w",
        ) as file:
            new_currency_board_with_mentions = [
                [coin[1], coin[2]] for coin in crypto_trends
            ]
            json.dump(new_currency_board_with_mentions, file)
        self.currency_board = new_currency_board
        await ctx_channel.send(message)

    def currency_difference_string(self, new_currency_board, coin):
        difference = new_currency_board.index(coin) - self.currency_board.index(coin)
        if difference > 0:
            return f" (*-{difference}*)\n"
        if difference < 0:
            return f" (*+{abs(difference)}*)\n"
        else:
            return "\n"
