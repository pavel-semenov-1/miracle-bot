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
        i = 1
        s = ''
        for row in self.bot.db_connection.getCursor().execute('SELECT id, steamid32 FROM users ORDER BY id DESC LIMIT 10;'):
            row = row[:-1] + (str(row[-1]),)
            s += str(i) + '. ' + ' '.join(row)
            i += 1
        if not(s):
            s = "No user data available."
        embed.add_field(name='Top-10', value=s)
        await ctx.send(embed=embed)

    @list_command.error
    async def list_command_error(self, ctx, exc):
        raise exc

async def setup(bot):
    await bot.add_cog(General(bot))
