from bot.cogs.utils.httpgetter import HttpGetter
from bot.cogs.utils.dbconnection import Connection
import os

def init():
    global httpgetter
    global datapath
    global connection
    global DISCORD_TOKEN
    global STRATZ_TOKEN
    datapath = '/home/ec2-user/miracle-bot/data'
    DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
    STRATZ_TOKEN = os.environ.get("STRATZ_TOKEN")

def resource(name):
    return os.path.join('data', name)
