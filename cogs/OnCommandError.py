import discord
from discord.ext import commands

class OnCommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #if isinstance(error, commands.MissingRequiredArgument):
            #await ctx.send(f"Hmmm, {ctx.message.author.name} I think you are missing something in that command :thinking: `Err: MissingRequiredArugment`")
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Woah you are coming in hot :fire: {ctx.message.author.name}, are you sure you should be running this command? `Err: MissingPermissions`")

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(f"{ctx.message.author.name}, did you made that up? :eyes: You can open a ticket and ask the IT Team to add that command. `Err: CommandNotFound`")
        
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send(f"{ctx.message.author.name}, wait does that channel exist? I thought I had administrator permissions. :thinking: `Err: ChannelNotFound`")

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"{ctx.message.author.name}, Ohhh wait..... I think I don't have that much power. :octopus:  `Err:BotMissingPermissions` ")

        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Oh no. I could not find that user. :see_no_evil: `Err: MemberNotFound` ")
        
        elif isinstance(error, commands.UserNotFound):
            await ctx.send("Oh no. I could not find that user. :see_no_evil: `Err: UserNotFound` ")
        
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"{ctx.message.author.mention} really? :expressionless: This is a command to restart a specific Cog. And I am sure you didn't update any code so just don't do that again....")
        
        #elif isinstance(error, commands.CommandError):
            #await ctx.send("Okay you just caused the program to think twice. :clap: Make sure to check if you are enter numbers only where requested, anything else even a fullstop will also show this error. Still getting the error? Kindly report to IT Team. `Err:GeneralCommandError` ")

        elif isinstance(error, commands.ConversionError):
            await ctx.send("Conversion Failed. `Err:ConversionError`")

        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send("Oops, argument could not be parsed. `Err:ArgumentParsingError`")

        elif isinstance(error, discord.InvalidArgument):
            await ctx.send("Discord just told me I caused an Invalid Argument. `Err:DiscordInvalidArgument`")

        elif isinstance(error, discord.NotFound):
            await ctx.send("Discord just told me the information was not found. `Err:DiscordNotFound`")
        
        else:
            print(f"Oops an error occured. `Err:{error}`")

def setup(bot):
    bot.add_cog(OnCommandError(bot))