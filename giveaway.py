import discord
from discord.ext import commands
import random
import asyncio
import sqlite3
import json

with open('settings.json', 'r') as file:
    data = json.load(file)

class GwCog(commands.Cog, name = "Gw"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gw_channel(self, ctx, id=None):
        if ctx.author.guild_permissions.kick_members:
            if id is None:
                return await ctx.send("Please mention a valid channel ID.")
            if ctx.author.guild_permissions.kick_members:
                try:
                    c_id = int(id)
                    channel = self.bot.get_channel(c_id)
                except:
                    return await ctx.send("An error occured while trying to perform this action, please mention a valid channel ID.")

                if channel is None:
                    return await ctx.send("An error occured while trying to perform this action, please mention a valid channel ID.")
                else:
                    db = sqlite3.connect('main.db')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT guild_id, channel_id FROM gwchannel WHERE guild_id = {ctx.message.guild.id}")
                    result = cursor.fetchone()
                    if result is None:
                        sql = ("INSERT INTO gwchannel(guild_id, channel_id) VALUES(?,?)")
                        val = (ctx.message.guild.id, c_id)
                        cursor.execute(sql, val)
                        db.commit()
                        await ctx.send(f"Successfully set giveaway channel to <#{c_id}>")
                    elif result is not None:
                        sql = (f"UPDATE gwchannel SET guild_id = ?, channel_id = ? WHERE guild_id = ?")
                        val = (ctx.message.guild.id, c_id, ctx.message.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        await ctx.send(f"Successfully set giveaway channel to <#{c_id}>")
            
    
    @commands.command()
    async def giveaway(self, ctx):
        if ctx.author.guild_permissions.kick_members:
            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT guild_id, channel_id FROM gwchannel WHERE guild_id = {ctx.message.guild.id}")
            results = cursor.fetchone()

            if results is None:
                return await ctx.send("You haven't set a giveaway channel, use `$gw_channel [channel ID]` to set it.")

            channel = self.bot.get_channel(int(results[1]))

            def convert(time):
                pos = ["s", "h", "m", "d"]
                time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}

                unit = time[-1]
                
                if unit not in pos:
                    return -1
                try:
                    val = int(time[:-1])
                except:
                    return -2

                return val * time_dict[unit]

            embedColor = 0x00a6ff

            questions = ["What do you want to giveaway?", "How much time do you want the giveaway to last?", "How many winners should there be?"]

            answers = []

            for q in questions:
                embed = discord.Embed(color=embedColor, title="Giveaway", description=q)
                embed.set_thumbnail(url=data['pfp'])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

                try:
                    response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.message.author and m.channel == ctx.message.channel, timeout = 300.0)
                except asyncio.TimeoutError:
                    return
                else:
                    answers.append(response.content)

            time = convert(answers[1])

            if time == -1:
                warnemb = discord.Embed(color=embedColor, title="Error", description="An error occured while trying to perform this action, please mention a valid duration.")
                embed.set_thumbnail(url=data['pfp'])
                return await ctx.send(embed=warnemb)
            elif time == -2:
                warnemb = discord.Embed(color=embedColor, title="Error", description="An error occured while trying to perform this action, please mention a valid duration.")
                embed.set_thumbnail(url=data['pfp'])
                return await ctx.send(embed=warnemb)

            gwembed = discord.Embed(color=embedColor, title=f"Giveaway-{answers[0]}", description="React with 🎉 to join!")
            gwembed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            gwembed.add_field(name="Prize", value=answers[0], inline=False)
            gwembed.add_field(name="Duration", value=answers[1], inline=False)
            gwembed.add_field(name="Number of Winners", value=answers[2], inline=False)
            gwembed.set_thumbnail(url=data['pfp'])

            gwmsg = await channel.send(embed=gwembed)

            await gwmsg.add_reaction("🎉")

            await ctx.send("Succesfully created a giveaway!")

            await asyncio.sleep(time)

            new_msg = await channel.fetch_message(gwmsg.id)

            users = await new_msg.reactions[0].users().flatten()
            users.pop(users.index(self.bot.user))

            try:
                winners = random.sample(users, k=int(answers[2]))
            except:
                return await ctx.send("An error occured while trying to perform this action, number of winners are greater than number of members in the giveaway.")

            winners_string = []
            for w in winners:
                winners_string.append(f"<@!{w.id}>")

            await channel.send(f"Congratulations to {', '.join(winners_string)} for winning {answers[0]}!")

def setup(bot):
    bot.add_cog(GwCog(bot))
    print("Giveaway cog loaded!")