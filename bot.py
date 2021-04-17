import discord
import traceback
import sys
from discord.ext import commands
import json

with open('settings.json', 'r') as file:
    data = json.load(file)

bot = commands.Bot(command_prefix =  data['prefix'], case_sensitive = False)
client = discord.Client()


bot.remove_command('help')

initial_extensions = ['cogs.giveaway', 'cogs.moderation', 'cogs.help', 'cogs.verification']

if __name__ == '__main__':
    for extension in initial_extensions:
       try:
           bot.load_extension(extension)
       except Exception as e:
           print(f"Failed to load extension {extension}", file = sys.stderr)
           traceback.print_exc()


@bot.event
async def on_ready():
    print(f"{data['name']} bot is online!")
    return await bot.change_presence(activity = discord.Activity(type = 2, name = 'to a song 😎'))

bot.run(data['token'])