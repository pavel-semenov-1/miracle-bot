from aiohttp import web
import asyncio
import discord 
from discord.ext import commands
        
class Server(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def webserver(self):
        async def handler(request):
            return web.Response(text="Hello, world")

        app = web.Application()
        app.router.add_get('/', handler)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, 'localhost', 5000)
        await self.bot.wait_until_ready()
        await self.site.start()

    def __unload(self):
        asyncio.ensure_future(self.site.stop())

async def setup(bot):
    server = Server(bot)
    await bot.add_cog(server)
    # TODO run webserver in separate loop
