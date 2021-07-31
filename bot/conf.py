from bot.cogs.utils.httpgetter import HttpGetter
import os

def init():
    global httpgetter
    global datapath
    datapath = '/home/ec2-user/miracle-bot/data'
    httpgetter = HttpGetter()

def resource(name):
    return os.path.join('data', name)
