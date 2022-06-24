from bot.cogs.utils.httpgetter import HttpGetter
from bot.cogs.utils.dbconnection import Connection
import os

def init():
    global httpgetter
    global datapath
    global connection
    global TOKEN
    datapath = '/home/ec2-user/miracle-bot/data'
    httpgetter = HttpGetter()
    connection = Connection()
    TOKEN = os.environ.get("DISCORD_TOKEN")

def resource(name):
    return os.path.join('data', name)
