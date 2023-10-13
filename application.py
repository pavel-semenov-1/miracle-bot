from bot import MiracleBot
import bot.conf as conf
import asyncio
from bot.cogs.utils.httpgetter import HttpGetter
from bot.cogs.utils.dbconnection import Connection

async def main():
    conf.init()
    async with HttpGetter() as http_client, Connection() as db_connection:
        async with MiracleBot(http_client, db_connection) as bot:
            await bot.start(conf.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
