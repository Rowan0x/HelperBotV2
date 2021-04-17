import discord
import sqlite3
import asyncio
from discord.ext import commands
import json
import datetime
from datetime import date

with open('settings.json', 'r') as file:
    data = json.load(file)

class ModCog(commands.Cog, name = "Mod"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def log_channel(self, ctx, id=None):
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
                    cursor.execute(f"SELECT guild_id, channel_id FROM logschannel WHERE guild_id = {ctx.message.guild.id}")
                    result = cursor.fetchone()
                    if result is None:
                        sql = ("INSERT INTO logschannel(guild_id, channel_id) VALUES(?,?)")
                        val = (ctx.message.guild.id, c_id)
                        cursor.execute(sql, val)
                        db.commit()
                        await ctx.send(f"Successfully set logs channel to <#{c_id}>")
                    elif result is not None:
                        sql = (f"UPDATE logschannel SET guild_id = ?, channel_id = ? WHERE guild_id = ?")
                        val = (ctx.message.guild.id, c_id, ctx.message.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        await ctx.send(f"Successfully set logs channel to <#{c_id}>")

    @commands.command()
    async def mute_role(self, ctx, id=None):
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
                    cursor.execute(f"SELECT guild_id, role_id FROM muterole WHERE guild_id = {ctx.message.guild.id}")
                    result = cursor.fetchone()
                    if result is None:
                        sql = ("INSERT INTO muterole(guild_id, role_id) VALUES(?,?)")
                        val = (ctx.message.guild.id, r_id)
                        cursor.execute(sql, val)
                        db.commit()
                        await ctx.send(f"Successfully set logs channel to {role.mention}")
                    elif result is not None:
                        sql = (f"UPDATE muterole SET guild_id = ?, role_id = ? WHERE guild_id = ?")
                        val = (ctx.message.guild.id, r_id, ctx.message.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        await ctx.send(f"Successfully set mute role to {role.mention}")
    
    @commands.command()
    async def kick(self, ctx, usr: discord.User=None, *, reason=None):

        embedColor = 0x00a6ff
        
        if ctx.author.guild_permissions.kick_members:
            try:
                id_check = user.id
            except:
                return await ctx.send("Please mention a valid user and reason.")
            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT guild_id, channel_id FROM logschannel WHERE guild_id = {ctx.message.guild.id}")
            results = cursor.fetchone()

            log_channel = self.bot.get_channel(int(results[1]))
            if usr is None:
                return await ctx.send("An error occured while trying to perform this action, please mention a valid user.")
            elif usr is not None:
                if reason is None:
                    embed = discord.Embed(color=embedColor, title="Kick", description=f"{usr.mention} has been kicked from this guild ✅\n```Unspecified```")
                    embed.set_author(name = usr, icon_url = usr.avatar_url)
                    embed.set_thumbnail(url = data['pfp'])
                    await ctx.send(embed=embed)
                    try:
                        await usr.kick(reason="Unspecified")
                    except:
                        return await ctx.send('An error occured while trying to perform this action, please mention a valid user.')

                    await log_channel.send(embed=embed)

                elif reason is not None:
                    embed = discord.Embed(color=embedColor, title="Kick", description=f"{usr.mention} has been kicked from this guild ✅\n```{reason}```")
                    embed.set_author(name = usr, icon_url = usr.avatar_url)
                    embed.set_thumbnail(url = data['pfp'])
                    await usr.kick(reason=reason)
                    await ctx.send(embed=embed)
                    if log_channel is None:
                        return
                    await log_channel.send(embed=embed)
        else:
            return await ctx.send("You don't have permission to use this command.")

    @commands.command()
    async def ban(self, ctx, usr: discord.User=None, *, reason=None):
        
        embedColor = 0x00a6ff
        if ctx.author.guild_permissions.ban_members:
            try:
                id_check = user.id
            except:
                return await ctx.send("Please mention a valid user and reason.")


            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT guild_id, channel_id FROM logschannel WHERE guild_id = {ctx.message.guild.id}")
            results = cursor.fetchone()

            log_channel = self.bot.get_channel(int(results[1]))
            if usr is None:
                return await ctx.send("An error occured while trying to perform this action, please mention a valid user.")
            elif usr is not None:
                if reason is None:
                    embed = discord.Embed(color=embedColor, title="Ban", description=f"{usr.mention} has been kicked from this guild ✅\n```Unspecified```")
                    embed.set_author(name = usr, icon_url = usr.avatar_url)
                    embed.set_thumbnail(url = data['pfp'])
                    await ctx.send(embed=embed)
                    try:
                        await usr.ban(reason="Unspecified")
                    except:
                        return await ctx.send('An error occured while trying to perform this action, please mention a valid user.')

                    await log_channel.send(embed=embed)

                elif reason is not None:
                    embed = discord.Embed(color=embedColor, title="Ban", description=f"{usr.mention} has been kicked from this guild ✅\n```{reason}```")
                    embed.set_author(name = usr, icon_url = usr.avatar_url)
                    embed.set_thumbnail(url = data['pfp'])
                    await usr.ban(reason=reason)
                    await ctx.send(embed=embed)
                    if log_channel is None:
                        return
                    await log_channel.send(embed=embed)
        else:
            return await ctx.send("You don't have permission to use this command.")

    @commands.command()
    async def mute(self, ctx, usr: discord.User=None, *, time=None):

        embedColor = 0x00a6ff
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT guild_id, role_id FROM muterole WHERE guild_id = {ctx.message.guild.id}")
        results = cursor.fetchone()

        mute_role = ctx.guild.get_role(int(results[1]))

        if mute_role is None:
            return await ctx.send("You haven't set a mute role, use `$mute_role [role ID]` to set it.")

        if ctx.author.guild_permissions.ban_members:
            try:
                id_check = user.id
            except:
                return await ctx.send("Please mention a valid user and duration.")
            
            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT guild_id, channel_id FROM logschannel WHERE guild_id = {ctx.message.guild.id}")
            result = cursor.fetchone()

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

            log_channel = self.bot.get_channel(int(result[1]))
            if usr is None:
                return await ctx.send("An error occured while trying to perform this action, please mention a valid user.")
            elif usr is not None:
                if time is None:
                    return await ctx.send("Please mention a valid duration (s|m|h|d).")

                secs = convert(time)

                if secs == -1:
                    return await ctx.send("Please mention a valid duration (s|m|h|d)")
                elif secs == -2:
                    return await ctx.send("Please mention a valid duration (s|m|h|d)")

                embed = discord.Embed(color=embedColor, title="Muted", description=f"{usr.mention} has been muted for {time} ✅")
                embed.set_author(name = usr, icon_url = usr.avatar_url)
                embed.set_thumbnail(url = data['pfp'])
                await ctx.send(embed=embed)
                try:
                    await usr.add_roles(mute_role)
                except:
                    return await ctx.send("An error occured while performing this actiion")
                try:
                    await log_channel.send(embed=embed)
                except:
                    print("welp")

                await asyncio.sleep(secs)

                embed = discord.Embed(color=embedColor, title="Unmuted", description=f"{usr.mention} has been unmuted ✅")
                embed.set_author(name = usr, icon_url = usr.avatar_url)
                embed.set_thumbnail(url = data['pfp'])
                await usr.remove_roles(mute_role)
                try:
                    await log_channel.send(embed=embed)
                except:
                    return
        else:
            return await ctx.send("You don't have permission to use this command.")

    @commands.command()
    async def warn(self, ctx, user: discord.Member=None, *, reason=None):
        if not ctx.author.guild_permissions.ban_members:
            return await ctx.send("You don't have permission to use this command.")


        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT guild_id, channel_id FROM logschannel WHERE guild_id = {ctx.message.guild.id}")
        result = cursor.fetchone()

        log_channel = self.bot.get_channel(int(result[1]))

        embedColor = 0x00a6ff

        if user is None:
            return await ctx.send("Please mention a valid user.")
        if reason is None:
            return await ctx.send("Please add a reason.")

        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT guild_id, user_id, warns FROM userwarns WHERE guild_id = {ctx.message.guild.id} AND user_id = {user.id}")
        results = cursor.fetchone()

        if results is None:
            timestamp = str(date.today())
            sql = ("INSERT INTO userwarns(guild_id, user_id, warns) VALUES(?,?,?)")
            val = (ctx.message.guild.id, user.id, f"» {reason} ~ <@!{ctx.message.author.id}> | {timestamp}")
            cursor.execute(sql, val)
            db.commit()

            warnembed = discord.Embed(color=embedColor, title="Warn", description=f"{user.mention} has been warned. ```{reason}```")
            warnembed.set_thumbnail(url=data['pfp'])
            warnembed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=warnembed)
            try:
                await log_channel.send(embed=warnembed)
            except:
                print("sad")

            warnembed2 = discord.Embed(color=embedColor, title="Warn", description=f"You have been warned. ```{reason}```")
            warnembed2.set_thumbnail(url=data['pfp'])
            warnembed2.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await user.send(embed=warnembed2)

            return
        if results[2] == "This user has no infractions.":
            timestamp = str(date.today())
            sql = (f"UPDATE userwarns SET warns = ? WHERE guild_id = ? AND user_id = ?")
            val = (f"» {reason} ~ <@!{ctx.message.author.id}> | {timestamp}", ctx.message.guild.id, ctx.message.author.id)
            cursor.execute(sql, val)
            db.commit()

            warnembed = discord.Embed(color=embedColor, title="Warn", description=f"{user.mention} has been warned. ```{reason}```")
            warnembed.set_thumbnail(url=data['pfp'])
            warnembed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=warnembed)
            try:
                await log_channel.send(embed=warnembed)
            except:
                print("sad")

            warnembed2 = discord.Embed(color=embedColor, title="Warn", description=f"You have been warned. ```{reason}```")
            warnembed2.set_thumbnail(url=data['pfp'])
            warnembed2.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await user.send(embed=warnembed2)

            return
        if results[2] is not None and not results[2] == "This user has no infractions.":
            timestamp = str(date.today())
            new_reason = results[2] + f"////» {reason} ~ <@!{ctx.message.author.id}> | {timestamp}"
            sql = (f"UPDATE userwarns SET warns = ? WHERE guild_id = ? AND user_id = ?")
            val = (new_reason, ctx.message.guild.id, ctx.message.author.id)
            cursor.execute(sql, val)
            db.commit()

            warnembed = discord.Embed(color=embedColor, title="Warn", description=f"{user.mention} has been warned. ```{reason}```")
            warnembed.set_thumbnail(url=data['pfp'])
            warnembed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=warnembed)
            try:
                await log_channel.send(embed=warnembed)
            except:
                print("sad")

            warnembed2 = discord.Embed(color=embedColor, title="Warn", description=f"You have been warned. ```{reason}```")
            warnembed2.set_thumbnail(url=data['pfp'])
            warnembed2.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await user.send(embed=warnembed2)
            return
        
    @commands.command()
    async def infractions(self, ctx, user: discord.Member=None):
        if user is not None:
            embedColor = 0x00a6ff
            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT guild_id, user_id, warns FROM userwarns WHERE guild_id = {ctx.message.guild.id} AND user_id = {user.id}")
            results = cursor.fetchone()

            if results[2] is not None:
                warns_list = results[2].split('////')
                warns_final = "\n".join(warns_list)
                if warns_final is None:
                    print("none")
                    embed1 = discord.Embed(color=embedColor, title="Infractions", description="This user has no infractions.")
                    embed1.set_thumbnail(url=data['pfp'])
                    embed1.set_author(name=user.name, icon_url=user.avatar_url)
                    return await ctx.send(embed=embed1)

                embed = discord.Embed(color=embedColor, title="Infractions", description=warns_final)
                embed.set_thumbnail(url=data['pfp'])
                embed.set_author(name=user.name, icon_url=user.avatar_url)
                await ctx.send(embed=embed)
            elif results[2] is None:
                embed = discord.Embed(color=embedColor, title="Infractions", description="This user has no infractions.")
                embed.set_thumbnail(url=data['pfp'])
                embed.set_author(name=user.name, icon_url=user.avatar_url)
                await ctx.send(embed=embed)
        elif user is None:
            embedColor = 0x00a6ff
            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT guild_id, user_id, warns FROM userwarns WHERE guild_id = {ctx.message.guild.id} AND user_id = {ctx.message.author.id}")
            results = cursor.fetchone()

            if results is not None:
                warns_list = results[2].split('////')
                warns_final = "\n".join(warns_list)

                embed = discord.Embed(color=embedColor, title="Infractions", description=warns_final)
                embed.set_thumbnail(url=data['pfp'])
                embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=embed)
            elif results is None:
                embed = discord.Embed(color=embedColor, title="Infractions", description="This user has no infractions.")
                embed.set_thumbnail(url=data['pfp'])
                embed.set_author(name=user.name, icon_url=user.avatar_url)
                await ctx.send(embed=embed)

    @commands.command()
    async def delwarn(self, ctx, user: discord.Member=None, warn_id=None):
        if not ctx.author.guild_permissions.kick_members:
            return await ctx.send("You don't have permission to use this command")
        try:
            id_check = user.id
        except:
            return await ctx.send("Please mention a valid user and warn ID.")

        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT guild_id, channel_id FROM logschannel WHERE guild_id = {ctx.message.guild.id}")
        result = cursor.fetchone()

        log_channel = self.bot.get_channel(int(result[1]))

        embedColor = 0x00a6ff
        if user is None:
            return await ctx.send("Please mention a valid user.")
        if warn_id is None:
            return await ctx.send("Please mention a valid warn ID.")

        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT guild_id, user_id, warns FROM userwarns WHERE guild_id = {ctx.message.guild.id} AND user_id = {user.id}")
        results = cursor.fetchone()

        if results is None or results[2] == "This user has no infractions.":
            return await ctx.send("This user has no infractions.")

        new_list = results[2].split("////")
            
        try:
            indexnumber = int(warn_id)-1
            if len(new_list) == 1:
                new_list.pop(indexnumber)
                new_list.append("This user has no infractions.")
            elif not len(new_list) == 1:   
                new_list.pop(indexnumber)
        except:
            return await ctx.send("The mentioned warn ID does not exist.")
        new_warn_string = "\n".join(new_list)

        sql = (f"UPDATE userwarns SET warns = ? WHERE guild_id = ? AND user_id = ?")
        val = (new_warn_string, ctx.message.guild.id, user.id)
        cursor.execute(sql, val)
        db.commit()

        delembed = discord.Embed(color=embedColor, title=f"Deleted Warning", description=f"Succesfully deleted warning {warn_id} from {user.mention}")
        await ctx.send(embed=delembed)
        await log_channel.send(embed=delembed)

    @commands.command()
    async def clearwarns(self, ctx, user: discord.Member=None):
        try:
            id_check = user.id
        except:
            return await ctx.send("Please mention a valid user and warn ID.")

        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT guild_id, channel_id FROM logschannel WHERE guild_id = {ctx.message.guild.id}")
        result = cursor.fetchone()

        log_channel = self.bot.get_channel(int(result[1]))

        if not ctx.author.guild_permissions.kick_members:
            return await ctx.send("You don't have permission to use this command")
        embedColor = 0x00a6ff

        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT guild_id, user_id, warns FROM userwarns WHERE guild_id = {ctx.message.guild.id} AND user_id = {user.id}")
        results = cursor.fetchone()

        if results[2] == "This user has no infractions.":
            return await ctx.send("This user has no infractions.")

        if results is None:
            return await ctx.send("This user has no infractions.")

        listwarns = results[2].split("////")

        warn_len = len(listwarns)

        new_txt = "This user has no infractions."

        sql = (f"UPDATE userwarns SET warns = ? WHERE guild_id = ? AND user_id = ?")
        val = (new_txt, ctx.message.guild.id, user.id)
        cursor.execute(sql, val)
        db.commit()

        embed = discord.Embed(color=embedColor, title="Cleard Warns", description=f"Succesfully cleared {warn_len} warning(s) from {user.mention}.")
        await ctx.send(embed=embed)
        await log_channel.send(embed=embed)



def setup(bot):
    bot.add_cog(ModCog(bot))
    print("Mod cog loaded!")