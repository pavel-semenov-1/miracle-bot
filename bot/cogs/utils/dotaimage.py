from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import datetime as dt
import os
from io import BytesIO

import bot.conf as conf

class DotaImage:
    def __init__(self, font_path, image_url):
        self.img = Image.new('RGBA', (1920, 1080), color=(23, 32, 41, 255))
        self.draw = ImageDraw.Draw(self.img)
        self.font_path = font_path
        self.image_url = image_url

    def put_text(self, text, x, y, color=(255,255,255,255), font_family='Oswald', font_size=40, anchor='center'):
        font=ImageFont.truetype(os.path.join(self.font_path, font_family+'-Regular.ttf'), font_size)
        w, h = self.draw.textsize(text, font=font)
        if anchor == 'center':
            self.draw.text((x-w/2,y-h/2), text, fill=color, font=font)
        elif anchor == 'left':
            self.draw.text((x, y-h/2), text, fill=color, font=font)
        elif anchor == 'right':
            self.draw.text((x-w, y-h/2), text, fill=color, font=font)

    async def put_radiant_dire(self, radiantWin, xr, yr, xd, yd, xri, yri, xdi, ydi):
        self.put_text('Radiant', xr, yr, color=(63, 191, 63, 255), font_family='Langar', font_size=70)
        self.put_text('Dire', xd, yd, color=(191, 63, 63, 255), font_family='Langar', font_size=70)
        try:
            radiant = Image.open(os.path.join(conf.resource('img/'), 'radiant.png'))
        except:
            radiant = await self.get_url_image(self.image_url+'radiant.png')
        self.img.paste(radiant, (xri, yri))
        try:
            dire = Image.open(os.path.join(conf.resource('img/'), 'dire.png'))
        except:
            dire = await self.get_url_image(self.image_url+'dire.png')
        self.img.paste(dire, (xdi, ydi))
        try:
            icon = Image.open(os.path.join(conf.resource('img/'), 'winner.png'))
        except:
            icon = await self.get_url_image(self.image_url+'winner.png')
        background = Image.new(icon.mode[:-1], (icon.size[0], icon.size[1]), (23, 32, 41, 255))
        background.paste(icon, icon.split()[-1])
        icon = background
        icon.convert('RGB')
        if radiantWin:
            self.img.paste(icon, (xr-64, yr-140))
        else:
            self.img.paste(icon, (xd-64, yd-140))

    def put_lobby(self, lobby_id, x, y):
        if lobby_id == 7:
            text = "Ranked"
        else:
            text = "Unknown"
        self.put_text(text, x, y, font_family='Langar', font_size=60)

    def put_date(self, timestamp, x, y):
        text = dt.datetime.fromtimestamp(timestamp).strftime('%d.%m.%y %H:%M')
        self.put_text(text, x, y, font_size=32)

    def put_mode(self, mode_id, x, y):
        if mode_id == 22:
            text = "All pick"
        else:
            text = "Unknown"
        self.put_text(text, x, y, font_family='Langar', font_size=40)

    def put_duration(self, duration, x, y):
        minutes, seconds = divmod(duration, 60)
        self.put_text('{:02}:{:02}'.format(minutes, seconds), x, y, font_size=32)

    async def put_hero_icon(self, hero_id, x, y):
        try:
            icon = Image.open(os.path.join(conf.resource("img/"), str(hero_id)+'_thumbnail.png'))
        except:
            icon = await self.get_url_image(self.image_url+str(hero_id)+'_thumbnail.png')
        background = Image.new(icon.mode[:-1], (icon.size[0]+4, icon.size[1]+4), (23, 32, 41, 255))
        bgdraw = ImageDraw.Draw(background)
        bgdraw.ellipse([(0,0), (144,144)], fill="#ffffff")
        background.paste(icon, (2,2), icon.split()[-1])
        icon = background
        icon.convert('RGB')
        self.img.paste(icon, (x,y))

    async def get_url_image(self, url):
        return Image.open(await conf.httpgetter.get(url, "bytes", cache=True))


    def show(self):
        self.img.show()

    def get_image(self):
        return self.img


async def create_match_result_image(data):
    img = DotaImage(conf.resource("fonts/"), 'http://www.quaranta.ru/dota_icons/')
    await img.put_radiant_dire(data['didRadiantWin'], 385, 170, 1535, 170, 45, 110, 1735, 110)
    img.put_lobby(data['lobbyType'], 960, 100)
    img.put_mode(data['gameMode'], 960, 170)
    img.put_date(data['startDateTime'], 960, 30)
    img.put_duration(data['durationSeconds'], 960, 210)
    x,y,i= 45,310,1
    for player in data['players']:
        await img.put_hero_icon(player['heroId'], x, y)
        kda = f'{player["numKills"]}/{player["numDeaths"]}/{player["numAssists"]}'
        nw = round(player['networth']/1000, 1)
        nw = f'{nw}k'
        if i == 1:
            img.put_text(player['steamAccount']['name'][:18], x+155, y+70, color=(0, 255, 255, 255), font_size=50, anchor='left', font_family='Oswald')
            img.put_text(kda, x+155+380, y+70, font_size=50, anchor='left')
            img.put_text(nw, x+155+380+215, y+70, font_size=50, anchor='left', color=(255, 220, 0, 255))
        else:
            img.put_text(player['steamAccount']['name'][:18], x-15, y+70, color=(0, 255, 255, 255), font_size=50, anchor='right', font_family='Oswald')
            img.put_text(kda, x-15-380, y+70, font_size=50, anchor='right')
            img.put_text(nw, x-15-380-215, y+70, font_size=50, anchor='right', color=(255, 220, 0, 255))
        y += 150
        if player['playerSlot'] == 4:
            x = 1735
            y = 310
            i = -1

    img = img.get_image()
    fp = BytesIO()
    img.save(fp, format="PNG")
    fp.seek(0)
    return fp
