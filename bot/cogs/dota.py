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

async def get_stratz_match(match_id):
    url = f"https://api.stratz.com/api/v1/match/{match_id}"
    try:
        result = await conf.httpgetter.get(url, cache=True, errors={500: "Looks like something wrong with the STRATZ api", 204: "STRATZ hasn't recieved this match yet. Try again a bit later"})
        return result
    except aiohttp.ClientConnectorError:
        raise StratzMatchNotParsedError()

async def get_stratz_player_last_match(player_id):
    url = f"https://api.stratz.com/api/v1/Player/{player_id}/matches"
    result = await conf.httpgetter.get(url, cache=False, errors={500: "Looks like something wrong with the STRATZ api", 204: "STRATZ hasn't recieved this match yet. Try again a bit later"})
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
        self.players = dict()
        with open(os.path.join(conf.resource(''), 'players.txt'), 'r') as t:
            for line in t.readlines():
                try:
                    username, steamid = line.split('~')
                    self.players[username] = steamid[:-1]
                except:
                    continue

    @commands.command(name='match')
    async def match_command(self, ctx, match_id):
        async with ctx.typing():
            data = await get_stratz_match(match_id)
        img = await dotaimage.create_match_result_image(data)
        file = discord.File(img, 'match.png')
        await ctx.send(file=file)

    @match_command.error
    async def match_command_error(self, ctx, exc):
        if isinstance(exc, StratzMatchNotParsedError):
            await ctx.send('Match is not yet parsed.')

    @commands.command(name="add")
    async def add_comand(self, ctx, steamId, *, username: t.Optional[str]):
        if not username:
            username = ctx.message.author.name
        self.players[username] = steamId
        s = ''
        for user, id in self.players.items():
            s += f'{user}~{id}\n'
        with open(os.path.join(conf.resource(''), 'players.txt'), 'w') as t:
            t.write(s)
        await ctx.send(f'Successfully added {username} with SteamID32 {steamId}.')

    @commands.command(name='lastmatch', aliases=['lm'])
    async def last_match_command(self, ctx, *, username: t.Optional[str]):
        try:
            if username:
                match = await get_stratz_player_last_match(self.players[get_user_name(username, ctx)])
            else:
                match = await get_stratz_player_last_match(self.players[ctx.message.author.name])
        except KeyError:
            await ctx.send('You have to add a SteamID32 number first (use "?add SteamID32 [username]" comand).')
            return
        async with ctx.typing():
            img = await dotaimage.create_match_result_image(await get_stratz_match(match['id']))
        file = discord.File(img, 'match.png')
        await ctx.send(file=file)

    @last_match_command.error
    async def last_match_command_error(self, ctx, exc):
        if isinstance(exc, KeyError):
            await ctx.send('You have to add a SteamID32 number first (use "?add SteamID32 [username]" comand).')


def setup(bot):
    bot.add_cog(Dota(bot))
