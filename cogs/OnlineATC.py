from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from lib.db import db
from dotenv import load_dotenv

import discord
import aiohttp
import os

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class OnlineATC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    scheduler = AsyncIOScheduler()
    db.autosave(scheduler)


    async def online(self):
        url = "https://data.vatsim.net/v3/vatsim-data.json"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    big_list = []
                    for controllers in data['controllers']:
                        callsign = controllers['callsign']
                        big_list.append(callsign)

                        if "VNSM_CTR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)
                            
                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)

                        if "VNSM_E_CTR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "VNSM_W_CTR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)

                        if "VNKT_APP" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "VNKT_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "VNKT_GND" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)

                        if "VNBW_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)

                        if "VNBP_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "VNVT_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)

                        if "VNJP_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "VNNG_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "VNPK_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "VNSI_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "VNCG_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "VNSK_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "VNDH_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)

                        if "VNRB_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "VNTR_TWR" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)
                        
                        if "ASIA_W_FSS" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                

                                name = controllers['name']
                                frequency = controllers['frequency']
                                logon_time = controllers['logon_time']

                                embed = discord.Embed(title = "ATC Online Alert :warning:", description = f"Looking for ATC? {callsign} is online on frequency {frequency}! Come fly & enjoy ATC service by {name}.",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                                online_channel = self.bot.get_channel(804352699997880321)
                                await online_channel.send(embed=embed)

                                value = "True"
                                db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)

                    
                    
                    
                    
                    if "VNSM_CTR" not in big_list:
                        callsign_find = "VNSM_CTR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNSM_E_CTR" not in big_list:
                        callsign_find = "VNSM_E_CTR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNSM_W_CTR" not in big_list:
                        callsign_find = "VNSM_W_CTR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNKT_APP" not in big_list:
                        callsign_find = "VNKT_APP"                   
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNKT_TWR" not in big_list:
                        callsign_find = "VNKT_TWR"      
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNKT_GND" not in big_list:
                        callsign_find = "VNKT_GND"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNBP_TWR" not in big_list:
                        callsign_find = "VNBP_TWR"            
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNVT_TWR" not in big_list:
                        callsign_find = "VNVT_TWR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNJP_TWR" not in big_list:
                        callsign_find = "VNJP_TWR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNNG_TWR" not in big_list:
                        callsign_find = "VNNG_TWR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNSI_TWR" not in big_list:
                        callsign_find = "VNSI_TWR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNCG_TWR" not in big_list:
                        callsign_find = "VNCG_TWR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNSK_TWR" not in big_list:
                        callsign_find = "VNSK_TWR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNDH_TWR" not in big_list:
                        callsign_find = "VNDH_TWR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNRB_TWR" not in big_list:
                        callsign_find = "VNRB_TWR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "VNTR_TWR" not in big_list:
                        callsign_find = "VNTR_TWR"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)
                    if "ASIA_W_FSS" not in big_list:
                        callsign_find = "ASIA_W_FSS"
                        db.execute("DELETE FROM onlineatc WHERE CallSign = ?", callsign_find)

 
            
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("online atc")
        self.scheduler.start()
        self.scheduler.add_job(self.online, CronTrigger(second="0"))                                

                    
                    

                       



def setup(bot):
    bot.add_cog(OnlineATC(bot))
