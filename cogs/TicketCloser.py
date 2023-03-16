from discord.ext import commands
from lib.db import db
import discord
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))



class TicketCloser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)

        if payload.member.id != self.bot.user.id and str(payload.emoji) == "🔒":
            
            ticket_channel = self.bot.get_channel(payload.channel_id)
            embed_id = db.field("SELECT ReactID FROM tickets WHERE TicketID = ?", ticket_channel.id)
            if payload.message_id == embed_id:
                category = discord.utils.get(guild.categories, id = 775330024139259916)
                get_ticket_channel = self.bot.get_channel(ticket_channel.id)
                member_id = db.field("SELECT UserID FROM tickets WHERE TicketID = ?", ticket_channel.id)
                member = self.bot.get_user(id = member_id)
                await get_ticket_channel.set_permissions(member, read_messages=False, send_messages=False, read_message_history=False)
                await get_ticket_channel.edit(reason=None, category=category)
                closed_channel = await get_ticket_channel.send("Ticket Closed, clearing up database.....")
                db.execute("DELETE FROM tickets WHERE ReactID = ?", embed_id)
                await asyncio.sleep(3)
                await closed_channel.edit(content = f"Ticket Closed :lock:. Denied Permissions to see channel for {member.mention}. Deleted `UserID`, `ChannelID` and `ReactionID` from database. :white_check_mark: ")




def setup(bot):
    bot.add_cog(TicketCloser(bot))