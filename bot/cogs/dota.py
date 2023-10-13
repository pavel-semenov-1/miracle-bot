import discord
from discord.ext import commands
import datetime as dt
import aiohttp
import os
import typing as t

import bot.conf as conf
import bot.cogs.utils.dotaimage as dotaimage

class StratzMatchNotParsedError(commands.CommandError):
    pass

async def get_stratz_match(bot, match_id):
    url = f"https://api.stratz.com/api/v1/match/{match_id}"
    try:
        result = await bot.http_client.get(url, cache=True, headers={"Authorization": f"Bearer {conf.STRATZ_TOKEN}"}, errors={500: "Looks like something wrong with the STRATZ api", 204: "STRATZ hasn't recieved this match yet. Try again a bit later"})
        return result
    except aiohttp.ClientConnectorError:
        raise StratzMatchNotParsedError()

async def get_stratz_player_last_match(bot, player_id):
    url = f"https://api.stratz.com/api/v1/Player/{player_id}/matches"
    result = await bot.http_client.get(url, cache=False, headers={"Authorization": f"Bearer {conf.STRATZ_TOKEN}"}, errors={500: "Looks like something wrong with the STRATZ api", 204: "STRATZ hasn't recieved this match yet. Try again a bit later"})
    return result[0]

def get_match_embed(data):
    winner = "Radiant"
    if not data['didRadiantWin']:
        winner = "Dire"
    embed = discord.Embed(
        title=f"Match {data['id']} results",
        description=(f"Duration: {data['durationSeconds']}\n" +
                    f"Game Mode: {data['gameMode']}\n" +
                    f"Winner: {winner}\n" +
                    f"Rank: {data['rank']}\n" +
                    f"Bracket: {data['bracket']}\n"),
        timestamp = dt.datetime.utcnow()
    )
    return embed

def get_user_name(query, ctx):
    for user in ctx.guild.members:
        if user.name == query or user.nick == query:
            return user.name

class Dota(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='match')
    async def match_command(self, ctx, match_id):
        async with ctx.typing():
            data = await get_stratz_match(self.bot, match_id)
        img = await dotaimage.create_match_result_image(data)
        file = discord.File(img, 'match.png')
        await ctx.send(file=file)

    @match_command.error
    async def match_command_error(self, ctx, exc):
        if isinstance(exc, StratzMatchNotParsedError):
            await ctx.send('Match is not yet parsed.')

    @commands.command(name="add")
    async def add_comand(self, ctx, steamId):
        member_id = ctx.message.author.id
        self.bot.db_connection.getCursor().execute('INSERT INTO users (id, steamid32) VALUES (?, ?) ON CONFLICT (id) DO UPDATE SET steamid32=excluded.steamid32 WHERE id=excluded.id;', (member_id, steamId))
        self.bot.db_connection.getConnection().commit()
        await ctx.send(f'Successfully associated {ctx.message.author.name} with SteamID32 {steamId}.')

    @commands.command(name='lastmatch', aliases=['lm'])
    async def last_match_command(self, ctx, *, username: t.Optional[str]):
        # TODO allow querying other users' matches
        # if not username:
        #    username = ctx.message.author.name
        member_id = ctx.message.author.id
        #try:
        steamId = self.bot.db_connection.getCursor().execute('SELECT steamid32 FROM users WHERE id=?;', (member_id,)).fetchone()
        #except:
        #    await ctx.send('You have to add a SteamID32 number first (use "?add SteamID32 [username]" comand).')
        #    return
        match = await get_stratz_player_last_match(self.bot, steamId[0])
        async with ctx.typing():
            img = await dotaimage.create_match_result_image(await get_stratz_match(self.bot, match['id']))
        file = discord.File(img, 'match.png')
        await ctx.send(file=file)

    @last_match_command.error
    async def last_match_command_error(self, ctx, exc):
        if isinstance(exc, KeyError):
            await ctx.send('You have to add a SteamID32 number first (use "?add SteamID32 [username]" comand).')
        else:
            raise exc


async def setup(bot):
    await bot.add_cog(Dota(bot))
