from telethon import events
from .. import loader, utils
import os
import requests
from PIL import Image,ImageFont,ImageDraw 
import re
import io
from textwrap import wrap

def register(cb):
	cb(JacquesMod())
	
class JacquesMod(loader.Module):
	"""Жаконизатор"""
	strings = {
		'name': 'Floppa_say',
		'usage': 'Напиши <code>.help Floppa_say</code>',
	}
	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []
	
	async def floppacmd(self, message):
		""".floppa <реплай на сообщение/свой текст>\n@offsd подпишись-пожалеешь"""
		
		ufr = requests.get("https://github.com/Sad0ff/modules-ftg/raw/master/open-sans.ttf")
		f = ufr.content
		
		reply = await message.get_reply_message()
		args = utils.get_args_raw(message)
		if not args:
			if not reply:
				await utils.answer(message, self.strings('usage', message))
				return
			else:
				txt = reply.raw_text
		else:
			txt = utils.get_args_raw(message)
		await message.edit("<b>Шлема крут...</b>")
		pic = requests.get("https://github.com/cotiknbtsFiles/shlepa_say/raw/main/Screenshot_2022-07-13-03-48-48-06_4ab34c1cc13001646ffc6e1ca68df0a1.jpg")
		pic.raw.decode_content = True
		img = Image.open(io.BytesIO(pic.content)).convert("RGB")
 
		W, H = img.size
		#txt = txt.replace("\n", "𓃐")
		text = "\n".join(wrap(txt, 19))
		t = text + "\n"
		#t = t.replace("𓃐","\n")
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype(io.BytesIO(f), 32, encoding='UTF-8')
		w, h = draw.multiline_textsize(t, font=font)
		imtext = Image.new("RGBA", (w+10, h+10), (0, 0,0,0))
		draw = ImageDraw.Draw(imtext)
		draw.multiline_text((10, 10),t,(0,0,0),font=font, align='left')
		imtext.thumbnail((339, 181))
		w, h = 339, 181
		img.paste(imtext, (10,10), imtext)
		out = io.BytesIO()
		out.name = "@offsd.jpg"
		img.save(out)
		out.seek(0)
		await message.client.send_file(message.to_id, out, reply_to=reply)
		await message.delete()