import discord
import requests
import random
import sqlite3
from discord.ext import commands
import asyncio
import json

with open('settings.json', 'r') as file:
    data = json.load(file)

class VerifyCog(commands.Cog, name = "Verification"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def verify(self, ctx):
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT guild_id, verifyrole, unverifiedrole FROM verifyrole WHERE guild_id = {ctx.message.guild.id}")
        result = cursor.fetchone()

        verified = ctx.guild.get_role(int(result[1]))
        unverified = ctx.guild.get_role(int(result[2]))

        embedColor = 0x00a6ff
        embed1 = discord.Embed(color=embedColor, title="Verification", description="Please reply with your Roblox username.")
        embed1.set_thumbnail(url=data['pfp'])
        await ctx.send(f"Redirected prompt to your Direct Messages, {ctx.message.author.mention}")
        await ctx.message.author.send(embed=embed1)
        try:
            response = await self.bot.wait_for("message", check=lambda m: m.author == ctx.message.author and isinstance(m.channel, discord.DMChannel), timeout = 300.0)
        except asyncio.TimeoutError:
            return
        else:
            rblx_ui = requests.get(f"https://userapi.js.org/rbx/{response.content}").json()
            if rblx_ui is None:
                return await ctx.message.author.send("This user does not exist.")

            words = ["Helper", "Hello", "Distant", "Desk", "Chair", "Monkey", "Golem", "Spin", "Hour", "Computer", "Spoon", "Imagine", "Cold", "Hot", "Nice", "Nameless", "Mario"]
            chosen_words = random.sample(words, k=6)
            random_string = " ".join(chosen_words)
            
            embed2 = discord.Embed(color=embedColor, title="Verification", description=f"To make sure this is your account, please enter this into your **status** and reply with 'done'. ```{random_string}```")
            embed2.set_thumbnail(url=data['pfp'])
            embed2.set_image(url="https://cdn.discordapp.com/attachments/794895902580932618/829348649908568114/exgif.gif")
            await ctx.message.author.send(embed=embed2)
            try:
                response2 = await self.bot.wait_for("message", check=lambda m: m.author == ctx.message.author and isinstance(m.channel, discord.DMChannel), timeout = 300.0)
            except asyncio.TimeoutError:
                return
            else:
                if not response2.content.lower() == "done":
                    cancelembed = discord.Embed(color=0xf50000, title="Not Verified", description="You have not been verified.")
                    cancelembed.set_thumbnail(url=data['pfp'])
                    return await ctx.message.author.send(embed=cancelembed)

                rblx_ui = requests.get(f"https://userapi.js.org/rbx/{response.content}").json()

                if rblx_ui['description'] == random_string:
                    db = sqlite3.connect('main.db')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT guild_id, user_id, rblx FROM verifyinfo WHERE guild_id = {ctx.message.guild.id} AND user_id = {ctx.message.author.id}")
                    result = cursor.fetchone()

                    if result is None:
                        sql = ("INSERT INTO verifyinfo(guild_id, user_id, rblx) VALUES(?,?,?)")
                        val = (ctx.message.guild.id, ctx.message.author.id, rblx_ui['name'])
                        cursor.execute(sql, val)
                        db.commit()
                    elif result is not None:
                        sql = (f"UPDATE verifyinfo SET guild_id = ?, user_id = ?, rblx = ? WHERE guild_id = ? AND user_id = {ctx.message.author.id}")
                        val = (ctx.message.guild.id, ctx.message.author.id, rblx_ui['name'], ctx.message.guild.id)
                        cursor.execute(sql, val)
                        db.commit()

                    embed3 = discord.Embed(color=embedColor, title=f"Hello {rblx_ui['name']}", description=f"You have been succesfully verified as {rblx_ui['name']}!")
                    embed3.set_thumbnail(url=data['pfp'])
                    await ctx.message.author.send(embed=embed3)
                    await ctx.message.author.edit(nick=rblx_ui['name'])
                    try:
                        await ctx.message.author.remove_roles(unverified)
                        await ctx.message.author.add_roles(verified)
                    except:
                        return

                elif not rblx_ui['description'] == random_string:

                    cancelembed = discord.Embed(color=0xf50000, title="Not Verified", description="You have not been verified.")
                    cancelembed.set_thumbnail(url=data['pfp'])
                    return await ctx.message.author.send(embed=cancelembed)

    @commands.command()
    async def rblx(self, ctx, user: discord.Member=None):
        if user is None:
            embedColor = 0x00a6ff

            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT guild_id, user_id, rblx FROM verifyinfo WHERE guild_id = {ctx.message.guild.id} AND user_id = {ctx.message.author.id}")
            result = cursor.fetchone()

            if result is None:
                return await ctx.send("This user hasn't been verified yet.")

            ui = requests.get(f"https://userapi.js.org/rbx/{result[2]}").json()
            infoembed = discord.Embed(color=embedColor, title="User Info")
            infoembed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            #infoembed.set_thumbnail(url=data['pfp'])
            infoembed.add_field(name="UserID", value=ui['id'], inline=True)
            infoembed.add_field(name="Name", value=ui['name'], inline=True)
            infoembed.add_field(name="Display Name", value=ui['displayname'], inline=True)
            infoembed.add_field(name="Profile", value=f"[Link]({ui['url']})", inline=True)
            infoembed.set_image(url=ui['avatar'])
            infoembed.add_field(name="Status", value=ui['status'], inline=True)
            infoembed.add_field(name="Description", value=ui['description'], inline=True)
            infoembed.add_field(name="Friends", value=ui['friends'], inline=True)
            infoembed.add_field(name="Followers", value=ui['followers'], inline=True)
            infoembed.add_field(name="Following", value=ui['following'], inline=True)
            infoembed.add_field(name="Account Age", value=ui['age'], inline=True)
            infoembed.add_field(name="Created", value=ui['created'], inline=True)

            await ctx.send(embed=infoembed)
        elif user is not None:
            embedColor = 0x00a6ff

            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT guild_id, user_id, rblx FROM verifyinfo WHERE guild_id = {ctx.message.guild.id} AND user_id = {user.id}")
            result = cursor.fetchone()

            if result is None:
                return await ctx.send("This user hasn't been verified yet.")

            ui = requests.get(f"https://userapi.js.org/rbx/{result[2]}").json()
            infoembed = discord.Embed(color=embedColor, title="User Info")
            infoembed.set_author(name=user.name, icon_url=user.avatar_url)
            #infoembed.set_thumbnail(url=data['pfp'])
            infoembed.add_field(name="UserID", value=ui['id'], inline=True)
            infoembed.add_field(name="Name", value=ui['name'], inline=True)
            infoembed.add_field(name="Display Name", value=ui['displayname'], inline=True)
            infoembed.add_field(name="Profile", value=f"[Link]({ui['url']})", inline=True)
            infoembed.set_image(url=ui['avatar'])
            infoembed.add_field(name="Status", value=ui['status'], inline=True)
            infoembed.add_field(name="Description", value=ui['description'], inline=True)
            infoembed.add_field(name="Friends", value=ui['friends'], inline=True)
            infoembed.add_field(name="Followers", value=ui['followers'], inline=True)
            infoembed.add_field(name="Following", value=ui['following'], inline=True)
            infoembed.add_field(name="Account Age", value=ui['age'], inline=True)
            infoembed.add_field(name="Created", value=ui['created'], inline=True)

            await ctx.send(embed=infoembed)
        
    
    @commands.command()
    async def verified_role(self, ctx, id=None):
        if ctx.author.guild_permissions.kick_members:
            if id is None:
                return await ctx.send("Please mention a valid role ID.")
            if ctx.author.guild_permissions.kick_members:
                try:
                    r_id = int(id)
                    role = ctx.guild.get_role(r_id)
                except:
                    return await ctx.send("An error occured while trying to perform this action, please mention a valid role ID.")

                if role is None:
                    return await ctx.send("An error occured while trying to perform this action, please mention a valid role ID.")
                else:
                    db = sqlite3.connect('main.db')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT guild_id, verifyrole, unverifiedrole FROM verifyrole WHERE guild_id = {ctx.message.guild.id}")
                    result = cursor.fetchone()
                    if result is None:
                        sql = ("INSERT INTO verifyrole(guild_id, verifyrole) VALUES(?,?)")
                        val = (ctx.message.guild.id, r_id)
                        cursor.execute(sql, val)
                        db.commit()
                        await ctx.send(f"Successfully set verified role to {role.mention}")
                    elif result is not None:
                        sql = (f"UPDATE verifyrole SET guild_id = ?, verifyrole = ? WHERE guild_id = ?")
                        val = (ctx.message.guild.id, r_id, ctx.message.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        await ctx.send(f"Successfully set verified role to {role.mention}")

    @commands.command()
    async def unverified_role(self, ctx, id=None):
        if ctx.author.guild_permissions.kick_members:
            if id is None:
                return await ctx.send("Please mention a valid role ID.")
            if ctx.author.guild_permissions.kick_members:
                try:
                    r_id = int(id)
                    role = ctx.guild.get_role(r_id)
                except:
                    return await ctx.send("An error occured while trying to perform this action, please mention a valid role ID.")

                if role is None:
                    return await ctx.send("An error occured while trying to perform this action, please mention a valid role ID.")
                else:
                    db = sqlite3.connect('main.db')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT guild_id, verifyrole, unverifiedrole FROM verifyrole WHERE guild_id = {ctx.message.guild.id}")
                    result = cursor.fetchone()
                    if result is None:
                        sql = ("INSERT INTO verifyrole(guild_id, unverifiedrole) VALUES(?,?)")
                        val = (ctx.message.guild.id, r_id)
                        cursor.execute(sql, val)
                        db.commit()
                        await ctx.send(f"Successfully set unverified role to {role.mention}")
                    elif result is not None:
                        sql = (f"UPDATE verifyrole SET guild_id = ?, unverifiedrole = ? WHERE guild_id = ?")
                        val = (ctx.message.guild.id, r_id, ctx.message.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        await ctx.send(f"Successfully set unverified role to {role.mention}")
            


def setup(bot):
    bot.add_cog(VerifyCog(bot))
    print("Verification cog loaded!")