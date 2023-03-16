from discord.ext import commands
import discord
from lib.db import db
from datetime import datetime
from dotenv import load_dotenv
import os
import chat_exporter
from io import *


load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))


OPTIONS = {
    "🔒" : 0
}

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        first_id = 856597157871616041
        sec_id = 856597211970404382
        
        if payload.member.id != self.bot.user.id and str(payload.emoji) == "📩":
            
            channel_id = 769205709882654770
            category_id = 769205620527071293 

            if payload.message_id == first_id:


                for category in guild.categories:
                    if category.id == category_id:
                        break

                channel = guild.get_channel(channel_id)
                
                ticketnumber = db.field("SELECT ChannelNum FROM tickets WHERE ReactID = 1963")
                ticket_channel = await category.create_text_channel(f"Ticket - {ticketnumber}")
                db.execute("UPDATE tickets SET ChannelNum = ChannelNum + 1")
                
                
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = False
                await ticket_channel.set_permissions(guild.default_role,overwrite=overwrite)
                await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True, read_message_history=True)

                message = await channel.fetch_message(first_id)
                await message.remove_reaction(payload.emoji, payload.member)
                embed1 = discord.Embed(title = "Ticket Created", description = "To close the ticket react with 🔒", colour = discord.Color(0xff0000))
                embed1.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)

                await ticket_channel.send(f"{payload.member.mention} I have created a separate support ticket channel. <@&766652488974991390> will be here shortly to assist you. In the meanwhile please write as to how can the vACC Staff help you.")
                ticket_created = await ticket_channel.send(embed=embed1)
                for emoji in list(OPTIONS.keys()):
                    await ticket_created.add_reaction(emoji)
                
                await discord.Message.pin(ticket_created)
                db.execute("INSERT INTO tickets (TicketID, ReactID, UserID) VALUES (?,?,?)", ticket_channel.id,ticket_created.id,payload.member.id)
            
            elif payload.message_id == sec_id:
                
                for category in guild.categories:
                    if category.id == category_id:
                        break

                channel = guild.get_channel(channel_id)

                ticketnumber = db.field("SELECT ChannelNum FROM tickets WHERE ReactID = 1963")
                ticket_channel = await category.create_text_channel(f"Ticket - {ticketnumber}")
                db.execute("UPDATE tickets SET ChannelNum = ChannelNum + 1")

                    
                overwrite = discord.PermissionOverwrite()
                overwrite.view_channel = False
                await ticket_channel.set_permissions(guild.default_role,overwrite=overwrite)
                await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True, read_message_history=True)

                message = await channel.fetch_message(sec_id)
                await message.remove_reaction(payload.emoji, payload.member)
                embed1 = discord.Embed(title = "Ticket Created", description = "To close the ticket react with 🔒", colour = discord.Color(0xff0000))
                embed1.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)

                await ticket_channel.send(f"{payload.member.mention} I have created a separate support ticket channel. <@&811154180730781736> will be here shortly to assist you. In the meanwhile please write your suggestions/feature requests.")
                ticket_created = await ticket_channel.send(embed=embed1)
                for emoji in list(OPTIONS.keys()):
                    await ticket_created.add_reaction(emoji)

                await discord.Message.pin(ticket_created)  
                db.execute("INSERT INTO tickets (TicketID, ReactID, UserID) VALUES (?,?,?)", ticket_channel.id,ticket_created.id,payload.member.id)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def transcriptpls(self, ctx):
        loading_embed = discord.Embed(color = 0xff0000)
        loading_embed.set_author(name=f"Standby {ctx.message.author.display_name}, this is gonna take some time.", icon_url="https://media.giphy.com/media/sSgvbe1m3n93G/source.gif?cid=ecf05e47a0z65sl6qyqji8f06i3zanuj9s581zjo8pp2jns9&rid=source.gif&ct=g")
        msg = await ctx.send(embed=loading_embed)
        transcript_channel = self.bot.get_channel(804404022688874566)
        await chat_exporter.quick_export(ctx, transcript_channel)
        await msg.delete()
        await ctx.send(f"Done check {transcript_channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def addmem(self, ctx, member : discord.Member):
        perm_channel = ctx.message.channel
        await perm_channel.set_permissions(member, read_messages=True, send_messages=True, read_message_history=True)
        embed = discord.Embed(title="Member Added In This Channel", description = f"{member.mention} was added to channel {ctx.channel.mention}", colour = discord.Color(0xff0000), timestamp=datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def remmem(self, ctx, member : discord.Member):
        perm_channel = ctx.message.channel
        await perm_channel.set_permissions(member, read_messages=False, send_messages=False, read_message_history=False)
        embed = discord.Embed(title="Member Removed From This Channel", description = f"{member.mention} was removed from channel {ctx.channel.mention}",colour = discord.Color(0xff0000), timestamp=datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def addrole(self, ctx, role: discord.Role):
        perm_channel = ctx.message.channel
        await perm_channel.set_permissions(role, read_messages=True, send_messages=True, read_message_history=True)
        embed = discord.Embed(title="Role Added In This Channel", description = f"{role.mention} was added to channel {ctx.channel.mention}",colour = discord.Color(0xff0000), timestamp=datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def remrole(self, ctx, role: discord.Role):
        perm_channel = ctx.message.channel
        await perm_channel.set_permissions(role, read_messages=False, send_messages=False, read_message_history=False)
        embed = discord.Embed(title="Role Removed From This Channel", description = f"{role.mention} was removed from channel {ctx.channel.mention}",colour = discord.Color(0xff0000), timestamp=datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
        await ctx.channel.send(embed=embed)
        await ctx.message.delete()
    
    # #comment both of them
    # @commands.command()
    # async def sendticket(self, ctx):
    #     embed = discord.Embed(title = "Contact vACC Staff", description = "To create a support ticket react with 📩",colour = discord.Color(0xff0000))
    #     embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
    #     channel = self.bot.get_channel(769205709882654770)
    #     info = await channel.send(embed=embed)
    #     await info.add_reaction("📩")


    # @commands.command()
    # async def sendsuggestions(self, ctx):
    #     embed = discord.Embed(title = "Nepal vACC Suggestions/Feature Requests in the bot", description = "To create a support ticket react with 📩",colour = discord.Color(0xff0000))
    #     embed.set_footer(text="Nepal vACC Supervisor", icon_url=self.bot.user.avatar_url)
    #     channel = self.bot.get_channel(769205709882654770)
    #     info = await channel.send(embed=embed)
    #     await info.add_reaction("📩")




def setup(bot):
    bot.add_cog(TicketSystem(bot))