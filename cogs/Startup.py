from discord.ext import commands
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lib.db import db
from datetime import datetime
from dotenv import load_dotenv
import aiohttp
import discord
import os
import requests


load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class Startup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    scheduler = AsyncIOScheduler()
    db.autosave(scheduler)


    async def DMQuote(self):
        user1 = self.bot.get_user(id = 388955006633508865)
        user2 = self.bot.get_user(id = 405974183604912140)
        url = "http://quotes.rest/qod.json?category=love"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    try:
                        await user1.send(f"*{data['contents']['quotes'][0]['quote']}*\n\n~ {data['contents']['quotes'][0]['author']}")
                    except:
                        pass
                    try:
                        await user2.send(f"*{data['contents']['quotes'][0]['quote']}*\n\n~ {data['contents']['quotes'][0]['author']}")
                    except:
                        pass
    
    
    
    async def APIcall(self):
        headers = {'Authorization' : "$WnY%#vMN@U_UA28xtg"}
        r = requests.get("https://www.members.nepalvacc.com/api/events/update", headers=headers)
        r1 = requests.get("https://www.members.nepalvacc.com/api/dashboard/update", headers=headers)
        r2 = requests.get("https://www.controllers.nepalvacc.com/api/data/update", headers=headers)

        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        
        if r.status_code != 200:
            await channel.send(f"**{r.status_code}** Status Code at Update Events API Endpoint, https://www.members.nepalvacc.com/api/events/update returned an error. ```{r.json()}```")

        if r1.status_code != 200:
            await channel.send(f"**{r1.status_code}** Status Code at Update Events API Endpoint, https://www.members.nepalvacc.com/api/dashboard/update returned an error. ```{r1.json()}```")
        
        if r2.status_code != 200:
            await channel.send(f"**{r2.status_code}** Status Code at Controller Roster API Endpoint, https://www.controllers.nepalvacc.com/api/data/update returned an error. ```{r2.json()}```")
    
    @commands.Cog.listener()
    async def on_connect(self):
        self.bot.launch_time = datetime.utcnow()
        print("Bot connected!")

    @commands.Cog.listener()
    async def on_ready(self):
        activity = discord.Activity(name="Nepal vACC Airspace | Developed by Mufassil Yasir | v1.1.6", type=discord.ActivityType.watching)
        await self.bot.change_presence(activity=activity)
        print ("Starting up")
        self.scheduler.start()
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        await channel.send("Getting Ready..... Engines Started! :man_running: ")
        self.scheduler.add_job(self.DMQuote, CronTrigger(hour=4,minute=0,second=0))
        self.scheduler.add_job(self.APIcall, CronTrigger(second=0, minute=0, hour="1,5,9,13,18,23"))
    
    @commands.command(description = "This command gets you the bot it self statistics. Run the command `?botinfo` and try it out!")
    async def uptime(self, ctx):
        embed = discord.Embed(title = "My Statistics:", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
        embed.set_thumbnail(url = self.bot.user.avatar_url)

        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        fields = [("Bot version:", "v1.1.6", True),
                   ( "Uptime:", f"{days}d, {hours}h, {minutes}m, {seconds}s", True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def forcedmquote(self, ctx):
        await self.DMQuote()

def setup(bot):
    bot.add_cog(Startup(bot))