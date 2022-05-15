import re

import discord
from discord.ext import commands, tasks

from jsonHandler import JsonHandler



handler = JsonHandler("data.json", createNew=True)


class ProfileEmbed(commands.Cog):
    
    def __init__(self, bot : commands.Bot) -> None :
        self.bot = bot
    
    
    def __createProfile(self, user : discord.User) -> None :
        defaultInfos = {
            "tag" : user.name,
            "thumbnail" : "",
            "mains" : [],
            "secondaries" : [],
            "games" : [],
            "switch-code" : "",
            "region" : "",
            "note" : "",
        }
        
        handler.createEntree(str(user.id), defaultInfos)


    def __validSwitchcode(self, switchCode : str) -> bool :
        return re.search("SW-(\d{4})-(\d{4})-(\d{4})-(\d{4})", switchCode)
    

    @commands.command()
    async def hello(self, ctx) -> None :
        await ctx.send(f"Hello {ctx.author.mention} !")


    @commands.command()
    async def tag(self, ctx, newTag : str = "") -> None:        
        if not handler.keyExists(str(ctx.author.id)):
            self.__createProfile(ctx.author)
            
        if not newTag:
            actualTag = handler.getJSON()[str(ctx.author.id)]["tag"]
            await ctx.message.reply(f"Your actual tag is `{actualTag}`")
            return
        
        data = handler.getJSON()
        data[str(ctx.author.id)]["tag"] = newTag
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
        
        
    @commands.command()
    async def thumbnail(self, ctx, url : str = ""):
        if not handler.keyExists(str(ctx.author.id)):
            self.__createProfile(ctx.author)
            
        
        if not url:
            actualThumbnail = handler.getJSON()[str(ctx.author.id)]["thumbnail"]
            
            if actualThumbnail:
                await ctx.message.reply(f"Your actual thumbnail is : {actualThumbnail}")
                return
            else:
                await ctx.message.reply(f"You actually have registered no thumbnail, to register one use `{self.bot.command_prefix}thumbnail <your image url here>`")
                return
            
            
        data = handler.getJSON()
        data[str(ctx.author.id)]["thumbnail"] = url
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
        

    
    @commands.command()
    async def mains(self, ctx, *mains):
        if not handler.keyExists(str(ctx.author.id)):
            self.__createProfile(ctx.author)
        
        if not mains:
            actualMains = handler.getJSON()[str(ctx.author.id)]["mains"]
            
            if not actualMains:
                await ctx.message.reply(f"You actually have registered no mains, to register mains use `{self.bot.command_prefix}mains <your mains here>`")
                return
                
            await ctx.message.reply(f"Your actual mains are : `{', '.join(actualMains)}`")
            return
        
        data = handler.getJSON()
        data[str(ctx.author.id)]["mains"] = list(mains)
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
    
    
    @commands.command()
    async def secondaries(self, ctx, *secondaries):
        if not handler.keyExists(str(ctx.author.id)):
            self.__createProfile(ctx.author)
        
        if not secondaries:
            actualSeconds = handler.getJSON()[str(ctx.author.id)]["secondaries"]
            
            if not actualSeconds:
                await ctx.message.reply(f"You actually have registered no mains, to register mains use `{self.bot.command_prefix}secondaries <your secondaries here>`")
                return
                
            await ctx.message.reply(f"Your actual mains are : `{', '.join(actualSeconds)}`")
            return
        
        data = handler.getJSON()
        data[str(ctx.author.id)]["secondaries"] = list(secondaries)
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
    

    @commands.command()
    async def games(self, ctx, *games):
        if not handler.keyExists(str(ctx.author.id)):
            self.__createProfile(ctx.author)
            
            
        availibleGames = [
            "Smash 64",
            "Melee",
            "Brawl",
            "Sm4sh",
            "SSBU",
        ]
        
        
        if not games:
            actualGames = handler.getJSON()[str(ctx.author.id)]["games"]
            
            if not actualGames:
                await ctx.message.reply(f"You actually have registered no mains, to register mains use `{self.bot.command_prefix}games <your games here>`")
                return
                
            await ctx.message.reply(f"Your actual mains are : `{', '.join(actualGames)}`")
            return
        
        
        for game in games:
            if game not in availibleGames:
                await ctx.message.reply(f"'{game}' is not a valid game. Availible games are : `{', '.join(availibleGames)}`")
                return
        
        data = handler.getJSON()
        data[str(ctx.author.id)]["games"] = list(games)
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
    
    
    @commands.command()
    async def switch_code(self, ctx, switchCode : str = ""):
        if not handler.keyExists(str(ctx.author.id)):
            self.__createProfile(ctx.author)


        if not switchCode:
            data = handler.getJSON()
            actualSwitchCode = data[str(ctx.author.id)]["switch-code"]
            
            if actualSwitchCode:
                await ctx.message.reply(f"Your actual switch code is : `{actualSwitchCode}`")
                return
            else:
                await ctx.message.reply(f"You have no switch code registered, to register one use `{self.bot.command_prefix}switch_code <your switch code here>`")
                return
        
        if not self.__validSwitchcode(switchCode):
            await ctx.message.reply(f"Your switch code is not valid")
            await ctx.message.add_reaction("❌")
            return
        
        data = handler.getJSON()
        data[str(ctx.author.id)]["switch code"] = switchCode
        
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
    
    
    @commands.command()
    async def region(self, ctx, region : str = ""):
        if not handler.keyExists(str(ctx.author.id)):
            self.__createProfile(ctx.author)
        
        
        regions = [
            'Europe',
            'Asia',
            'North America',
            'Center America',
            'South America',
            'Africa',
            'Antarctica'
        ]
        
        
        if not region:
            data = handler.getJSON()
            actualRegion = data[str(ctx.author.id)]["region"]
            
            if actualRegion:
                await ctx.message.reply(f"Your actual region is : `{actualRegion}`")
                return
            else:
                await ctx.message.reply(f"You have no region registered, to register one use `{self.bot.command_prefix}region <your region here>`")
                return
            
        
        if region not in regions:
            await ctx.send(f"```\n'{region}' is not an availible region for the moment or does not exists...```")
            return
        
        
        data = handler.getJSON()
        data[str(ctx.author.id)]["region"] = region
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
        
        
    @commands.command()
    async def note(self, ctx, *note):
        if not note:
            data = handler.getJSON()
            actualNote = data[str(ctx.author.id)]["note"]
            
            if actualNote:
                await ctx.message.reply(f"Your actual note is : `{actualNote}`")
                return
            else:
                await ctx.message.reply(f"You have no note registered, to register one use `{self.bot.command_prefix}note <your note here>`")
                return

        data = handler.getJSON()
        data[str(ctx.author.id)]["note"] = " ".join(note)
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
    
    
    @commands.command()
    async def reset_profile(self, ctx):
        defaultInfos = {
            "tag" : ctx.author.name,
            "thumbnail" : "",
            "mains" : [],
            "secondaries" : [],
            "games" : [],
            "switch code" : "",
            "region" : "",
            "note" : "",
        }
        
        data = handler.getJSON()
        data[str(ctx.author.id)] = defaultInfos
        handler.update(data)
        
        await ctx.message.add_reaction("✅")


    @commands.command()
    async def profile(self, ctx, user : discord.User = None):
        if not user:
            user = ctx.author
        
        if not handler.keyExists(str(ctx.author.id)):
            self.__createProfile(user)
            
        userInfos = handler.getJSON()[str(user.id)]


        profileEmbed = discord.Embed()
        
        
        # Adding thumbnail if there is one registered
        if userInfos["thumbnail"]:
            profileEmbed.set_thumbnail(url=userInfos["thumbnail"])
        
        
        for key in userInfos.keys():
            info = userInfos[key]

            if info and key != "thumbnail":
                if type(info) == list:
                    for index, element in enumerate(info):
                        info[index] = f"`{element}`"
                    
                    info = ", ".join(info)

                profileEmbed.add_field(name=f"**{key.title()}**", value=info, inline=False)
                
                
        profileEmbed.set_footer(icon_url=user.avatar_url, text=f"{user.name}'s profile")        
        
        
        await ctx.message.reply(embed=profileEmbed)

