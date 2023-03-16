import discord
from discord.ext import commands
from datetime import datetime



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    


#help menu
    @commands.command(description = "Self explanatory I think :sweat_smile: ")
    async def Help(self, ctx, commandSent=None):
        if commandSent != None:
            
            for command in self.bot.commands:
                if commandSent.upper() == command.name.upper():

                    paramString = ""

                    for param in command.clean_params:
                        paramString += param + ", "

                    paramString = paramString[:-2]

                    if len(command.clean_params) == 0:
                        paramString = "None"
                        
                    embed=discord.Embed(title=f"How to use command: {command.name}?", description=command.description, colour = discord.Colour(0xff0000) ,timestamp = datetime.utcnow())
                    embed.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.name}")
                    await ctx.send(embed=embed)
    
        else:
            embed=discord.Embed(title="User Help Menu! / SERVER PREFIX = ?", colour = discord.Colour(0xff0000) ,timestamp = datetime.utcnow())
            embed.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.name}")
            embed.add_field(name="Hi:", value="Says hello to a specified user", inline=False)
            embed.add_field(name="Uptime:", value="Returns bot uptime.")
            embed.add_field(name="Ping:", value="Returns time taken by the server to respond back in ms", inline=False)
            embed.add_field(name="Music:", value="Yes, we have music bot implemented as well. For all commands use `?help play`")
            embed.add_field(name="RequestATC:", value="This command is to be only used if you need to request ATC. Run the command `?requestatc` in the <#850055844083007488> channel and the bot will ask you further questions. ", inline=False)
            embed.add_field(name="NepalAIP:", value="Sends you Nepal AIP link in DM", inline=False)
            embed.add_field(name="VNKTCharts:", value="Sends you VNKT (Kathmandu) charts link in DM", inline=False)
            embed.add_field(name="UserInfo:", value="Returns information for the user mentioned. Leave empty to check your information.", inline=False)
            embed.add_field(name="ServerInfo:", value="Returns Nepal vACC server information.", inline=False)
            embed.add_field(name="Metar:", value="Returns metar for the specified ICAO and tries to decode it. *Some information might not be decoded.*", inline=False)
            embed.add_field(name="TAF:", value="Returns TAF for the specified ICAO", inline=False)
            embed.add_field(name="VATSIM:", value="Returns VATSIM member information. Use the command and bot will ask you some questions.", inline=False)
            embed.add_field(name="VATSIMHours:", value="Returns VATSIM member ATC Hours on a specific position. Use the command `?vatsimhours` and bot will ask you some questions.", inline=False)
            embed.add_field(name="Information on a specific command needed?", value="This is not a command but, if you require more information on a specific command use `?help` followed by the command name for more information on that command", inline=False)
            embed.add_field(name="Finally remember:", value="**YOU DO NOT NEED TO USE CASE SENSITIVE COMMANDS**. For example even if you use `?pInG` it will work. Still have any questions? Open a ticket to the IT Team.", inline=False)
            

            await ctx.send(embed=embed)

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Help(bot))