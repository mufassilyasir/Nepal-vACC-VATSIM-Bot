from operator import mod
from discord.ext import commands
from datetime import datetime, timedelta
from better_profanity import profanity
from dotenv import load_dotenv
from typing import Optional

from lib.db import db
import discord
import asyncio
import os

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))


profanity.load_censor_words_from_file("./data/profanity.txt")

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if profanity.contains_profanity(message.content):
                await message.delete()
                mod_channel = self.bot.get_channel(767052402775162892)
                if "nitro" not in message.content.lower():
                    await message.channel.send(f"{message.author.mention}, Nepal vACC Discord Server does not allow the use of curse words. If you believe this was a mistake, please contact Nepal vACC Staff. :slight_smile: ")
                    embed = discord.Embed(title = "Curse Word Used!", description = f"{message.author.mention} used a word that was found in profanity database. \n **Channel:** {message.channel.mention}, **Message that was deleted:** {message.content}",colour=discord.Colour(0xff0000), timestamp = datetime.utcnow() )
                    await mod_channel.send(embed=embed)
                else:
                    await mod_channel.send(f'Use of word "Nitro" in {message.channel.mention} by {message.author.mention} <@&766652488974991390>')

        
        if "news" in message.channel.type:
            await discord.Message.publish(message)
    
    async def mute_member(self, message, target, actual_hours, reason):
    
        log_channel = self.bot.get_channel(767052402775162892)
        guild = self.bot.get_guild(765542639717974026)
        mute_role = discord.utils.get(guild.roles, id = 856520973956415539)

 	
        if not mute_role in target.roles:				
            if message.guild.me.top_role.position > target.top_role.position:				
                
                role_ids = ",".join([str(r.id) for r in target.roles])
                
                end_time = datetime.utcnow() + timedelta(seconds=actual_hours) if actual_hours else None

                
                db.execute("INSERT INTO mutes VALUES (?, ?, ?)",
                            target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())

                await target.edit(roles=[mute_role])

                
                embed = discord.Embed(title="Member Muted!",colour=discord.Color(0xff0000),timestamp=datetime.utcnow())
                embed.set_thumbnail(url=target.avatar_url)

                if actual_hours != None:
                    converted_hours = actual_hours // 3600
                else:
                    converted_hours = None
                
                fields = [("Member Name:", target.mention, False),
                            ("Moderator:", message.author.mention, False),
                            ("Time Period:", f"{converted_hours:,} hour(s)" if converted_hours else "Indefinite", False),
                            ("Reason:", reason, False)]

                
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await log_channel.send(embed=embed)
                embed1 = discord.Embed(title = "You have been muted! :mute:",colour=discord.Color(0xff0000),timestamp=datetime.utcnow())
                embed1.set_footer(text=f"Mute Notification for {target.display_name}", icon_url=target.avatar_url)
                embed1.add_field(inline=False, name="Description:", value="You were muted in VATSIM Nepal vACC Server. Your permission to read, see & type in all channels in VATSIM Nepal vACC discord server has been revoked.")
                embed1.add_field(inline=False, name="Mute Time Period:", value= f"{converted_hours}, hour(s)" if converted_hours else "Indefinite")
                embed1.add_field(inline=False, name="Reason:", value=reason)
                try:
                    await target.send(embed=embed1)
                except:
                    pass
            
            else:
                await message.channel.send("Hold up! Are you trying to kick yourself or someone who has a higher role than me? :face_with_monocle: Grow up! `Err: Permissions not sufficient`")   
        else:
            pass    
    
                
	
    @commands.command(name="mute")
    @commands.has_any_role(766652488974991390, 804331016168276028)
	
    async def mute_command(self, ctx, target: discord.Member, hours: Optional[float], *,reason: Optional[str] = "No reason provided by the vACC Staff."):
		
        mute_role = discord.utils.get(ctx.guild.roles, id = 856520973956415539)

        if target == None:
            await ctx.send("Hey you need to mention the member at least. `Err:MissingRequiredArgument`")
	
        
        elif not mute_role in target.roles:
            if hours != None:
                actual_hours = hours*3600
            else:
                actual_hours = None
            await self.mute_member(ctx.message, target, actual_hours, reason)
			
            await ctx.message.delete()
            await ctx.send(f"{ctx.message.author.mention} I have muted the member :wink: ")
			
            await asyncio.sleep(actual_hours)			
            await self.unmute_member(ctx.guild, target)
        else:
            await ctx.send(f"{ctx.message.author.mention} Uhhh, I have checked and the member already has the <@&856520973956415539> Role.... What do you want me to do? What were you thinking?")

    async def unmute_member(self, guild, target, *, reason="Mute time period ended."):
        log_channel = self.bot.get_channel(767052402775162892)
        guild = self.bot.get_guild(765542639717974026)
        mute_role = discord.utils.get(guild.roles, id = 856520973956415539)

        
        if mute_role in target.roles:
        
            role_ids = db.field("SELECT RoleIDs FROM mutes WHERE UserID = ?", target.id)
            roles = [guild.get_role(int(id_)) for id_ in role_ids.split(",") if len(id_)]

            db.execute("DELETE FROM mutes WHERE UserID = ?", target.id)

            await target.edit(roles=roles)

            embed = discord.Embed(title="Member Unmuted!",colour=discord.Color(0xff0000),timestamp=datetime.utcnow())
            embed.set_thumbnail(url=target.avatar_url)

            fields = [("Member", target.mention, False),
                    ("Reason", reason, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            log_channel = self.bot.get_channel(767052402775162892)
            await log_channel.send(embed=embed)
        else:
            pass

    
    @commands.command(name="unmute")
    @commands.has_any_role(766652488974991390, 804331016168276028)
    async def unmute_command(self, ctx, target: discord.Member, *, reason: Optional[str] = "No reason provided."):

        mute_role = discord.utils.get(ctx.guild.roles, id = 856520973956415539)
        
        if target == None:
            await ctx.send("Hey you need to mention the member at least. `Err:MissingRequiredArgument`")
        elif mute_role in target.roles:
            await self.unmute_member(ctx.guild, target, reason=reason)
            await ctx.message.delete()
            await ctx.send(f"{ctx.message.author.mention} I have unmuted the member :wink: ")
        elif not mute_role in target.roles:
            await ctx.send(f"{ctx.message.author.mention} Uhhh, I have checked and the member does not have the <@&856520973956415539> Role.... What do you want me to do? What were you thinking?")


    #Announcement Command
    @commands.command(hidden = True)
    @commands.has_any_role(766652488974991390, 804331016168276028)
    async def Announcement(self, ctx):
        ask_channel_name = await ctx.send("Hmmm, me again? :expressionless: Bots will take over the world, lazy humans. Alright human, in which channel should this so called 'announcement' will be sent in? Reply back to me within **20 seconds.** Make sure the channel is **MENTIONED** otherwise I won't send!")

        try:
            channel_name = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 20.0)
        
        except asyncio.TimeoutError:
            await ask_channel_name.delete()
            await ctx.send("I think I said, reply me within 20 seconds :triumph:, I am a bot and hence **punctual**, human!")
        

        else:
            for channel in channel_name.channel_mentions:
                mentioned_channel_id = channel.id
            
            channel = self.bot.get_channel(mentioned_channel_id)
            ask_message = await ctx.send(f"Alright, what should I send in {channel.mention}? Hurry up you got **60** seconds to reply.")

            try:
                message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60.0)

            except asyncio.TimeoutError:
                await ask_message.delete()
                await ctx.send("If you don't have a message ready to send why call me? :unamused:  Woke me in the middle of night. Lemme sleep now! Or my mom will kick me out. :sleeping:  ")

            else:
                try:
                    await channel.send(f"{message.content}")
                except:
                    await ctx.send("Noooo... I could not send the announcement :pensive: maybe check my permissions? `Err:MissingPermissions`")
                else:
                    await ask_message.delete()
                    await message.delete()
                    await channel_name.delete()
                    await ask_channel_name.delete()
                    await ctx.message.delete()
                    await ctx.send(f"{ctx.message.author.mention} I have successfully posted the announcement")
                    channel = self.bot.get_channel(LOG_CHANNEL_ID)
                    embed = discord.Embed(Title = "**Announcement Sent**",colour=discord.Colour(0xff0000),description = f"Announcement command used in {ctx.message.channel.mention} by {ctx.message.author.mention}, was successfully posted", timestamp = datetime.utcnow())
                    await channel.send(embed=embed)
    @Announcement.error
    async def Announcement_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send("Are you sure the channel is mentioned?")

