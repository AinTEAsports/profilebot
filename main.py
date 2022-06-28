import discord
from discord.ext import commands, tasks

from profileCog import ProfileEmbed


bot = commands.Bot(command_prefix=".sp ", description="A simple bo to test a cog I'm making", help_command=None)



################################# EVENTS #######################################

@bot.event
async def on_ready():
    print(f"Ready, logged in as {bot.user}")



################################# HELP COMMAND #######################################


@bot.command()
async def help(ctx):
    commands = {
        "tag" : "to display/change your current tag",
        "thumbnail" : "to display change your current thumbnail image",
        "mains" : "to display/change your current mains",
        "secondaries" : "to display/change your current secondaries",
        "games" : "to display/change your current games",
        "switch_code" : "to display/change your current switch code",
        "region" : "to display/change your current region",
        "note" : "to display/change your current note",
        "reset_profile" : "to reset your profile",
        "profile" : "to show your profile in a beautiful embed",
    }

    embed_string = ""

    for command, description in commands.items():
        embed_string += f"**{command}** {description}\n"
        
        
    help_embed = discord.Embed(title="__Help embed__")
    help_embed.add_field(name="**Commands :**\n", value=embed_string, inline=False)
    help_embed.set_footer(icon_url=ctx.message.guild.icon_url, text=ctx.message.guild.name)
    
    await ctx.send(embed=help_embed)


################################# COG ADDS #######################################

bot.add_cog(ProfileEmbed(bot))


################################# BOT LAUNCH #######################################

bot.run("TOKEN")

