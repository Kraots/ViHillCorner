from discord.ext import commands
import async_cse as cse
import discord
import os

GoogleKey1 = os.getenv("GOOGLE_API_KEY_A")
GoogleKey2 = os.getenv("GOOGLE_API_KEY_B")
GoogleKey3 = os.getenv("GOOGLE_API_KEY_C")

class GoogleSearch(commands.Cog):
	def __init__(self, client):
		self.client = client 

	@commands.command()
	async def google(self, ctx, *, query):
		GoogleClient = cse.Search([GoogleKey1, GoogleKey2, GoogleKey3])
		query = str(query)
		results = await GoogleClient.search(query, safesearch=False)
		result = results[0]
		em = discord.Embed(title=result.title, url=result.url, description=result.description)
		if str(result.image_url) != "https://image.flaticon.com/teams/slug/google.jpg":
			em.set_image(url=result.image_url)
		await ctx.send(embed=em)
		await GoogleClient.close()

def setup (client):
	client.add_cog(GoogleSearch(client))