#Dm new one
    @commands.command(hidden = True)
    @commands.has_any_role(766652488974991390, 804331016168276028)
    async def DM(self, ctx, user: discord.Member):

        server_nick = user.display_name
        ask_message = await ctx.send(f"Oh we are sending Private messages now huh? :smirk: What should I send to {user.name} ? I will give you **15** seconds type it!")

        try:
            message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 15.0)

        except asyncio.TimeoutError:
            await ask_message.delete()
            await ctx.send("Time is up. Are you feeling ok? Should I call 911?")

        else:
            try:
                await user.send(f'Hi **{server_nick}**, Nepal vACC staff has asked me to send this message to you :smile: \n\n**"{message.content}"**')
            except:
                await ctx.send(f"Ooops :astonished: it seems that {user.name} has their DM's closed! `Err: DM NOT REACHABLE`")
            else:
                await ctx.message.delete()
                await message.delete()
                await ask_message.delete()
                await ctx.send(f"{ctx.message.author.mention} I have successfully sent the DM")
                channel = self.bot.get_channel(LOG_CHANNEL_ID)
                embed = discord.Embed(Title = "**DM Sent**",colour=discord.Colour(0xff0000),description = f"DM command used in {ctx.message.channel.mention} by {ctx.message.author.mention}, was successfully sent to {user.mention} with a message '{message.content}'", timestamp = datetime.utcnow())
                await channel.send(embed=embed)
    @DM.error
    async def DM_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Hmmm {ctx.message.author.name}, I need the person's ID or mention them to actually allow me to send them a DM.")

        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f"Oh no {ctx.message.author.name}. I could not find that user. :see_no_evil: `Err: MemberNotFound` ")

    #kick new one.
    @commands.command(hidden = True)
    @commands.has_permissions(kick_members = True)
    async def Kick(self, ctx, member: discord.Member,*, reason="*No reason was provided by the staff*"):
    
        display_reason = await ctx.send(f"You are trying to kick someone, I see, what will the reason be to kick {member.mention} will be? Tell me within **60** seconds or i will use the default reason.")
        
        try:
            reason_check = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60.0)
            reason = reason_check.content

        except asyncio.TimeoutError:
            await display_reason.delete()
            await ctx.send("Time is up. Told you this is not the way to solve things...")
        
        kick_dm = discord.Embed(title=f"Kicked from {ctx.message.guild.name}",colour=discord.Colour(0xff0000), description = f'Hi {member.name}, sorry to inform you but you have been kicked from {ctx.message.guild.name} reason being "{reason}" by Nepal vACC Staff Team. Please contact vACC Staff to appeal your case.')

        embed = discord.Embed(title="**Nepal vACC Contact Information**", colour=discord.Colour(0xff0000))
        embed.add_field(inline=False, name="To contact Nepal vACC Director", value="**Bikesh Devkota**\n Nepal vACC Director, ACCNPL1\n director_bikesh@nepalvacc.com")
        embed.add_field(inline=False, name="To contact Nepal vACC Deputy Director", value="**Resh B. Bhattarai**\n Nepal vACC Deputy Director, ACCNPL2\n deputy@nepalvacc.com")

        try:
            await member.send(embed=kick_dm)
            await member.send(embed=embed)
        except:
            await ctx.send(f"Ooops :astonished: it seems that {member.name} has their DM's closed! `Err: DM NOT REACHABLE`")
        
        else:
            await ctx.send(f"{ctx.message.author.name} DM to the member was sent successfully")
            channel = self.bot.get_channel(LOG_CHANNEL_ID)
            embed = discord.Embed(Title = '**DM Sent**',colour=discord.Colour(0xff0000),description = f"Kick command's module DM used in {ctx.message.channel.mention} by {ctx.message.author.mention}, was successfully sent to {member.name}, with a reason **{reason}** ", timestamp = datetime.utcnow())
            await channel.send(embed=embed)
        try:
            await member.kick(reason=reason)
        except:
            await ctx.send("Hold up! Are you trying to kick yourself or someone who has a higher role than me? :face_with_monocle: Grow up! `Err: Permissions not sufficient`")
        else:
            await ctx.send(f"{ctx.message.author.mention} you just **kicked** {member.name}, let's hope you did the right thing. :face_with_raised_eyebrow:")
            channel = self.bot.get_channel(LOG_CHANNEL_ID)
            embed = discord.Embed(Title = "**Member Kicked**",colour=discord.Colour(0xff0000),description = f"KICK command used in {ctx.message.channel.mention} by {ctx.message.author.mention}, successfully kicked {member.name}, with a reason '{reason}' ", timestamp = datetime.utcnow())
            await channel.send(embed=embed)
    @Kick.error
    async def Kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Alright Mr.Admin to kick the person you need to mention him like with the command? Here is an example `?kick @resh`")

    #ban new one.
    @commands.command(hidden = True)
    @commands.has_permissions(administrator = True)
    async def Ban(self, ctx, member: discord.Member,*, reason="*No reason was provided by the staff*"):
    
        display_reason = await ctx.send(f"You are trying to **Ban** someone, I see, what will the reason be to ban {member.mention} will be? Tell me within **60** seconds or i will use the default reason.")
        
        try:
            reason_check = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 60.0)
            reason = reason_check.content

        except asyncio.TimeoutError:
            await display_reason.delete()
            await ctx.send("Time is up. Told you this is not the way to solve things...")
        
        ban_dm = discord.Embed(title=f"Banned from {ctx.message.guild.name}",colour=discord.Colour(0xff0000), description = f'Hi {member.name}, sorry to inform you but you have been banned from {ctx.message.guild.name} reason being "{reason}" by Nepal vACC Staff Team. Please contact vACC Staff to appeal your case.')

        embed = discord.Embed(title="**Nepal vACC Contact Information**", colour=discord.Colour(0xff0000))
        embed.add_field(inline=False, name="To contact Nepal vACC Director", value="**Bikesh Devkota**\n Nepal vACC Director, ACCNPL1\n director_bikesh@nepalvacc.com")
        embed.add_field(inline=False, name="To contact Nepal vACC Deputy Director", value="**Resh B. Bhattarai**\n Nepal vACC Deputy Director, ACCNPL2\n deputy@nepalvacc.com")

        try:
            await member.send(embed=ban_dm)
            await member.send(embed=embed)
        except:
            await ctx.send(f"Ooops :astonished: it seems that {member.name} has their DM's closed! `Err: DM NOT REACHABLE`")
        
        else:
            await ctx.send(f"{ctx.message.author.name} DM to the member was sent successfully")
            channel = self.bot.get_channel(LOG_CHANNEL_ID)
            embed = discord.Embed(Title = '**DM Sent**',colour=discord.Colour(0xff0000),description = f"Ban command's module DM used in {ctx.message.channel.mention} by {ctx.message.author.mention}, was successfully sent to {member.name}, with a reason **{reason}** ", timestamp = datetime.utcnow())
            await channel.send(embed=embed)
        try:
            await member.ban(reason=reason)
        except:
            await ctx.send("Hold up! Are you trying to ban yourself or someone who has a higher role than me? :face_with_monocle: Grow up! `Err: Permissions not sufficient`")
        else:
            await ctx.send(f"{ctx.message.author.mention} you just **Banned** {member.name}, must be hard.")
            channel = self.bot.get_channel(LOG_CHANNEL_ID)
            embed = discord.Embed(Title = "**Member Banned**",colour=discord.Colour(0xff0000),description = f"Ban command used in {ctx.message.channel.mention} by {ctx.message.author.mention}, successfully banned {member.name}, with a reason '{reason}' ", timestamp = datetime.utcnow())
            await channel.send(embed=embed)
    @Ban.error
    async def Ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Alright Mr.Admin to ban the person you need to mention him like with the command? Here is an example `?ban @resh`")

    #delete messages command
    @commands.command(aliases = ["purge"], hidden = True)
    @commands.has_any_role(766652488974991390, 804331016168276028)
    async def Delete(self, ctx, amount: int):
        with ctx.channel.typing():
            try:
                deleted = await ctx.channel.purge(limit=amount+1)
            except:
                await ctx.send("Oh no. I got a dead end here. Cannot delete this message. `Err: DeleteMessageFailed`")
            else:
                await ctx.send(f"Woah I feel powerful :open_mouth: I have deleted {len(deleted)-1:,} message(s) *Lemme delete this one too*", delete_after = 5)
                channel = self.bot.get_channel(LOG_CHANNEL_ID)
                embed = discord.Embed(Title = "**Bulk Messages Deleted**",colour=discord.Colour(0xff0000),description = f"Delete messages command used in {ctx.message.channel.mention} by {ctx.message.author.mention}, successfully deleted {len(deleted)-1:,} message(s)", timestamp = datetime.utcnow())
                await channel.send(embed=embed)
    @Delete.error
    async def Delete_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Ahhh, you really need to tell me how many messages to delete. I basically won't **guess**. Example: `?purge 100`")

    
    @commands.command()
    @commands.has_any_role(766652488974991390, 804331016168276028)
    async def role_add_all(self, ctx, role: discord.Role):
        embed=discord.Embed(title = "Standby.... this will take time and won't stop until completed.",colour=discord.Color(0xff0000),timestamp = datetime.utcnow())
        stby = await ctx.send(embed=embed)
        for members in ctx.message.guild.members:
            if members.bot == False:
                await members.add_roles(role)
            else:
                pass
        embed1 = discord.Embed(title = "Added Role To All Members:", description = f"{role.mention} was added to all members in {ctx.guild.name}", colour=discord.Color(0xff0000),timestamp = datetime.utcnow())
        embed1.set_footer(text = f"Requested by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
        await stby.edit(embed=embed1)

    @role_add_all.error
    async def role_add_all_error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            await ctx.send(f"Oops {ctx.message.author.display_name} I could not find that role. `Err:RoleNotFound`")

    @commands.command()
    @commands.has_any_role(766652488974991390, 804331016168276028)
    async def role_rem_all(self, ctx, role: discord.Role):
        embed=discord.Embed(title = "Standby.... this will take time and won't stop until completed.",colour=discord.Color(0xff0000),timestamp = datetime.utcnow())
        stby = await ctx.send(embed=embed)
        for members in ctx.message.guild.members:
            if members.bot == False:
                await members.remove_roles(role)
            else:
                pass
        embed1 = discord.Embed(title = "Removed Role From All Members:", description = f"{role.mention} was removed from all members in {ctx.guild.name}", colour=discord.Color(0xff0000),timestamp = datetime.utcnow())
        embed1.set_footer(text = f"Requested by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
        await stby.edit(embed=embed1)
    
    @role_rem_all.error
    async def role_rem_all_error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            await ctx.send(f"Oops {ctx.message.author.display_name} I could not find that role. `Err:RoleNotFound`")



def setup(bot):
    bot.add_cog(Moderation(bot))

