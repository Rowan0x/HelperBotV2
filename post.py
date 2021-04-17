import discord
from discord.ext import commands
import json

with open('settings.json', 'r') as file:
    data = json.load(file)

class PostCog(commands.Cog, name = "Post"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def post(self, ctx):
        
        questions = []
                                    

def setup(bot):
    bot.add_cog(PostCog(bot))
    print("Post cog loaded!")