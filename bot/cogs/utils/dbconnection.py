import sqlite3

class Connection:
    def __init__(self):
        self.connection = sqlite3.connect('miracle-bot.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (id serial primary key, name text NOT NULL UNIQUE, steamid32 varchar(9), time integer)')
        self.connection.commit()

    def getConnection(self):
        return self.connection

    def getCursor(self):
        return self.cursor

    def close(self):
        self.connection.close()
