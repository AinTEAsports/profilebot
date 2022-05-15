import discord
from discord.ext import commands, tasks

from profileCog import ProfileEmbed


bot = commands.Bot(command_prefix=".sp ", description="A simple bo to test a cog I'm making")



################################# EVENTS #######################################


@bot.event
async def on_ready():
    print(f"Ready, logged in as {bot.user}")



################################# COG ADDS #######################################

bot.add_cog(ProfileEmbed(bot))


################################# BOT LAUNCH #######################################

bot.run("token")
