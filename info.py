import discord
from discord.ext import commands
import json

with open('settings.json', 'r') as file:
    data = json.load(file)

class HelpCog(commands.Cog, name = "Help"):
    def __init__(self, bot):
        self.bot = bot
    

def setup(bot):
    bot.add_cog(HelpCog(bot))
    print("Help cog loaded!")