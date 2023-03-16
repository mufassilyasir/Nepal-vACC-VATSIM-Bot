import discord
import os
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class MemberListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(Title = f"**Welcome**",colour=discord.Colour(0xff0000),description = f"Namastey {member.mention}! Welcome to {member.guild.name}. You should already have access to the server channels. We update member ratings every day at 1900 UTC, please wait until that time and your ratings will automatically update as per VATSIM records. Please take a look at <#804615185498374155> where you can find our Discord server policy and guidelines. If you have any questions feel free to reply here and the bot will convey your message to us. Once again welcome and we hope you enjoy your stay! \n **Regards, Nepal vACC Staff Team**")
        await member.send(embed=embed)
        embed = discord.Embed(title = "**Member Joined :clap: **", colour = discord.Colour(0xff0000),timestamp = datetime.utcnow())
        embed.set_thumbnail(url = member.avatar_url)
        fields = [("Who?", member.mention,  False), 
                ("Name", str(member.name), True),
                ("Bot?", member.bot, True),
                ("Created Discord account on", member.created_at.strftime("%d/%m/%Y %H:%M:%S UTC"), True),
                ("Joined this server on", member.joined_at.strftime("%d/%m/%Y %H:%M:%S UTC"), True)]
        
        for name, value, inline in fields:
            embed.add_field(name = name, value = value, inline = inline)
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        await channel.send(embed=embed)


        role1 = discord.utils.get(member.guild.roles, id = 850770522995294289)
        role2 = discord.utils.get(member.guild.roles, id = 768142567283359824)
        role3 = discord.utils.get(member.guild.roles, id = 768139821876641822)
        role4 = discord.utils.get(member.guild.roles, id = 768141705496887297)
        role5 = discord.utils.get(member.guild.roles, id = 765542666095558676)

        try:
            await member.add_roles(role1)
            await member.add_roles(role2)
            await member.add_roles(role3)
            await member.add_roles(role4)
            await member.add_roles(role5)
        except:
            await channel.send(f"Error I could not assign a role to the member {member.mention}")
        else:
            embed1 = discord.Embed(colour = discord.Colour(0xff0000),timestamp = datetime.utcnow())
            embed1.add_field(inline=False, name = "**Role Assigned:**", value = f"I successfully assigned the **{role1}**, **{role2}**, **{role3}**, **{role4}** and **{role5}**  roles to {member.mention}")
            await channel.send(embed=embed1)
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title = "**Member Left**",colour=discord.Colour(0xff0000), timestamp = datetime.utcnow())
        embed.set_thumbnail(url = member.avatar_url)
        embed.add_field(inline=False,name = f"{member}, Left the server!", value = "..." )
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        await channel.send(embed=embed)

def setup(bot):
  bot.add_cog(MemberListener(bot))