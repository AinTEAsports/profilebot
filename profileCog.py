import re

import discord
from discord.ext import commands, tasks

from jsonHandler import JsonHandler



handler = JsonHandler("./data.json", create_new=True)


class ProfileEmbed(commands.Cog):
    
    def __init__(self, bot : commands.Bot) -> None :
        """Init method for the cog

        Args:
            bot (commands.Bot): bot instance
        """
        
        self.bot = bot


    def __create_profile(self, user : discord.User) -> None :
        """Private method that adds a new empty/default profile into json file

        Args:
            user (discord.User): the user you want to create a profile_embed
        """
        
        default_infos = {  
            "tag" : user.name,
            "thumbnail" : "",
            "mains" : [],
            "secondaries" : [],
            "games" : [],
            "switch-code" : "",
            "region" : "",
            "note" : "",
        }
        
        handler.create_entree(str(user.id), default_infos)


    def __valid_switch_code(self, switch_code : str) -> bool :
        """Private method that returns if a switch code has valid syntax or not

        Args:
            switch_code (str): the switch code

        Returns:
            bool: validity of syntax of switch code
        """
        
        return re.search("SW-(\d{4})-(\d{4})-(\d{4})-(\d{4})", switch_code)


    @commands.command()
    async def tag(self, ctx, new_tag : str = ""):        
        if not handler.key_exists(str(ctx.author.id)):
            self.__create_profile(ctx.author)
            
        if not new_tag:
            actual_tag = handler.get_json()[str(ctx.author.id)]["tag"]
            await ctx.message.reply(f"Your actual tag is `{actual_tag}`")
            return
        
        data = handler.get_json()
        data[str(ctx.author.id)]["tag"] = new_tag
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
        
        
    @commands.command()
    async def thumbnail(self, ctx, url : str = ""):
        if not handler.key_exists(str(ctx.author.id)):
            self.__create_profile(ctx.author)
            
        
        if not url:
            actual_thumbnail = handler.get_json()[str(ctx.author.id)]["thumbnail"]
            
            if actual_thumbnail:
                await ctx.message.reply(f"Your actual thumbnail is : {actual_thumbnail}")
                return
            else:
                await ctx.message.reply(f"You actually have registered no thumbnail, to register one use `{self.bot.command_prefix}thumbnail <your image url here>`")
                return
            
            
        data = handler.get_json()
        data[str(ctx.author.id)]["thumbnail"] = url
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
        

    
    @commands.command()
    async def mains(self, ctx, *mains):
        if not handler.key_exists(str(ctx.author.id)):
            self.__create_profile(ctx.author)
        
        if not mains:
            actual_mains = handler.get_json()[str(ctx.author.id)]["mains"]
            
            if not actual_mains:
                await ctx.message.reply(f"You actually have registered no mains, to register mains use `{self.bot.command_prefix}mains <your mains here>`")
                return
                
            await ctx.message.reply(f"Your actual mains are : `{', '.join(actual_mains)}`")
            return
        
        data = handler.get_json()
        data[str(ctx.author.id)]["mains"] = list(mains)
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
    
    
    @commands.command()
    async def secondaries(self, ctx, *secondaries):
        if not handler.key_exists(str(ctx.author.id)):
            self.__create_profile(ctx.author)
        
        if not secondaries:
            actual_seconds = handler.get_json()[str(ctx.author.id)]["secondaries"]
            
            if not actual_seconds:
                await ctx.message.reply(f"You actually have registered no mains, to register mains use `{self.bot.command_prefix}secondaries <your secondaries here>`")
                return
                
            await ctx.message.reply(f"Your actual mains are : `{', '.join(actual_seconds)}`")
            return
        
        data = handler.get_json()
        data[str(ctx.author.id)]["secondaries"] = list(secondaries)
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
    

    @commands.command()
    async def games(self, ctx, *games):
        if not handler.key_exists(str(ctx.author.id)):
            self.__create_profile(ctx.author)
            
            
        availible_games = [
            "Smash 64",
            "Melee",
            "Brawl",
            "Sm4sh",
            "SSBU",
        ]
        
        
        if not games:
            actual_games = handler.get_json()[str(ctx.author.id)]["games"]
            
            if not actual_games:
                await ctx.message.reply(f"You actually have registered no mains, to register mains use `{self.bot.command_prefix}games <your games here>`")
                return
                
            await ctx.message.reply(f"Your actual mains are : `{', '.join(actual_games)}`")
            return
        
        
        for game in games:
            if game not in availible_games:
                await ctx.message.reply(f"'{game}' is not a valid game. Availible games are : `{', '.join(availible_games)}`")
                return
        
        data = handler.get_json()
        data[str(ctx.author.id)]["games"] = list(games)
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
    
    
    @commands.command()
    async def switch_code(self, ctx, switch_code : str = ""):
        if not handler.key_exists(str(ctx.author.id)):
            self.__create_profile(ctx.author)


        if not switch_code:
            data = handler.get_json()
            actual_switch_code = data[str(ctx.author.id)]["switch-code"]
            
            if actual_switch_code:
                await ctx.message.reply(f"Your actual switch code is : `{actual_switch_code}`")
                return
            else:
                await ctx.message.reply(f"You have no switch code registered, to register one use `{self.bot.command_prefix}switch_code <your switch code here>`")
                return
        
        if not self.__valid_switch_code(switch_code):
            await ctx.message.reply(f"Your switch code is not valid")
            await ctx.message.add_reaction("❌")
            return
        
        data = handler.get_json()
        data[str(ctx.author.id)]["switch code"] = switch_code
        
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
    
    
    @commands.command()
    async def region(self, ctx, region : str = ""):
        if not handler.key_exists(str(ctx.author.id)):
            self.__create_profile(ctx.author)
        
        
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
            data = handler.get_json()
            actual_region = data[str(ctx.author.id)]["region"]
            
            if actual_region:
                await ctx.message.reply(f"Your actual region is : `{actual_region}`")
                return
            else:
                await ctx.message.reply(f"You have no region registered, to register one use `{self.bot.command_prefix}region <your region here>`")
                return
            
        
        if region not in regions:
            await ctx.send(f"```\n'{region}' is not an availible region for the moment or does not exists...```")
            return
        
        
        data = handler.get_json()
        data[str(ctx.author.id)]["region"] = region
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
        
        
    @commands.command()
    async def note(self, ctx, *note):
        if not note:
            data = handler.get_json()
            actual_note = data[str(ctx.author.id)]["note"]
            
            if actual_note:
                await ctx.message.reply(f"Your actual note is : `{actual_note}`")
                return
            else:
                await ctx.message.reply(f"You have no note registered, to register one use `{self.bot.command_prefix}note <your note here>`")
                return

        data = handler.get_json()
        data[str(ctx.author.id)]["note"] = " ".join(note)
        handler.update(data)
        
        await ctx.message.add_reaction("✅")
    
    
    @commands.command()
    async def reset_profile(self, ctx):
        default_infos = {
            "tag" : ctx.author.name,
            "thumbnail" : "",
            "mains" : [],
            "secondaries" : [],
            "games" : [],
            "switch code" : "",
            "region" : "",
            "note" : "",
        }
        
        data = handler.get_json()
        data[str(ctx.author.id)] = default_infos
        handler.update(data)
        
        await ctx.message.add_reaction("✅")


    @commands.command()
    async def profile(self, ctx, user : discord.User = None):
        if not user:
            user = ctx.author
        
        if not handler.key_exists(str(ctx.author.id)):
            self.__create_profile(user)
            
        user_infos = handler.get_json()[str(user.id)]


        profile_embed = discord.Embed()
        
        
        # Adding thumbnail if there is one registered
        if user_infos["thumbnail"]:
            profile_embed.set_thumbnail(url=user_infos["thumbnail"])
        
        
        for key in user_infos.keys():
            info = user_infos[key]

            if info and key != "thumbnail":
                if type(info) == list:
                    for index, element in enumerate(info):
                        info[index] = f"`{element}`"
                    
                    info = ", ".join(info)

                profile_embed.add_field(name=f"**{key.title()}**", value=info, inline=False)
                
                
        profile_embed.set_footer(icon_url=user.avatar_url, text=f"{user.name}'s profile")        
        
        
        await ctx.message.reply(embed=profile_embed)

