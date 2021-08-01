from bot.cogs.utils.httpgetter import HttpGetter
from bot.cogs.utils.dbconnection import Connection
import os

def init():
    global httpgetter
    global datapath
    global connection
    datapath = '/home/ec2-user/miracle-bot/data'
    httpgetter = HttpGetter()
    connection = Connection()

def resource(name):
    return os.path.join('data', name)
