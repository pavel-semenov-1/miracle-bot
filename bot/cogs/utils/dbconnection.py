import sqlite3

class Connection:
    def __init__(self, bot):
        print("Connecting to the database `miracle-bot.db`...")
        self.connection = sqlite3.connect('miracle-bot.db')
        self.cursor = self.connection.cursor()

        # create tables `guilds` and `members`
        self.cursor.execute('CREATE TABLE IF NOT EXISTS guilds (id serial primary key, name text NOT NULL UNIQUE, role1 text, role2 text, role3 text)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS members (id serial primary key, guild_id integer REFERENCES guilds, name text NOT NULL UNIQUE, steamid32 varchar(9), time integer)')

        # populate tables with data
        for guild in bot.guilds:
            self.cursor.execute('INSERT INTO guilds VALUES (?, ?, NULL, NULL, NULL)', (guild.id, guild.name))
            for member in guild.members:
                self.cursor.execute('INSERT INTO members (guild_id, name, steamid32, time) VALUES (?, ?, NULL, 0)', (guild.id, member.name))

        self.connection.commit()
        print("Successfully connected to the database")

    def getConnection(self):
        return self.connection

    def getCursor(self):
        return self.cursor

    def close(self):
        self.connection.close()
