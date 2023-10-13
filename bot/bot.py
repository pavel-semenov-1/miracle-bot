from pathlib import Path

import discord
from discord.ext import commands
import bot.conf as conf

class MiracleBot(commands.Bot):
    def __init__(self, http_client, db_connection):
        self.prefix = '?'
        self._cogs = [p.stem for p in Path('.').glob('./bot/cogs/*.py')]
        self.http_client = http_client
        self.db_connection = db_connection
        print(self.db_connection)
        super().__init__(command_prefix=self.prefix, case_insensitive=True, intents=discord.Intents.all())

    async def setup_hook(self):
        print('Runnig setup...')

        for cog in self._cogs:
            await self.load_extension(f'bot.cogs.{cog}')
            print(f'Loaded `{cog}` cog.')

        print('Setup complete.')

    async def shutdown(self):
        print('Closing connection to Discord...')
        await super().close()

    async def on_connect(self):
        print(f'Connected to Discord (latency: {self.latency*1000:,.0f}ms).')

    async def on_resumed(self):
        print('Bot resumed')

    async def on_disconnect(self):
        print('Bot disconnected.')

    async def on_error(self, err, *args, **kwargs):
        raise

    async def on_command_error(self, ctx, exc):
        raise getattr(exc, 'original', exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print(f'Bot ready. id:{self.client_id}')

    async def prefix(self):
        return commands.when_mentioned_or(self.prefix)(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)

    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, id=518413093764595723)
        await member.add_roles(role)
