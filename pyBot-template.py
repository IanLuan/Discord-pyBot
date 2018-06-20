import discord
from random import choice
from weather import Weather, Unit
import urllib.request
import json

# Discord pyBot Template
# Made by Ian Luan 

# You have to get your own template on Discord Developers
TOKEN = 'YOUR TOKEN'

client = discord.Client()

@client.event
async def on_message(message):

	# we do not want the bot to reply to itself
	if message.author == client.user:
		return

	if message.content.startswith('!hello'):
		msg = 'Hello {0.author.mention}, You are Amazing!'.format(message)
		await client.send_message(message.channel, msg)

	# Help
	if message.content.startswith('!help'):
		msg = """Hi {0.author.mention}! This list will help You: 
			\n\n!hello - A Simple Welcome message
			\n\nMath - Just type your expression and IL bot will solve it.
			\n    Example: 2 + 2 *  5
			\n    OPs: sum(x+y)  sub(x-y)  mult(x*y)  div(x/y)  exponent(x**n)
			\n\n!draw - Easy random choice. Type !draw and the options separated by commas.
			\n    Example: !draw Matheus, Yasmin, Peter Pan, John (IL Bots will choose a random option.)
			"""
		await client.send_message(message.channel, msg)

	# Math
	# No Lib used
	if message.content[0].isnumeric():
		msg = eval(message.content)

		await client.send_message(message.channel, msg)

	# Random Choice
	# Lib Random
	if message.content.startswith('!draw'):
		msglist = message.content
		msglist = msglist[5:]
		msglist = [x.strip() for x in msglist.split(',')]
		msg = choice(msglist)

		await client.send_message(message.channel, msg)

	# Weather
	# Lib Weather
	if message.content.startswith('!weather'):
		city = message.content[9:]
		weather = Weather(unit=Unit.CELSIUS)
		location = weather.lookup_by_location(city)
		condition = location.condition
		forecast = location.forecast
		msg = "Between {} and {}, {}.".format(forecast[0].low, forecast[0].high, forecast[0].text)

		await client.send_message(message.channel, msg)

	# Youtube Count
	# Youtube API
	if message.content.startswith('!yt'):
		name = message.content[4:]
		key = 'AIzaSyC89SFpIUDMdo0aCNXE9gXMdtwTSZ-6hoQ'

		data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+name+"&key="+key).read()
		subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]

		msg = "{} has {:,d} subscribers!".format(name, int(subs))

		await client.send_message(message.channel, msg)



@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run(TOKEN)
