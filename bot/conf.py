from bot.cogs.utils.httpgetter import HttpGetter
import os

def init():
    global httpgetter
    global datapath
    datapath = '/home/paradox/Desktop/MiracleBot/data'
    httpgetter = HttpGetter()

def resource(name):
    return os.path.join('data', name)
