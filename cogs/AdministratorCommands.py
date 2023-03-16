from discord.ext import commands

import discord
import aiohttp
import traceback
import os


class AdministratorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #admin help menu
    @commands.command(hidden = True)
    @commands.has_permissions(administrator = True)
    async def Helpadmin(self, ctx):
        embed1 = discord.Embed(title="**Administrators Help Menu \n\n Moderation Commands!**", colour=discord.Colour(0xff0000))
        embed1.set_thumbnail(url = ctx.guild.icon_url)
        

        embed1.add_field(inline=False, name="Notice:", value="If you are able to run this command you have administrator permissions. Hence these commands are for you.")
        embed1.add_field(inline=False, name="Send Announcement:", value="This command sends a custom message to the specified channel. To use this command simply use `?announcement` and the bot will ask you for further questions. An example to run this command can be: \n `?announcement`")
        embed1.add_field(inline=False, name="Send DM:", value="This command sends a custom message to the specified server member. To use this command simply use `?dm` followed by member id or mention and the bot will ask you for the message that will be sent to the member. An example to run this command can be: \n `?dm 494904136760819727`")
        embed1.add_field(inline=False, name="Kick Member:", value="This command will kick the specified member with a DM (if DM's are allowed by the member) and reason. To use this command simply use `?kick` followed by member id or mention and the bot will ask you for the reason. If you did not provide any reason within the time frame provided by the bot, the bot will automatically kick with reason 'No reason provided by the vACC Staff' as default. An example to run this command can be: \n `?kick @resh`")
        embed1.add_field(inline=False, name="Ban Member:", value="This command will ban the specified member with a DM (if DM's are allowed by the member) and reason. To use this command simply use `?ban` followed by member id or mention and the bot will ask you for the reason. If you did not provide any reason within the time frame provided by the bot, the bot will automatically ban with reason 'No reason provided by the vACC Staff' as default. An example to run this command can be: \n `?ban @resh`")
        embed1.add_field(inline=False, name="Delete Messages", value="This command will delete specified number of messages in the channel where it was ran. To use this command simply go to the channel where you wish to delete messages and use `?delete` or `?purge` followed by number of messages that you want to delete. An example to run this command can be: \n `?delete 10` or alternatively you can use `?purge 10` **Note:** This command can quickly delete messages sent upto 2 weeks before. If the time frame goes more older than 2 weeks it would keep on deleting but 1 by 1. *So keep patience it will be a little slow* ")
        embed1.add_field(inline=False, name="Mute:", value="This command will mute a member. To use this command type ?mute @resh/or his ID [time in hours] [reason]. If time is left empty member will muted forever until manually unmuted. If reason is left empty default reason will be used 'No reason provided by the vACC Staff' **(FOR NOW THIS IS ONLY FOR LOG PURPOSES)** Example of this command will be `?mute 225302886106660864 5 testing` ")                                                                    
        embed1.add_field(inline=False, name="Unmute:", value="This command will unmute a member. To use this command type ?unmute @resh/or his ID [reason]. If reason is left empty default reason will be used 'No reason provided by the vACC Staff' **(FOR NOW THIS IS ONLY FOR LOG PURPOSES)** Example of this command will be `?unmute 225302886106660864 testing` ")    
        embed1.add_field(inline=False, name="Add Member:", value="This command will add a member in the channel where the command was ran with default perms. To use this command type ?addmem and the person you wish to add ID or mention. Example of this command will be `?addmem 388955006633508865`")
        embed1.add_field(inline=False, name="Remove member:", value="This command will remove the member in the channel where the command was ran. To use this command type ?remmem and the person you wish to remove ID or mention. Example of this command will be `?remmem 388955006633508865`")
        embed1.add_field(inline=False, name="Add Role:", value="This command will add the role in the channel where the command was ran with default perms. To use this command type ?addrole and the role you wish to add ID or mention. Example of this command will be `?addrole 530729347288662033`")
        embed1.add_field(inline=False, name="Remove role:", value="This command will remove the role in the channel where the command was ran. To use this command type ?remrole and the role you wish to remove ID or mention. Example of this command will be `?remrole 530729347288662033`")
        embed1.add_field(inline=False, name="Generate Transcript:", value="This command will generate transcript of the channel and send it to transcripts channel. Example of this command will be `?transcriptpls`")
        
        
        embed2 = discord.Embed(title="**Administrators Help Menu \n\n Informative Commands **", colour=discord.Colour(0xff0000))
        

        embed2.set_thumbnail(url = ctx.guild.icon_url)
        embed2.add_field(inline=False, name="Howtogetrole:", value="This command will send a message where this command was ran to mention the member to link their account via VATSIM community Hub. (It will automatically delete the message of the person who ran the command). To use this command simply go to the channel where you wish to send the message. To run this command use: \n `?howtogetrole`")
        embed2.add_field(inline=False, name="Atcprocess:", value="This command will send a message where this command was ran to explain member the process to get started as ATC in Nepal vACC. (It will automatically delete the message of the person who ran the command). To use this command simply go to the channel where you wish to send the message. To run this command use: \n `atcprocess`")                           
        embed2.add_field(inline=False, name="Social Media:", value="This command will send a message where this command was ran to mention Nepal vACC Social Media links including Nepal vACC Website link. (It will automatically delete the message of the person who ran the command). To use this command simply go to the channel where you wish to send the message. To run this command use: \n `socialmedia`")
        embed2.add_field(inline=False, name="Send Rules:", value="This command will send rules where this command was ran to mention Nepal vACC Rules, VATSIM Network Rules and Discord Rules. (It will automatically delete the message of the person who ran the command). To use this command simply go to the channel where you wish to send rules. To run this command use: \n `?send_rules_admin`")
        embed2.add_field(inline=False, name="Send Nepal vACC Policy Link:", value="This command will send Nepal vACC Policy link where this command was ran. (It will automatically delete the message of the person who ran the command). To use this command simply go to the channel where you wish to send Nepal vACC Policy link. To run this command use: \n `?policy`")
        
        embed3 = discord.Embed(title="**Administrators Help Menu \n\n Finally... **", colour=discord.Colour(0xff0000))
        embed3.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.name}")

        embed3.add_field(inline=False, name="Something wrong?", value="Anything missing or not working? Let the IT Team know.")

        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)
        await ctx.send(embed=embed3)
    
    @commands.command()
    @commands.has_any_role(766652488974991390, 804331016168276028)
    async def helpstaff(self,ctx):
        embed1 = discord.Embed(title="**Staff Help Menu \n\n Moderation Commands!**", colour=discord.Colour(0xff0000))
        embed1.set_thumbnail(url = ctx.guild.icon_url)
        embed1.add_field(inline=False, name="Notice:", value="If you are able to run this command you have staff permissions. Hence these commands are for you.")
        embed1.add_field(inline=False, name="Send Announcement:", value="This command sends a custom message to the specified channel. To use this command simply use `?announcement` and the bot will ask you for further questions. An example to run this command can be: \n `?announcement`")
        embed1.add_field(inline=False, name="Send DM:", value="This command sends a custom message to the specified server member. To use this command simply use `?dm` followed by member id or mention and the bot will ask you for the message that will be sent to the member. An example to run this command can be: \n `?dm 494904136760819727`")
        embed1.add_field(inline=False, name="Kick Member:", value="This command will kick the specified member with a DM (if DM's are allowed by the member) and reason. To use this command simply use `?kick` followed by member id or mention and the bot will ask you for the reason. If you did not provide any reason within the time frame provided by the bot, the bot will automatically kick with reason 'No reason provided by the vACC Staff' as default. An example to run this command can be: \n `?kick @resh`")
        embed1.add_field(inline=False, name="Delete Messages", value="This command will delete specified number of messages in the channel where it was ran. To use this command simply go to the channel where you wish to delete messages and use `?delete` or `?purge` followed by number of messages that you want to delete. An example to run this command can be: \n `?delete 10` or alternatively you can use `?purge 10` **Note:** This command can quickly delete messages sent upto 2 weeks before. If the time frame goes more older than 2 weeks it would keep on deleting but 1 by 1. *So keep patience it will be a little slow* ")
        embed1.add_field(inline=False, name="Mute:", value="This command will mute a member. To use this command type ?mute @resh/or his ID [time in hours] [reason]. If time is left empty member will muted forever until manually unmuted. If reason is left empty default reason will be used 'No reason provided by the vACC Staff' **(FOR NOW THIS IS ONLY FOR LOG PURPOSES)** Example of this command will be `?mute 225302886106660864 5 testing` ")                                                                    
        embed1.add_field(inline=False, name="Unmute:", value="This command will unmute a member. To use this command type ?unmute @resh/or his ID [reason]. If reason is left empty default reason will be used 'No reason provided by the vACC Staff' **(FOR NOW THIS IS ONLY FOR LOG PURPOSES)** Example of this command will be `?unmute 225302886106660864 testing` ")    
        embed1.add_field(inline=False, name="Add Member:", value="This command will add a member in the channel where the command was ran with default perms. To use this command type ?addmem and the person you wish to add ID or mention. Example of this command will be `?addmem 388955006633508865`")
        embed1.add_field(inline=False, name="Remove member:", value="This command will remove the member in the channel where the command was ran. To use this command type ?remmem and the person you wish to remove ID or mention. Example of this command will be `?remmem 388955006633508865`")
        embed1.add_field(inline=False, name="Add Role:", value="This command will add the role in the channel where the command was ran with default perms. To use this command type ?addrole and the role you wish to add ID or mention. Example of this command will be `?addrole 530729347288662033`")
        embed1.add_field(inline=False, name="Remove role:", value="This command will remove the role in the channel where the command was ran. To use this command type ?remrole and the role you wish to remove ID or mention. Example of this command will be `?remrole 530729347288662033`")
        embed1.add_field(inline=False, name="Add role to everyone:", value="This command will add the role to all members in the server. To use this command type ?role_add_all and mention the role you wish to add. Example of this command will be `?role_add_all @guest`")
        embed1.add_field(inline=False, name="Remove role from everyone:", value="This command will remove the role from all members in the server. To use this command type ?role_rem_all and the role you wish to remove. Example of this command will be `?role_rem_all @guest`")
       
        embed2 = discord.Embed(title="**Staff Help Menu \n\n Informative Commands **", colour=discord.Colour(0xff0000))
        

        embed2.set_thumbnail(url = ctx.guild.icon_url)
        embed2.add_field(inline=False, name="Howtogetrole:", value="This command will send a message where this command was ran to mention the member to link their account via VATSIM community Hub. (It will automatically delete the message of the person who ran the command). To use this command simply go to the channel where you wish to send the message. To run this command use: \n `?howtogetrole`")
        embed2.add_field(inline=False, name="Atcprocess:", value="This command will send a message where this command was ran to explain member the process to get started as ATC in Nepal vACC. (It will automatically delete the message of the person who ran the command). To use this command simply go to the channel where you wish to send the message. To run this command use: \n `atcprocess`")                           
        embed2.add_field(inline=False, name="Social Media:", value="This command will send a message where this command was ran to mention Nepal vACC Social Media links including Nepal vACC Website link. (It will automatically delete the message of the person who ran the command). To use this command simply go to the channel where you wish to send the message. To run this command use: \n `socialmedia`")
        embed2.add_field(inline=False, name="Send Rules:", value="This command will send rules where this command was ran to mention Nepal vACC Rules, VATSIM Network Rules and Discord Rules. (It will automatically delete the message of the person who ran the command). To use this command simply go to the channel where you wish to send rules. To run this command use: \n `?send_rules_admin`")
        embed2.add_field(inline=False, name="Send Nepal vACC Policy Link:", value="This command will send Nepal vACC Policy link where this command was ran. (It will automatically delete the message of the person who ran the command). To use this command simply go to the channel where you wish to send Nepal vACC Policy link. To run this command use: \n `?policy`")

        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)
    
    #how to get a role command
    @commands.command(hidden = True)
    @commands.has_any_role(766652488974991390, 804331016168276028)
    async def howtogetrole(self, ctx):
        await ctx.send("Hello! You need to link your discord account with VATSIM via https://community.vatsim.net/. Once done  go to https://community.vatsim.net and after linking your Discord and VATSIM accounts, head over to the 'Joined' section, look for 'VATSIM Nepal vACC' server, click on 'Edit Username', select your preferred choice, and accept. Then we can start chatting again!")
        await ctx.message.delete()
    
    #ATC process command
    @commands.command(hidden = True)
    @commands.has_any_role(766652488974991390, 804331016168276028)
    async def atcprocess(self, ctx):
        await ctx.send("Hello, are you intrested to be a Part of ATC with Nepal vACC? Before we proceed please ensure that you are a part of Nepal vACC within West Asia Division. For procedure please visit https://vatwa.net/transfers/. Once you are a part of Nepal vACC, Please open a ticket in VATWA HQ & assign to Nepal vACC requsting ATC training and we will explain further process. See you there!")
        await ctx.message.delete()
    
    #social media command
    @commands.command(hidden= True)
    @commands.has_any_role(766652488974991390, 804331016168276028)
    async def socialmedia(self, ctx):
        embed = discord.Embed(title="**Nepal vACC Social Media**", colour=discord.Colour(0xff0000))

        embed.add_field(inline=False, name="Website Link:", value="https://nepalvacc.com/")
        embed.add_field(inline=False, name="Dashboard Website Link:", value="https://www.members.nepalvacc.com")
        embed.add_field(inline=False, name="Instagram Account Link:", value="https://www.instagram.com/vatsim_nepal/")
        embed.add_field(inline=False, name="Facebook Account Link:", value="https://www.facebook.com/NepalvACC")
        embed.add_field(inline=False, name="Twitter Account Link:", value="https://twitter.com/VatsimN")

        await ctx.send(embed=embed)
        await ctx.message.delete()
    
    #Rules command
    @commands.command(hidden=True)
    @commands.has_any_role(766652488974991390, 804331016168276028)
    async def send_rules_admin(self, ctx):
        embed1 = discord.Embed(title="**Rules**", colour=discord.Colour(0xff0000))

        embed1.add_field(inline=False, name="Discord Terms of Service & Community Guidelines", value="All members must follow Discord's Community Guidelines and Terms of Service at all times.\nToS — https://discordapp.com/terms\nGuidelines — https://discordapp.com/guidelines")
        embed1.add_field(inline=False, name="Adhere to VATSIM CoC at all times", value="We ask everyone to show respect to each other at all times. This is Article A1 of the Code of Conduct of the VATSIM Network.\nhttps://www.vatsim.net/documents/code-of-conduct")
        embed1.add_field(inline=False, name="Spam, including images, text, or emotes.", value="Do not send spam in the server, including images, text, or emotes. ")
        
        embed2 = discord.Embed(title="**Nepal vACC Important Links**", colour=discord.Colour(0xff0000))

        embed2.add_field(inline=False, name="Website Link:", value="https://nepalvacc.com/")
        embed2.add_field(inline=False, name="Dashboard Website Link:", value="https://www.members.nepalvacc.com")
        embed2.add_field(inline=False, name="Instagram Account Link:", value="https://www.instagram.com/vatsim_nepal/")
        embed2.add_field(inline=False, name="Facebook Account Link:", value="https://www.facebook.com/NepalvACC")
        embed2.add_field(inline=False, name="Twitter Account Link:", value="https://twitter.com/VatsimN")
        embed2.add_field(inline=False, name="Nepal vACC GDPR Link:", value="https://vats.im/NPLGDPR")
        embed2.add_field(inline=False, name="Nepal vACC Constituion Link:", value="https://vats.im/NPLConstitution")
        embed2.add_field(inline=False, name="Nepal vACC Discord Policy Link:", value="https://vats.im/NPLDiscordPolicy")
        
        embed3 = discord.Embed(title="**Nepal vACC Contact Information**", colour=discord.Colour(0xff0000))
        
        embed3.add_field(inline=False, name="To contact Nepal vACC Director", value="**Bikesh Devkota**\n Nepal vACC Director, ACCNPL1\n director_bikesh@nepalvacc.com")
        embed3.add_field(inline=False, name="To contact Nepal vACC Events & Marketing Director", value="**Ben Pope**\n Nepal vACC Events & Marketing Director, ACCNPL5\n event.director@nepalvacc.com")
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)
        await ctx.send(embed=embed3)
        await ctx.message.delete()
    
    #Policy command
    @commands.command(hidden = True)
    @commands.has_permissions(manage_messages = True)
    async def policy(self, ctx):
        await ctx.send("Nepal vACC Policy v1.1 is available to be viewed through this link: https://www.nepalvacc.com/npl-vacc-policy/")
        await ctx.message.delete()
    
    #meme API
    @commands.command(hidden = True)
    @commands.has_permissions(administrator = True)
    async def meme(self, ctx):
        url = "https://meme-api.herokuapp.com/gimme"
        
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        await ctx.send(data["title"])
                        await ctx.send(data["url"])
                    else:
                        await ctx.send(f"Ohhh I hate this.... :triumph: I got an error. `Err: {response.status} response code`" )
    
    @commands.command()
    @commands.is_owner()
    async def reload_cog(self, ctx, cog: str):
        await ctx.trigger_typing()
        ext = f"{cog}.py"
        if not os.path.exists(f"./cogs/{ext}"):
            await ctx.send(f"{ctx.message.author.name} I could not unload that Cog. Possibly spelling issue...")
        elif ext.endswith(".py") and not ext.startswith("_"):
            try:
                self.bot.unload_extension(f"cogs.{ext[:-3]}")
                self.bot.load_extension(f"cogs.{ext[:-3]}")
            except Exception:
                desired_trace = traceback.format_exc()
                await ctx.send(f"Failed to reload Cog: `{ext}`\nTrackback Error:\n{desired_trace}")
            else:
                await ctx.send(f"{ctx.message.author.name} I successfully reloaded Cog {cog} :repeat: ")
    
    @commands.command()
    @commands.is_owner()
    async def load_cog(self, ctx, cog: str):
        await ctx.trigger_typing()
        ext = f"{cog}.py"
        if not os.path.exists(f"./cogs/{ext}"):
            await ctx.send(f"{ctx.message.author.name} I could not load Cog {cog}. Possibly spelling issue...")
        
        elif ext.endswith(".py") and not ext.startswith("_"):
            try:
                self.bot.load_extension(f"cogs.{ext[:-3]}")
            except Exception:
                desired_trace = traceback.format_exc()
                await ctx.send(f"Failed to log Cog: `{ext}`\nTrackback Error:\n{desired_trace}")
            else:
                await ctx.send(f"{ctx.message.author.name} I successfully loaded Cog {cog} :repeat: ")



def setup(bot):
    bot.add_cog(AdministratorCommands(bot))