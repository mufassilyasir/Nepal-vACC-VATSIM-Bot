from discord.ext import commands
from datetime import datetime,timedelta
from time import time
from typing import Optional
from dotenv import load_dotenv

import aiohttp
import asyncio
import discord
import os

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Hi command
    @commands.command(description = "Returns you a hello. Just use `?hi` and woala bot will reply back")
    async def Hi(self, ctx):
        await ctx.send(f"Hello {ctx.message.author.name}!")
    
    #Ping command
    @commands.command(description = "This command basically calculates the time taken from the message being sent by the user and the message being returned by the bot. 'ms' is an abbreviation of 'milliseconds' Simply use `?ping` and you shall get a ping. ", brief = "Returns time taken by the server to respond back in ms")
    async def Ping(self, ctx):
        start = time()
        message = await ctx.send("Pinging Server...")
        end = time()

        await message.edit(content = f"Server to Discord latency: `{self.bot.latency*1000:,.0f}` ms\nUser to bot response time `{(end-start)*1000:,.0f}` ms. :rocket:")

    #nepal AIP dm command
    @commands.command(description = "This command will send you AIP link in your DM. The AIP has complete list of airports in Nepal including charts of all airports.", brief = "Sends you the AIP link in DM")
    async def NepalAIP(self, ctx):
        try:
            await ctx.message.author.send(f"Hey there! :wave:  The Nepal AIP that you requested in {ctx.guild.name} is available through this link:\n https://e-aip.caanepal.gov.np/welcome/listall/1 ")
        except:
            await ctx.send(f"Oh no! :confused: {ctx.message.author.display_name}, I can't reach your DM. Check your privacy settings. `Err: DM NOT REACHABLE` ")
        else:
            await ctx.send(f"Sent! :thumbsup: {ctx.message.author.display_name}, check your DM.")
            channel = self.bot.get_channel(LOG_CHANNEL_ID)
            embed = discord.Embed(Title = "**Nepal AIP DM Command Used**",colour=discord.Colour(0xff0000),description = f"Nepal AIP command used in {ctx.message.channel.mention} by {ctx.message.author.mention}, was successfully executed", timestamp = datetime.utcnow())
            await channel.send(embed=embed)
    
    #vnkt AIP dm command
    @commands.command(description = "This command will send you Kathmandu (VNKT) airport charts link in your DM.", brief = "Sends you VNKT airport charts link in DM")
    async def VNKTcharts(self, ctx):
        try:
            await ctx.message.author.send(f"Hey there! :wave: The VNKT AIP that you requested in {ctx.guild.name} is available through this link:\n https://e-aip.caanepal.gov.np/_uploads/_pdf/a6426a6018832c85c3421b8251de3246.pdf")
        except:
            await ctx.send(f"Oh no! :confused: {ctx.message.author.display_name}, I can't reach your DM. Check your privacy settings. `Err: DM NOT REACHABLE` ")
        else:
            await ctx.send(f"Sent! :thumbsup: {ctx.message.author.display_name}, check your DM.")
            channel = self.bot.get_channel(LOG_CHANNEL_ID)
            embed = discord.Embed(Title = "**VNKT AIP DM Command Used**",colour=discord.Colour(0xff0000),description = f"VNKT AIP command used in {ctx.message.channel.mention} by {ctx.message.author.mention}, was successfully executed", timestamp = datetime.utcnow())
            await channel.send(embed=embed)
    
    #userinfo command
    @commands.command(description = "This command will give you public information about a user account. Make sure to mention them correctly.", brief = "Returns information for a user leave empty to check your self")
    async def UserInfo(self, ctx, target: Optional[discord.Member]):
        target = target or ctx.message.author

        embed = discord.Embed(title = "User Information", colour = target.colour,timestamp = datetime.utcnow())
        embed.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.name}")
        embed.set_thumbnail(url = target.avatar_url)
        fields = [("ID", target.id,  False), 
                ("Name", str(target.name), True),
                ("Bot?", target.bot, True),
                ("Created Discord account on", target.created_at.strftime("%d/%m/%Y %H:%M:%S UTC"), True),
                ("Joined this server on", target.joined_at.strftime("%d/%m/%Y %H:%M:%S UTC"), True)]
        
        for name, value, inline in fields:
            embed.add_field(name = name, value = value, inline = inline)
        await ctx.send(embed=embed)
    
    #serverinfo command
    @commands.command(description = "This command returns server information. For example when it was created at, Number of members and more!", brief = "Returns server information")
    async def ServerInfo(self, ctx):
        embed = discord.Embed(title= "Server Information", colour = discord.Colour(0xff0000),timestamp = datetime.utcnow())
        embed.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.name}")
        embed.set_thumbnail(url = ctx.guild.icon_url)
        fields1 = [("Server Name", ctx.guild.name, True),
                    ("Owner", ctx.guild.owner.mention, True),
                    ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S UTC"), True),
                    ("Members including bots", len(ctx.guild.members), True),
                    ("Living Creatures", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                    ("\u200b", "\u200b", True)]
        
        for name, value, inline in fields1:
            embed.add_field(name = name, value = value, inline = inline)
        await ctx.send(embed=embed)
    
   #metar API
    @commands.command(description = "This command returns metar for the specified ICAO code and tries to decode it. Simply use `?metar` followed by the ICAO code and you shall recieve the METAR information for that airport... hopefully.", brief = "Returns metar for the specified ICAO")
    async def Metar(self, ctx,*,icao_random :str):
        icao = icao_random.upper()
        url = f"https://api.checkwx.com/metar/{icao}/decoded"

        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                headers = {"X-API-Key": "MYKEY"}
                async with cs.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()

                        if data["results"] == 1:
                            await ctx.send("Finding.....", delete_after = 1.0)
                            data_original = data["data"][0]['raw_text']
                            formatted_data = str(data_original)

                            store_for_t = data['data'][0]['observed']
                            remove_t = store_for_t.replace('T', ' ')



                            embed = discord.Embed(title = "Metar Information", colour = discord.Color(0xff0000))
                            embed.add_field(inline=False, name=f"{icao} Metar:", value=formatted_data)
                            embed2 = discord.Embed(title = "Decoded Metar", colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                            embed2.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.name}")
                            embed2.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.name}")
                            embed2.add_field(inline=False, name="Airport Name:", value=data['data'][0]['station']['name'])
                            embed2.add_field(inline=False, name="Observed at:", value=remove_t)
                            try:
                                embed2.add_field(inline=False, name="Wind direction:", value=str(data['data'][0]['wind']['degrees'])+" Degrees")
                                embed2.add_field(inline=False, name="Wind speed:", value=str(data['data'][0]['wind']['speed_kts'])+" Knots")
                            except:
                                embed2.add_field(inline=False, name="Wind direction:", value="Winds Calm")
                                embed2.add_field(inline=False, name="Wind speed:", value="Winds Calm")
                            embed2.add_field(inline=False, name="Visibility:", value=str(data['data'][0]['visibility']['meters'])+" Meters")
                            embed2.add_field(inline=False, name="Temperature:", value=str(data['data'][0]['temperature']['celsius'])+"C")
                            embed2.add_field(inline=False, name="Dewpoint:", value=str(data['data'][0]['dewpoint']['celsius'])+"C")
                            embed2.add_field(inline=False, name="QNH:", value=str(data['data'][0]['barometer']['hpa'])+" hPa")

                            await ctx.send(embed=embed)
                            await ctx.send("Decoding...", delete_after = 2.0)
                            await asyncio.sleep(1.0)
                            await ctx.send(embed=embed2)
                    
                        else:
                            await ctx.send(f"Uhhh {ctx.message.author.name}, I could not find that ICAO Code. Are you sure that ICAO code matches an airport ICAO? :face_with_monocle: `Err: InvalidICAOCode` ")

                    elif response.status == 401:
                        await ctx.send("This doesn't happen often. Mufassil kindly look into this. `Err:InvalidKey`")
                    
                    elif response.status == 429:
                        await ctx.send("If you see this, it's an error unfortunately. This means the bot is unable to accomodate further requests for the metar command. `Err: MaxLimitReached`")
                
                    elif response.status == 404:
                        await ctx.send(f"Uhhh {ctx.message.author.name}, I could not find that ICAO Code. Are you sure that ICAO code matches an airport ICAO? :face_with_monocle: `Err: {response.status} response code` ")
                
                    else:
                        await ctx.send(f"Ohhh I hate this.... :triumph: I got an error. `Err: {response.status} response code`")
    @Metar.error
    async def Metar_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Hold up! :face_with_monocle: You need to enter an ICAO code to get Metar.")
            
    #TAF command API
    @commands.command(description = "This command returns metar for the specified ICAO code and tries to decode it. Simply use `?taf` followed by the ICAO code and you shall recieve the TAF information for that airport... hopefully.", brief = "Returns TAF for the specified ICAO")
    async def TAF(self, ctx,*,icao_random = ""):
        icao = icao_random.upper()

        url = f"https://api.checkwx.com/taf/{icao}"
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                headers = {"X-API-Key": "MYAPI"}
                async with cs.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data["results"] == 1:
                            await ctx.send("Finding.....", delete_after = 1.0)
                            data_original = data["data"]
                            formatted_data = str(data_original)[2:-2]
                            
                            embed = discord.Embed(title = f"TAF Information", colour = discord.Colour(0xff0000), timestamp = datetime.utcnow())
                            embed.add_field(inline=False, name=f"{icao} TAF:", value=formatted_data)
                            await ctx.send(embed=embed)
          
                        else:
                            await ctx.send(f"Uhhh {ctx.message.author.display_name}, I could not find that ICAO Code. Are you sure that ICAO code matches an airport ICAO? :face_with_monocle: `Err: InvalidICAOCode` ")

                    elif response.status == 401:
                        await ctx.send("This doesn't happen often. Mufassil kindly look into this. `Err:InvalidKey`")
            
                    elif response.status == 429:
                        await ctx.send("If you see this, it's an error unfortunately. This means the bot is unable to accomodate further requests for the metar command. `Err: MaxLimitReached`")
            
                    elif response.status == 404:
                        await ctx.send(f"Uhhh {ctx.message.author.display_name}, I could not find that ICAO Code. Are you sure that ICAO code matches an airport ICAO? :face_with_monocle: `Err: {response.status} response code` ")
            
                    else:
                        await ctx.send(f"Ohhh I hate this.... :triumph: I got an error. `Err: {response.status} response code`")
    @TAF.error
    async def TAF_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Hold up! :face_with_monocle: You need to enter an ICAO code to get TAF.")



    #vatsim command
    @commands.command(description = "This command returns VATSIM Member Information. Simply use `?vatsim` and the bot will ask you further questions.")
    async def VATSIM(self, ctx):

        await ctx.trigger_typing()
        ask_vatid_message = await ctx.send(f"Hello {ctx.message.author.display_name}, what's the VATSIM ID? Kindly make sure it's only numbers nothing else, reply back to me within **15** seconds.")
  
        try:
            get_vatid_message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 15.0)
            get_vatid = int(get_vatid_message.content)
        except asyncio.TimeoutError:
            await ask_vatid_message.delete()
            await ctx.send("Uh no, your 15 seconds are up, no worries run me again **with** VATSIM ID handy.")
  
        else:
            url = f"https://api.vatsim.net/api/ratings/{get_vatid}"
            await ctx.trigger_typing()
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as response:
                    if response.status == 200:
                        ask_option_message = await ctx.send(f"Alright the VATSIM ID exists within VATSIM Database, let me know if you want me to get 'VATSIM Certificate Information' for the CID for example like current rating, region, division and etc (Option 1), or do you want me to get VATSIM ATC Rating hours for the CID (Option 2) or finally, get the last filed flight plan for the CID (Option 3) Reply back with numbers only (1, 2 or 3) within **35** seconds. Remember I am a bot :robot: I will only understand what I expect.")

                        try:
                            get_option_message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 35)
                            get_option = get_option_message.content
            
                        except asyncio.TimeoutError:
                            await ctx.trigger_typing()
                            await ctx.send("Hmmm, you did not get me the option within the required time frame, it's alright make up your mind and run the command again. :slight_smile:  ")
                            await ask_option_message.delete()
            
                        else:
                            if get_option == "1":
                                await ctx.trigger_typing()
                
                                data = await response.json()
                  
                                if data["rating"] == 0:
                                    data["rating"] = "Account Disabled"
                            
                                elif data["rating"] == -1:
                                    data["rating"] = "Inactive account"

                                elif data["rating"] == 1:
                                    data["rating"] = "Pilot/Observer (OBS)"

                                elif data["rating"] == 2:
                                    data["rating"] = "Tower Trainee (S1)"

                                elif data["rating"] == 3:
                                    data["rating"] = "Tower Controller (S2)"

                                elif data["rating"] == 4:
                                    data["rating"] = "TMA Controller (S3)"

                                elif data["rating"] == 5:
                                    data["rating"] = "Enroute Controller (C1)"

                                elif data["rating"] == 7:
                                    data["rating"] = "Senior Enroute Controller (C3)"

                                elif data["rating"] == 8:
                                    data["rating"] = "Instructor (I1)"

                                elif data["rating"] == 10:
                                    data["rating"] = "Senior Instructor (I3)"

                                elif data["rating"] == 11:
                                    data["rating"] = "Supervisor (SUP)"

                                elif data["rating"] == 12: 
                                    data["rating"] = "Administrator (ADM)"
                                    
                                else:
                                    data["rating"] = "This rating did not exist according to Mufassil....\n would you ask him?"
                            
                                if data["pilotrating"] == 0:
                                    data["pilotrating"] = "P0"

                                elif data["pilotrating"] == 1:
                                    data["pilotrating"] = "P1"

                                elif data["pilotrating"] == 3:
                                    data["pilotrating"] = "P2"
                                    
                                elif data["pilotrating"] == 7:
                                    data["pilotrating"] = "P3"
                                    
                                elif data["pilotrating"] == 15:
                                    data["pilotrating"] = "P4"
                                    
                                if data["subdivision"] == "":
                                    data["subdivision"] = "None"
                                    
                                if data["lastratingchange"] == None:
                                    data["lastratingchange"] = "No time found in"

                                save_t_lastchange = data["lastratingchange"]
                                save_t_regdate = data["reg_date"]
                                remove_t_lastchange = save_t_lastchange.replace('T', ' ')
                                remove_t_regdate = save_t_regdate.replace('T', ' ')
                                add_utc_lastchange = remove_t_lastchange + " UTC"
                                add_utc_regdate = remove_t_regdate + " UTC"
                            

                                embed = discord.Embed(title = "VATSIM Member Information", colour = discord.Colour(0xff0000),timestamp = datetime.utcnow())
                                embed.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.display_name}")
                                embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/753269447166263296/852237933079167016/Vatsim-social_icon.thumb.png.e9bdf49928c9bd5327f08245a68d8304.png")
                                    
                                embed.add_field(inline=False, name="Member CID:", value=data["id"])
                                embed.add_field(inline=False, name="Member ATC Rating:", value=data["rating"])
                                embed.add_field(inline=False, name="Member Pilot Rating:", value=data["pilotrating"])
                                embed.add_field(inline=False, name="Member Region:", value=data["region"])
                                embed.add_field(inline=False, name="Member Division:", value=data["division"])
                                embed.add_field(inline=False, name="Member Subdivision/vACC:", value=data["subdivision"])
                                embed.add_field(inline=False, name="Member Last Rating Change:", value=add_utc_lastchange)
                                embed.add_field(inline=False, name="Member Registeration Date:", value=add_utc_regdate)
                                    
                                await ctx.send(embed=embed)
              
                            #vatsim hours option
                            elif get_option == "2":
                
                                url2 = f"https://api.vatsim.net/api/ratings/{get_vatid}/rating_times/"
                                await ctx.trigger_typing()
                                async with aiohttp.ClientSession() as cs:
                                    async with cs.get(url2) as response2:

                                        data2 = await response2.json()

                                        embed = discord.Embed(title = f"Time spent online by VATSIM member {get_vatid}", colour = discord.Colour(0xff0000),timestamp = datetime.utcnow())
                                        embed.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.display_name}")
                                        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/753269447166263296/852237933079167016/Vatsim-social_icon.thumb.png.e9bdf49928c9bd5327f08245a68d8304.png")
                                        embed.add_field(inline=False, name="Hours on S1 Rating:", value=data2["s1"])
                                        embed.add_field(inline=False, name="Hours on S2 Rating:", value=data2["s2"])
                                        embed.add_field(inline=False, name="Hours on S3 Rating:", value=data2["s3"])
                                        embed.add_field(inline=False, name="Hours on C1 Rating:", value=data2["c1"])
                                        embed.add_field(inline=False, name="Hours on C3 Rating:", value=data2["c3"])
                                        embed.add_field(inline=False, name="Hours on I1 Rating:", value=data2["i1"])
                                        embed.add_field(inline=False, name="Hours on I3 Rating:", value=data2["i3"])
                                        embed.add_field(inline=False, name="Total Pilot Hours:", value=data2["pilot"])
                                        embed.add_field(inline=False, name="Total ATC Hours:", value=data2["atc"])
                                        await ctx.send(embed=embed)
                            
                            #vatsim fpl
                            elif get_option == "3":        
                                
                                url3 = f"https://api.vatsim.net/api/ratings/{get_vatid}/flight_plans/"
                                await ctx.trigger_typing()
                                async with aiohttp.ClientSession() as cs:
                                    async with cs.get(url3) as response3:

                                        data3 = await response3.json()
                                        if data3['count'] != 0:

                                            save_t_lastchange = data3['results'][0]['filed']
                                            remove_t_lastchange = save_t_lastchange.replace('T', ' ')

                                            embed = discord.Embed(title = f"Last Flight Plan Filed By VATSIM Member {get_vatid}",colour = discord.Colour(0xff0000),timestamp = datetime.utcnow())
                                            embed.set_footer(icon_url= ctx.message.author.avatar_url, text= f"Information requested by {ctx.message.author.display_name}")
                                            embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/753269447166263296/852237933079167016/Vatsim-social_icon.thumb.png.e9bdf49928c9bd5327f08245a68d8304.png")
                                            embed.add_field(inline=False, name="Callsign:", value=data3['results'][0]['callsign'])
                                            embed.add_field(inline=False, name="Flight Rules:", value=data3['results'][0]['flight_type'])
                                            embed.add_field(inline=False, name="Aircraft Details:", value=data3['results'][0]['aircraft'])
                                            embed.add_field(inline=False, name="Departure Airport ICAO:", value=data3['results'][0]['dep'])
                                            embed.add_field(inline=False, name="Arrival Airport ICAO:", value=data3['results'][0]['arr'])
                                            embed.add_field(inline=False, name="Filed Cruising Altitude:", value=data3['results'][0]['altitude'])
                                            embed.add_field(inline=False, name="Filed Cruising Speed:", value=data3['results'][0]['cruisespeed']+ " knots")
                                            embed.add_field(inline=False, name="Enroute Flight Time:", value=str(data3['results'][0]['hrsenroute'])+ " hour(s) " +str(data3['results'][0]['minenroute'])+ " minute(s)")
                                            embed.add_field(inline=False, name="Flight Plan Filed On:", value=remove_t_lastchange + " UTC")
                                            embed.add_field(inline=False, name=f"Total Flight Plans Filed on VATSIM CID {get_vatid}", value=data3['count'])
                                            await ctx.send(embed=embed)

                                        else:
                                            await ctx.send(f"Sorry I could not find any filed flight plans for VATSIM CID {get_vatid}")

                            
                            else:
                                await ctx.trigger_typing()
                                await ctx.send("I said, I won't understand anything other than what I expect. I was expecting a number 1, 2 or 3. Simple try again!")    


                    elif response.status == 404:
                        await ctx.send(f"Uhhh {ctx.message.author.display_name}, I could not find that ID. Are you sure that vatsim id is a real person? :face_with_monocle: `Err: {response.status} response code` ")
                    else:
                        await ctx.send(f"Ohhh I hate this.... :triumph: I got an error. `Err: {response.status} response code`")

    @VATSIM.error
    async def VATSIM_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send("Wait... I don't think that's a correct VATSIM ID. Make sure it's only numbers and nothing else.")

    @commands.command(description = "This command will return VATSIM member hours on a specific position from a start date that was mentioned. Use the command `?vatsimhours` and the bot will ask you further questions. ")
    async def vatsimhours(self, ctx):
        await ctx.trigger_typing()
        ask_vatid_message = await ctx.send(f"{ctx.message.author.display_name} hello, what's your VATSIM ID? Kindly make sure it's only numbers nothing else, reply back to me within **20** seconds.")

        try:
            get_vatid_message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 20.0)
            get_vatid = int(get_vatid_message.content)
        except asyncio.TimeoutError:
            await ask_vatid_message.delete()
            await ctx.trigger_typing()
            await ctx.send("Uh no, your 20 seconds are up, no worries run me again **with** your VATSIM ID handy.")
        else:
            
            await ctx.trigger_typing()
            ask_position_message = await ctx.send("Gib me the position callsign. i.e 'VNKT_TWR' without quotation marks. Reply back within **20** seconds. ")

            try:
                get_position_message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 20.0)
                get_position = get_position_message.content
            except asyncio.TimeoutError:
                await ask_vatid_message.delete()
                await ask_position_message.delete()
                await ctx.trigger_typing()
                await ctx.send("Uh no, your 20 seconds are up, no worries run me again **with** the position you want to check.")
            else:
                
                await ctx.trigger_typing()
                ask_start_time_message = await ctx.send("Alright finally the start time i.e '2021-01-01' but without the quotation marks. Format is YYYY-MM-DD. Reply back within **20** seconds.")
                
                try:
                    get_start_time_message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 20.0)
                    get_start_time = get_start_time_message.content
                except asyncio.TimeoutError:
                    ask_vatid_message.delete()
                    ask_position_message.delete()
                    ask_start_time_message.delete()
                    await ctx.trigger_typing()
                    await ctx.send("Uh no, your 20 seconds are up, no worries run me again **with** the start time.")
                else:

                    url = f"https://api.vatsim.net/api/ratings/{get_vatid}/atcsessions/{get_position}/?start={get_start_time}"
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(url) as response:
                            if response.status == 200:
                                data = await response.json()

                                if data['count'] != 0:

                                    find = 0.0
                                    total = 0.0
                                    for results in data['results']:
                                        find = float(results['minutes_on_callsign'])
                                        convert = find / 60 
                                        total = total + convert
                                        #now = results['end']
                                        
                                        # replace_than = then.replace('T', ' ')
                                        # replace_now = now.replace('T', ' ')
                                        
                                        # checker_than = datetime.strptime(replace_than, '%Y-%m-%d %H:%M:%S')
                                        # checker_now = datetime.strptime(replace_now, '%Y-%m-%d %H:%M:%S')
                                        # difference = checker_now - checker_than
                                        # find = (difference.seconds / 3600)

                                    hours_ = str(timedelta(hours=total))[:-9]
                                    hours = hours_.replace(':', '.')

                                    await ctx.trigger_typing()
                                    embed = discord.Embed(title = f"{get_vatid} Hours On {get_position} from {get_start_time}", colour=discord.Colour(0xff0000), timestamp = datetime.utcnow())
                                    embed.set_footer(text=f"Requested by {ctx.message.author.name}", icon_url=ctx.author.avatar_url)
                                    embed.add_field(inline=False, name="Hours controlled:", value=hours+ " Hour(s) ")
                                    await ctx.send(embed=embed)
                                    await ctx.message.delete()
                                    await ask_vatid_message.delete()
                                    await ask_position_message.delete()
                                    await ask_start_time_message.delete()
                                    await get_vatid_message.delete()
                                    await get_position_message.delete()
                                    await get_start_time_message.delete()

                                else:
                                    await ctx.trigger_typing()
                                    await ctx.send(f"Nope {get_vatid} has not controlled {get_position}")
                            
                            elif response.status == 404:
                                await ctx.trigger_typing()
                                await ctx.send(f"Uhhh {ctx.message.author.name}, I could not find that ID. Are you sure that vatsim id is a real person? :face_with_monocle: `Err: {response.status} response code` ")

                            elif response.status == 500:
                                await ctx.trigger_typing()
                                await ctx.send("I was programmed to think that if this happens, it means that you entered a date which is in future. What do you think I am, time machine? Or you did not follow the correct date format. But the first one was more funny right? :sweat_smile: ")
    @vatsimhours.error
    async def vatsimhours_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send("Wait... I don't think that's a correct VATSIM ID. Make sure it's only numbers and nothing else.")



def setup(bot):
    bot.add_cog(UserCommands(bot))


                    
