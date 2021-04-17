import discord
from discord.ext import commands
import json

with open('settings.json', 'r') as file:
    data = json.load(file)

class DBCog(commands.Cog, name = "DashBoard"):
    def __init__(self, bot):
        self.bot = bot
    


def setup(bot):
    bot.add_cog(DBCog(bot))
    print("DashBoard cog loaded!")