from PIL import Image, ImageOps
import discord

async def invert_pfp(user):
	await user.avatar_url_as(format='jpg').save(fp='inverted_avatar.png')
	img = Image.open('inverted_avatar.png')
	im_invert = ImageOps.invert(img)
	im_invert.save('inverted_avatar.png')
	file = discord.File(fp='inverted_avatar.png', filename=f'{user.display_name}_inverted_avatar.png')
	return file