import discord
from discord.ext import commands
import datetime as dt
import aiohttp
import os
import bot.conf as conf

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='list')
    async def list_command(self, ctx):
        embed = discord.Embed(title="List of top users")
        s = '\n'.join(conf.connection.getCursor().execute('SELECT name, steamid32, time FROM users ORDER BY time DESC LIMIT 10;'))
        embed.add_field(name='', value=s)
        await ctx.send(embed=embed)

    @list_command.error
    async def list_command_error(self, ctx, exc):
        pass

def setup(bot):
    bot.add_cog(General(bot))
