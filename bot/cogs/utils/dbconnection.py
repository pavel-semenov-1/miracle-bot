import sqlite3

class Connection:
    async def __aenter__(self):
        self.connection = sqlite3.connect('miracle-bot.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (id integer primary key, steamid32 varchar(9))')
        self.connection.commit()
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        self.connection.close()

    def getConnection(self):
        return self.connection

    def getCursor(self):
        return self.cursor

    def close(self):
        self.connection.close()
