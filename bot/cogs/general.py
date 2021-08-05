import discord
from discord.ext import commands
import datetime as dt
import aiohttp
import os
import bot.conf as conf
from bot.ext import tasks

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=1)
    async def update_user_db(self):
        pass # TODO

    @commands.command(name='list')
    async def list_command(self, ctx):
        embed = discord.Embed(title="List of top users")
        i = 1
        s = ''
        for row in conf.connection.getCursor().execute('SELECT name, steamid32, time FROM users ORDER BY time DESC LIMIT 10 WHERE guild_id=?;', (ctx.message.guild.id)):
            row = row[:-1] + (str(row[-1]),)
            s += str(i) + '. ' + ' '.join(row)
            i += 1
        if not(s):
            s = "No user data available."
        embed.add_field(name='Top-10', value=s)
        await ctx.send(embed=embed)

    @list_command.error
    async def list_command_error(self, ctx, exc):
        pass # TODO

def setup(bot):
    bot.add_cog(General(bot))
