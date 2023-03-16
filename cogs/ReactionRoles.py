import discord
import os
from discord.ext import commands
from datetime import datetime
from lib.db import db
from dotenv import load_dotenv

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Reaction Role Assignment
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        get_reaction_channel = self.bot.get_channel(850297428234338334)
        msg =  get_reaction_channel.get_partial_message(854817561723797544)
        ourMessageId = 854817561723797544
        if ourMessageId == payload.message_id:
            member = payload.member
            guild = member.guild
            emoji = payload.emoji.name

            if emoji == "📢":
                role = discord.utils.get(guild.roles, id = 810793952990593045)
                try:
                    await member.add_roles(role)
                except:
                    embed = discord.Embed(title = "Reaction Role Error :(", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                    embed.add_field(inline=False, name = "Role Assignment Error:", value = f"Could not assign role to member {member.mention}")
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(title = "Reaction Role(s) Assigned", colour = discord.Color(0xff0000))
                    embed.add_field(inline=False, name="\u200b",value = f"I have added the {role} role because you reacted in {guild.name}")
                    embed.set_footer(text="Regards Nepal vACC Staff")
                    await member.send(embed=embed)
            
            elif emoji == "📝":
                role = discord.utils.get(guild.roles, id = 804331394347171900)
                try:
                    await member.add_roles(role)
                except:
                    embed = discord.Embed(title = "Reaction Role Error :(", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                    embed.add_field(inline=False, name = "Role Assignment Error:", value = f"Could not assign role to member {member.mention}")
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(title = "Reaction Role(s) Assigned", colour = discord.Color(0xff0000))
                    embed.add_field(inline=False, name="\u200b",value = f"I have added the {role} role because you reacted in {guild.name}")
                    embed.set_footer(text="Regards Nepal vACC Staff")
                    await member.send(embed=embed)
                
            elif emoji == "📅":
                role = discord.utils.get(guild.roles, id = 810791169936064512)
                try:
                    await member.add_roles(role)
                except:
                    embed = discord.Embed(title = "Reaction Role Error :(", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                    embed.add_field(inline=False, name = "Role Assignment Error:", value = f"Could not assign role to member {member.mention}")
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(title = "Reaction Role(s) Assigned", colour = discord.Color(0xff0000))
                    embed.add_field(inline=False, name="\u200b",value = f"I have added the {role} role because you reacted in {guild.name}")
                    embed.set_footer(text="Regards Nepal vACC Staff")
                    await member.send(embed=embed)
            
            elif emoji == "📡":
                check_role = discord.utils.get(guild.roles, id = 767396981856534528)
                role_assign = discord.utils.get(guild.roles, id = 850069042160992276)
                if check_role in member.roles:
            
                    try:
                        await member.add_roles(role_assign)
                    except:
                        embed = discord.Embed(title = "Reaction Role Error :(", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                        embed.add_field(inline=False, name = "Role Assignment Error:", value = f"Could not assign role to member {member.mention}")
                        await channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title = "Reaction Role(s) Assigned", colour = discord.Color(0xff0000))
                        embed.add_field(inline=False, name="\u200b",value = f"I have added the {role_assign} role because you reacted in {guild.name}")
                        embed.set_footer(text="Regards Nepal vACC Staff")
                        await member.send(embed=embed)
                else:
                    embed2 = discord.Embed(title = f"Hello {member.display_name}", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                    embed2.set_thumbnail(url = guild.icon_url)
                    embed2.add_field(inline=False, name="Reaction Role Error:", value = "Unfortunately I am 'smort' :sunglasses: and Nepal vACC Staff told me `@Request ATC` role is only for Nepal vACC Approved Controllers.")
                    embed2.add_field(inline=False, name="What happens now?", value="Well nothing, I just didn't assign you the `@Request ATC` role but other than that all is good. :)")
                    embed2.add_field(inline=False, name="No this is not correct:", value="If you think I am not 'smort' and this is a mistake, please contact the Nepal vACC Staff Team. Tell them you should have the `@Nepal vACC Approved Controller` role. I apologize for any inconvenience caused :sweat_smile: ")
                    await member.send(embed=embed2)
                    await msg.remove_reaction(emoji, member)
            

                    embed3 = discord.Embed(title = "Reaction Role Error:",colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                    embed3.set_thumbnail(url = member.avatar_url)
                    embed3.add_field(inline=False, name="What??", value=f"{member.mention} used the reaction role and asked for <@&850069042160992276> role :joy:. Since he didn't had <@&767396981856534528> role, I didn't assign him the role he requested.")
                    await channel.send(embed=embed3)
        
        elif payload.emoji.name == "⭐":

            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if not message.author.bot:
                msg_id, stars = db.record("SELECT StarMessageID, Stars FROM starboard WHERE RootMessageID = ?", message.id) or (None, 0)
                embed = discord.Embed(title= "Highlighted Message", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                embed.set_footer(text=f"Highlighted Message Author: {message.author.display_name}", icon_url=message.author.avatar_url)
                embed.add_field(inline=False, name="Message:", value=f"{message.content}" or "Author has attached an attachment:")
                embed.add_field(inline=False, name="Message Link:", value=f"[Jump to Message]({message.jump_url})")
                embed.add_field(inline=False, name="Message Stars:", value=f"{stars+1} :star:")
                self.starboard_channel = self.bot.get_channel(856087039233490954)
                
                if len(message.attachments):
                  embed.set_image(url=message.attachments[0].url)
        
                if not stars:
                  db.execute("INSERT INTO starboard (RootMessageID) VALUES (?)", message.id)
                  db.execute("UPDATE starboard SET Stars = Stars + 1 WHERE RootMessageID = ?", message.id)
                
                if stars == 1 and msg_id == None:
                   star_message = await self.starboard_channel.send(embed=embed)
                   db.execute("UPDATE starboard SET StarMessageID = ? WHERE RootMessageID = ?", star_message.id, message.id)
                   db.execute("UPDATE starboard SET Stars = Stars + 1 WHERE RootMessageID = ?", message.id)
        
                elif stars == 1 and msg_id != None:
                  star_message = await self.starboard_channel.fetch_message(msg_id)
                  await star_message.edit(embed=embed)
                  db.execute("UPDATE starboard SET Stars = Stars + 1 WHERE RootMessageID = ?", message.id)
                 
                elif stars >= 2:
                  star_message = await self.starboard_channel.fetch_message(msg_id)
                  await star_message.edit(embed=embed)
                  db.execute("UPDATE starboard SET Stars = Stars + 1 WHERE RootMessageID = ?", message.id)
            
            else:
                await message.remove_reaction(payload.emoji, payload.member)
                payload_channel = self.bot.get_channel(payload.channel_id)
                await payload_channel.send(f"Hey {payload.member.mention} you can't highlight my own message.:sneezing_face:  I am already very highlighted bot.")

    
    #Reaction Role Removed
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = self.bot.get_channel(850460188867952650)
        ourMessageId = 854817561723797544
        if ourMessageId == payload.message_id:
            guild = await(self.bot.fetch_guild(payload.guild_id))
            emoji = payload.emoji.name
            member = await(guild.fetch_member(payload.user_id))

            if emoji == "📢":
                role = discord.utils.get(guild.roles, id = 810793952990593045)
                if member is not None:
                    try:
                        await member.remove_roles(role)
                    except:
                        embed = discord.Embed(title = "Reaction Role Error :(", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                        embed.add_field(inline=False, name = "Role Removal Error:", value = f"Could not remove role from member {member.mention}")
                        await channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title = "Reaction Role(s) Removed", colour = discord.Color(0xff0000))
                        embed.add_field(inline=False, name="\u200b",value = f"I have removed the {role} role because you unreacted in {guild.name}")
                        embed.set_footer(text="Regards Nepal vACC Staff")
                        await member.send(embed=embed)
                else:
                    await channel.send("Member Not Found. `Err:ReactionRoleRemoval`")

            elif emoji == "📝":
                role = discord.utils.get(guild.roles, id = 804331394347171900)
                if member is not None:
                    try:
                        await member.remove_roles(role)
                    except:
                        embed = discord.Embed(title = "Reaction Role Error :(", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                        embed.add_field(inline=False, name = "Role Removal Error:", value = f"Could not remove role from member {member.mention}")
                        await channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title = "Reaction Role(s) Removed", colour = discord.Color(0xff0000))
                        embed.add_field(inline=False, name="\u200b",value = f"I have removed the {role} role because you unreacted in {guild.name}")
                        embed.set_footer(text="Regards Nepal vACC Staff")
                        await member.send(embed=embed)
                else:
                    await channel.send("Member Not Found. `Err:ReactionRoleRemoval`")

            elif emoji == "📅":
                role = discord.utils.get(guild.roles, id = 810791169936064512)
                if member is not None:
                    try:
                        await member.remove_roles(role)
                    except:
                        embed = discord.Embed(title = "Reaction Role Error :(", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                        embed.add_field(inline=False, name = "Role Removal Error:", value = f"Could not remove role from member {member.mention}")
                        await channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title = "Reaction Role(s) Removed", colour = discord.Color(0xff0000))
                        embed.add_field(inline=False, name="\u200b",value = f"I have removed the {role} role because you unreacted in {guild.name}")
                        embed.set_footer(text="Regards Nepal vACC Staff")
                        await member.send(embed=embed)
                else:
                    await channel.send("Member Not Found. `Err:ReactionRoleRemoval`")

            elif emoji == "📡":
                role = discord.utils.get(guild.roles, id = 850069042160992276)
                if role in member.roles:
                    if member is not None:
                        try:
                            await member.remove_roles(role)
                        except:
                            embed = discord.Embed(title = "Reaction Role Error :(", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                            embed.add_field(inline=False, name = "Role Removal Error:", value = f"Could not remove role from member {member.mention}")
                            await channel.send(embed=embed)
                        else:
                            embed = discord.Embed(title = "Reaction Role(s) Removed", colour = discord.Color(0xff0000))
                            embed.add_field(inline=False, name="\u200b",value = f"I have removed the {role} role because you unreacted in {guild.name}")
                            embed.set_footer(text="Regards Nepal vACC Staff")
                            await member.send(embed=embed)
                    else:
                        await channel.send("Member Not Found. `Err:ReactionRoleRemoval`")
                else:
                    pass
        elif payload.emoji.name == "⭐":

            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if not message.author.bot:

                msg_id, stars = db.record("SELECT StarMessageID, Stars FROM starboard WHERE RootMessageID = ?", message.id)
                embed = discord.Embed(title= "Highlighted Message", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                embed.set_footer(text=f"Highlighted Message Author: {message.author.display_name}", icon_url=message.author.avatar_url)
                embed.add_field(inline=False, name="Message:", value=f"{message.content}" or "Author has attached an attachment:")
                embed.add_field(inline=False, name="Message Link:", value=f"[Jump to Message]({message.jump_url})")
                embed.add_field(inline=False, name="Message Stars:", value=f"{stars-1} :star:")
                
                if len(message.attachments):
                    embed.set_image(url=message.attachments[0].url)
                
                self.starboard_channel = self.bot.get_channel(856087039233490954)
                star_message = await self.starboard_channel.fetch_message(msg_id)
                if stars == 1:
                    await star_message.delete()
                    db.execute("DELETE FROM starboard WHERE RootMessageID = ?", message.id)
                else:
                    await star_message.edit(embed=embed)
                    db.execute("UPDATE starboard SET Stars = Stars - 1 WHERE RootMessageID = ?", message.id)
            else:
                pass  


    # #reaction role send (DANGER)
    # @commands.command(hidden = True)
    # @commands.has_permissions(administrator = True)
    # async def send_the_react_message_in_channel_get_role_admin_yes_sorry_needed_to_make_sure_you_dont_send_it_by_mistake(self, ctx):
    #     channel = self.bot.get_channel(850297428234338334)
    #     embed = discord.Embed(title = ":bell: Get Notification Roles By Reacting To This Message.", colour = discord.Color(0xff0000))
    #     embed.set_footer(text = "VATSIM Nepal vACC |🌐 www.nepalvacc.com | 📧 staff@nepalvacc.com")
    #     embed.set_thumbnail(url = ctx.guild.icon_url)
    #     embed.add_field(inline=False,name="\u200b", value= "📢 - React to this emoji to get <@&810793952990593045> role.")
    #     embed.add_field(inline=False,name="\u200b", value= "📝 - React to this emoji to get <@&804331394347171900> role.")
    #     embed.add_field(inline=False,name="\u200b",value= "📅 - React to this emoji to get <@&810791169936064512> role.")
    #     embed.add_field(inline=False,name="Note:", value= "**<@&850069042160992276> role is only for Nepal vACC Approved Controllers!**")
    #     embed.add_field(inline=False,name="\u200b", value= "📡 - React to this emoji to get <@&850069042160992276> role and get notified in DM if a VATSIM member requests ATC in Nepal vACC.")
    #     react_message = await channel.send(embed=embed)
    #     await react_message.add_reaction("📢")
    #     await react_message.add_reaction("📝")
    #     await react_message.add_reaction("📅")
    #     await react_message.add_reaction("📡")
    #     await ctx.message.delete()
    #     await ctx.send("Reaction Roles Posted")

def setup(bot):
    bot.add_cog(ReactionRoles(bot))