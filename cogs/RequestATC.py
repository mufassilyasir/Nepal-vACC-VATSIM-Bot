import discord
from discord.ext import commands
import asyncio
from datetime import datetime
from lib.db import db
from dotenv import load_dotenv
import os

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

OPTIONS = {
    "✅" : 0,
    "❎" : 1 
}


class RequestATC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Request ATC DM Command
    @commands.command(description = "This command allows members to request ATC in Nepal vACC. All the controllers with the role <@&850069042160992276> will receive a DM from the Bot with all details. Use the command `?requestatc` in channel <#850055844083007488> and the bot will further ask you some questions before it sends the DM. ")
    async def RequestATC(self, ctx):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )
        
        try:    
            user_exists = db.field("SELECT bool FROM requestatc WHERE UserID = ?", ctx.message.author.id)
        except:
            pass
        else:
            if user_exists != "True":

                ask_icao_code_message = await ctx.send(f"Hi {ctx.message.author.mention}! Want to request ATC? You have come to the right place. Please be aware while using the command, you will send a DM to the Nepal vACC controllers with the role 'Request ATC'.\n  :no_entry: Abusing this command  will have consequences that will be enforced by the Nepal vACC Staff! \n Before you reply to me, please ensure the details are correct & will only be valid for Nepal vACC. \n ``` NOTE:  This will not guarantee that there will be controller(s) for you, but you might get controller(s) if they are free to control.``` Please reply back with **only** the ICAO code of the airport that you want to request ATC for within **40** seconds.")

                try:
                    icao_code_message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 50.0)
                    icao_something = icao_code_message.content
                    icao_code = icao_something.upper()

                except asyncio.TimeoutError:
                    await ask_icao_code_message.delete()
                    await ctx.send("You must reply to me within **40** seconds. :(")

                else:

                    ask_timings_message = await ctx.send("Got the ICAO code! Now what time do you require controller(s) to be online at :timer: ? It must be an understandable format, it must include the date and month and especially the time in zulu/UTC. \n For example: **29th June at 1000z till 1100z** Please reply within **40** seconds.")

                    try:
                        timings_message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 35.0)
                        timing_something = timings_message.content
                        timings = timing_something.upper()

                    except asyncio.TimeoutError:
                        await ask_timings_message.delete()
                        await ask_icao_code_message.delete()
                        await ctx.send("You must reply to me within **40** seconds. Please run the command again when ready.")
                    
                    else:
                        embed = discord.Embed(title = "ATC Request Details:", colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                        embed.set_footer(text=f"Requested by {ctx.message.author.display_name}", icon_url=ctx.author.avatar_url)
                        embed.add_field(inline=False, name="Requested Airport ICAO Code:", value=f"{icao_code}")
                        embed.add_field(inline=False, name="Requested Timings:", value=f"{timings}")
                        embed.add_field(inline=False, name="Are the details correct and ready to send to the controllers?", value="React with ✅ emoji to send the request to controller(s) if all details are correct. \n Or react with ❎ to cancel the request and run the command again. ")
                        msg = await ctx.send(embed=embed)
                        for emoji in list(OPTIONS.keys()):
                            await msg.add_reaction(emoji)


                        try:
                            reactions, _= await self.bot.wait_for("reaction_add", timeout = 20.0, check=_check)
                        except asyncio.TimeoutError:
                            await msg.delete()
                            await ctx.message.delete()
                            await ask_icao_code_message.delete()
                            await ask_timings_message.delete()
                            await ctx.send("Time's up. Run the command again, if still interested.")

                        else:
                            reaction = OPTIONS[reactions.emoji]
                            
                            if reaction == 1:
                                await msg.delete()
                                await ctx.message.delete()
                                await ask_icao_code_message.delete()
                                await ask_timings_message.delete()
                                await ctx.send(f"{ctx.message.author.display_name} I have cancelled ❎ your 'request ATC' request. If something was incorrect you may run the command and try sending request again with correct details. :slight_smile: ")

                            elif reaction == 0:
                                await ctx.message.delete()
                                await ask_icao_code_message.delete()
                                await ask_timings_message.delete()
                                await ctx.send(f"{ctx.message.author.display_name} I have sent :white_check_mark: your 'request ATC' request to the controllers in DM, with the role  <@&850069042160992276>.")
                                await msg.clear_reactions()
                                value = "True"
                                db.execute("INSERT INTO requestatc (UserID, bool) VALUES (?, ?)", ctx.message.author.id, value)
                                count = 0
                                role = discord.utils.get(ctx.message.guild.roles, id = 850069042160992276)
                                for member in ctx.guild.members:
                                    if role in member.roles:
                                        count = count + 1
                                        try:
                                            embed1 = discord.Embed(title = f"'Request ATC' request!",colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                            embed1.add_field(inline=False, name="Request ATC By:", value=f"Controller(s) are requested by member {ctx.message.author.display_name}")
                                            embed1.add_field(inline=False, name="Requested Airport ICAO Code:", value=f"{icao_code}")
                                            embed1.add_field(inline=False, name="Requested Timings:", value=f"{timings}")
                                            embed1.add_field(inline=False, name="Why did I got the DM?", value=f"You have recieved this request from {ctx.message.guild.name} since you reacted to the 'Request ATC' role. You may at anytime unreact to stop receiving 'Request ATC' requests from channel <#850297428234338334> in the server.")
                                            await member.send(embed=embed1)
                
                                        except:
                                            pass

                                        else:
                                
                                            embed2 = discord.Embed(title = "'Request ATC' command usage!", colour = discord.Color(0xff0000),timestamp = datetime.utcnow())
                                            embed2.add_field(inline=False, name="Request ATC command by:", value=f"Controller(s) are requested by member {ctx.message.author.display_name}")
                                            embed2.add_field(inline=False, name="Requested Airport ICAO Code:", value=f"{icao_code}")
                                            embed2.add_field(inline=False, name="Requested Timings:", value=f"{timings}")
                                            embed2.add_field(inline=False, name="How many controllers got the DM?", value=f"{count}")
                                            embed2.add_field(inline=False, name="Why do I see this message?", value=f"You see this because you probably are an Administrator :slight_frown: But really because someone recieved a DM.")
                                            
                                channel = self.bot.get_channel(LOG_CHANNEL_ID)
                                await channel.send(embed=embed2)
                                await asyncio.sleep(86400)
                                db.execute("DELETE FROM requestatc WHERE UserID = ?", ctx.message.author.id)
            else:
                await ctx.send(f"{ctx.message.author.display_name}, you can only request ATC services once in **24 hours**. Please be patient someone will show up.")


def setup(bot):
    bot.add_cog(RequestATC(bot))