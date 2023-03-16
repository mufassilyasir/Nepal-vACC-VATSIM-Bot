from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

import discord
import os


load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if isinstance(message.channel, discord.DMChannel):
                if len(message.content) < 30:
                    await message.channel.send("Hi. :wave: This DM Channel is strictly for conveying your message/complaint to Nepal vACC Staff team :flag_np: . If you wish to contact Nepal vACC Staff team, please ensure your message is at least 30 characters long.\n\n -Thanks Nepal vACC Supervisor.")

                else:
                    embed = discord.Embed(title = "Recieved a DM! (Mod Mail)", colour = discord.Color(0xff0000), timestamp = datetime.utcnow())
                    embed.set_footer(text=f"Message received from {message.author.name}", icon_url=message.author.avatar_url)
                    embed.add_field(inline=False, name="Message Content:", value=message.content)
                    channel = self.bot.get_channel(LOG_CHANNEL_ID)
                    await channel.send(embed=embed)
                    await channel.send("<@&766652488974991390> ^^ :)")
                    await message.channel.send("Thank you. Your request has been forwarded to Nepal vACC Staff Team. If you do not receive a reply from a member of Nepal vACC Staff team **within 24-48 hours**. Please send them an email at `staff@nepalvacc.com`. \n -Thanks Nepal vACC Supervisor")



def setup(bot):
    bot.add_cog(ModMail(bot))