import discord
from datetime import time
from discord.ext import commands, tasks
from collections import defaultdict
from config import config
import pytz
import asyncio

"""
tasks for future:
1) to save reports to DB for future analysis
2) to scedule start_daily_report and send_report
3) pretty format for daily report
"""


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


department_responses = defaultdict(list)


run_at = time(hour=23, minute=18, tzinfo=pytz.timezone("Europe/Kyiv"))


class ReportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_report.start()

    def cog_unload(self):
        self.send_report.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user.name}")

    @commands.command()
    async def report(self, ctx, department: str, *, response: str):
        department_responses[department.lower()].append(response)
        await ctx.send(f"Response for {department} department saved.")

    @commands.command()
    async def start_daily_report(self, ctx):
        await ctx.send(
            "Daily report has started. Please submit your responses before 20:00 Berlin time."
        )

    @tasks.loop(hours=24)
    async def send_report(self):
        channel = self.bot.get_channel(config["CHANNEL_ID"])
        if channel:
            await channel.send(repr(department_responses))


async def main():
    cog = ReportCog(bot)
    await bot.add_cog(cog)
    await bot.start(config["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
