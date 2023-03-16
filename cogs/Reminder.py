from discord.ext import commands
from lib.db import db
from datetime import datetime
import discord
import asyncio



class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remind(self, ctx):
        await ctx.trigger_typing()
        ask_remind_message = await ctx.send("Alright to setup the remind command, reply back with the complete reminder message. Don't type anything else just the reminder message it self. You have **30** seconds to type it.")

        try:
            get_remind_message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel, timeout = 30.0 )
            remind_message = get_remind_message.content
        
        except asyncio.TimeoutError:
            await ask_remind_message.delete()
            await ctx.send(f"{ctx.message.author.display_name}, time's up! Try again but this time actually remember what you need to be reminded about. ")
        
        else:
            ask_remind_time = await ctx.send("Alright I have the reminder message, when do you need me to remind you? Make sure it's only numbers (can be float values as well) and they will be in hours be default (you can't change that). For example if you need me to remind you in 1 hour just type **1** or if you need me to remind you in 30 minutes type **0.5**. Reply back within **20** seconds.")

            try:
                get_remind_time = await self.bot.wait_for("message", check=lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel, timeout = 20.0 )
                remind_time_float = float(get_remind_time.content)
                remind_time = (remind_time_float*3600)
            
            except asyncio.TimeoutError:
                await ask_remind_message.delete()
                await ask_remind_time.delete()
                await ctx.send(f"{ctx.message.author.display_name}, time's up! Try again, but this time let me know when you need to be reminded.")
            
            else:
                stby = await ctx.send("Standby.... let me add that in my database so i don't forget it myself :sweat_smile: ")
                db.execute("INSERT INTO reminder (UserID, Remind_Message, Remind_Time) VALUES (?,?,?)", ctx.message.author.id, remind_message, remind_time)
                await asyncio.sleep(1.5)
                await stby.edit(content = f"{ctx.message.author.mention} Added, you will be reminded in {remind_time_float} hour(s), you will get the reminder in your DM make sure it's open so I can send it.")
                await ctx.message.delete()
                await ask_remind_time.delete()
                await ask_remind_message.delete()
                await get_remind_time.delete()
                await get_remind_message.delete()
                await asyncio.sleep(remind_time)

                embed = discord.Embed(title = "Reminder!", colour=discord.Color(0xff0000),timestamp=datetime.utcnow())
                embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                embed.add_field(inline=False, name="Why?", value=f"You asked me to remind you in {ctx.message.guild.name} in {remind_time_float} hour(s) about the message below.")
                embed.add_field(inline=False, name = "Reminder Message:", value=remind_message)
                await ctx.message.author.send(embed=embed)
                db.execute("DELETE FROM reminder WHERE UserID = ?", ctx.message.author.id)


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def training(self, ctx):
        await ctx.trigger_typing()

        ask_member_id_message = await ctx.send("Alright I need the member ID who I will remind. Make sure it's only number (integer). Reply back within **20** seconds.")
        
        try:
            get_member_id = await self.bot.wait_for("message", check=lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel, timeout = 20.0)
            convert_member_id = int(get_member_id.content)
            member = self.bot.get_user(convert_member_id)

        except asyncio.TimeoutError:
            await ask_member_id_message.delete()
            await ctx.send("Uh oh. I could not get the member ID in time. :pensive:")
        
        else:

            ask_session_time_message = await ctx.send("Alright to setup the reminder command, reply back with the session time to display it to user (in utc obviously). Don't type anything else just the utc time it self. For example '30th June, 2021 at 1000z'. You have **20** seconds to type it.")

            try:
                get_session_time = await self.bot.wait_for("message", check=lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel, timeout = 20.0)
                session_time = get_session_time.content
            
            except asyncio.TimeoutError:
                await ask_member_id_message.delete()
                await ask_session_time_message.delete()
                await ctx.send(f"{ctx.message.author.display_name}, time's up! Try again but this time actually remember when is {member.display_name}'s session.")
            
            else:
                ask_session_mentor_message = await ctx.send(f"Alright I have the session time, who will mentor {member.display_name}? Make sure you only reply back as text message. Reply back within **20** seconds.")

                try:
                    get_session_mentor = await self.bot.wait_for("message", check=lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel, timeout = 20.0 )
                    session_mentor = get_session_mentor.content
                
                except asyncio.TimeoutError:
                    await ask_member_id_message.delete()
                    await ask_session_time_message.delete()
                    await ask_session_mentor_message.delete()
                    await ctx.send(f"{ctx.message.author.display_name}, time's up! Try again but this time let me know who will mentor {member.display_name}")
                
                else:

                    ask_remind_time = await ctx.send("Alright I have the reminder message, when do you need me to remind you? Make sure it's only numbers (can be float values as well) and they will be in hours be default (you can't change that). For example if you need me to remind you in 1 hour just type **1** or if you need me to remind you in 30 minutes type **0.5**. Reply back within **20** seconds.")

                    try:
                        get_remind_time = await self.bot.wait_for("message", check=lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel, timeout = 20.0 )
                        remind_time_float = float(get_remind_time.content)
                        remind_time = (remind_time_float*3600)
                    
                    except asyncio.TimeoutError:
                        await ask_member_id_message.delete()
                        await ask_session_time_message.delete()
                        await ask_session_mentor_message.delete()
                        await ask_remind_time.delete()
                        await ctx.send(f"{ctx.message.author.display_name}, time's up! Try again, but this let me know when you need {member.display_name} to be reminded.")

                    else:

                        stby = await ctx.send("Standby.... let me add that in my database so i don't forget it myself :sweat_smile: ")
                        db.execute("INSERT INTO reminder (UserID, Remind_Time) VALUES (?,?)", member.id, remind_time)
                        await asyncio.sleep(1.0)
                        await stby.edit(content = f"{ctx.message.author.mention} added, {member.display_name} will be reminded in {remind_time_float} hour(s), member will get the reminder in DM make sure they have it open so I can send it.")
                        await ctx.message.delete()
                        await ask_member_id_message.delete()
                        await ask_remind_time.delete()
                        await ask_session_mentor_message.delete()
                        await get_remind_time.delete()
                        await get_member_id.delete()
                        await get_session_time.delete()
                        await ask_session_time_message.delete()
                        await get_session_mentor.delete()
                        await asyncio.sleep(remind_time)

                        embed = discord.Embed(title = "Training Session Reminder!", colour=discord.Color(0xff0000),timestamp=datetime.utcnow())
                        embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
                        embed.add_field(inline=False, name="Why?", value="You have a training session scheduled.")
                        embed.add_field(inline=False, name = "Session Time:", value=session_time)
                        embed.add_field(inline=False, name = "Session Mentor:", value=session_mentor)
                        embed.add_field(inline=False, name = "Session Venue:", value="Session will be held in Nepal vACC Discord Server as always.")
                        embed.add_field(inline=False, name="Any problem?", value="If you cannot attend the session or have any questions, feel free to reply down below and I will convey your message to the Mentor/vACC Staff.")
                        db.execute("DELETE FROM reminder WHERE UserID = ?", member.id)
                        await member.send(embed=embed)
                        
    
    @training.error
    async def training_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send("Uh ohh, I don't think that's a correct member ID.")
    



def setup(bot):
    bot.add_cog(Reminder(bot))