from discord.ext.commands import Bot
from discord import Game
import requests
import random
import asyncio
import json
import re

"""
Use your own bot tokens etc,
prefix for bot commands is "?"
"""
BOT_PREFIX = ("?")
#BOT TOKEN
TOKEN = "###########PLACEHOLDER###########"

client = Bot(command_prefix = BOT_PREFIX)


"""
eight_ball:
returns a random answer to a question chosen from a predefined list of answers
"""
@client.command(name='8ball',
				description='Answers a yes/no question, 8ball style',
				brief = 'Answers a question',
				aliases=['eight_ball', 'eightball','8-ball'],
				pass_context = True)
async def eight_ball(context):
	possible_responses = [
	'That is a resounding no',
	'It is not looking likely',
	'Too hard to tell',
	'It is quite possible',
	'For sure!']
	await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

"""
square:
first testing function, returns square of 'number'
:param number:
:type number: int
"""
@client.command()
async def square(number):
	squared_value = int(number) * int(number)
	await client.say(str(number)+" squared is " + str(squared_value))
"""
on_ready
event function, when ready, logged in, changes its 'Playing' field with 'with fire'
"""
@client.event
async def on_ready():
	await client.change_presence(game=Game(name="with fire"))
	print("Logged in as " + client.user.name)

"""
bitcoin
returns the current price of 1btc in Euros using the coindesk api
"""
@client.command()
async def bitcoin():
	url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
	response = requests.get(url)
	value = response.json()['bpi']['EUR']['rate']
	await client.say("Current bitcoin price: " + value + "€")

"""
fortune
returns a random choice of a fortune cookie saying from the json file fortune.json
"""
@client.command(name='fortune',
				description='Get your fortune cookie and lucky number',
				brief='Fortune Cookie!',
				aliases=['fortunecookie', 'cookie', 'fortune_cookie'],
				pass_context=True)
async def fortunecookie(context):
	with open('fortune.json') as j:
		data = json.load(j)
	lst = []
	for fortune in data:
		lst.append(fortune)
	choice = random.choice(lst)
	await client.say(context.message.author.mention + 
		" your fortune cookie reads: " +
		choice)

"""
weather
returns a simple description and current temperature in Celsius of the current weather in the specified city
using the openweathermap api
:param city:
:type string:
TODO: make the input from the user more lax
"""
@client.command(name='weather',
				description='weather city,countrycode, example: ?weather Athens,gr gets the current weather in athens',
				brief='get the current weather at your chosen city',
				aliases=['currentweather', 'current_weather'])
async def weather(city):
	
	#OPEN WEATHER MAP API KEY!
	payload = {'APPID':'########PLACEHOLDER#########', 'units':'metric'}
	url = 'http://api.openweathermap.org/data/2.5/weather?q='
	pattern = re.compile(r'[a-zA-z]+,[a-zA-z]+')
	if(pattern.match(city) == None):
		await client.say("Invalid city input")
	else:
		newurl = url + city
		r = requests.get(newurl, params=payload)
		weatherdisc = r.json()['weather'][0]['description']
		temp = r.json()['main']['temp']
		await client.say("Weather in "+city+ ": "+ weatherdisc + ", temp: " + str(temp) +"oC")

"""
remindme
reminds the user of a defined task in X minutes defined by the user
:param task:
:type string:
:param minutes:
:type int:
"""
@client.command(name='remindme',
				description='usage: ?remindme "task" minutes will remind you of the task in <minutes> minutes',
				brief='Reminds you of a task in defined minutes',
				aliases=['memo','reminder'],
				pass_context=True)
async def remindme(context, task, minutes):
	try:
		minutes = int(minutes)
	except ValueError:
		await client.say("Please give me a positive number for minutes")
	secs = int(minutes) * 60
	if task == None or secs < 0:
		await client.say("Invalid input")
	else:
		await client.say(context.message.author.mention + " I will remind you of: " + task + " in " + str(minutes) + " minute(s)")
		await asyncio.sleep(secs)
		await client.say(context.message.author.mention + " Time to: " + task)

#HLIAS
"""
roll
rolls xdy dice
:param dice:
:type string (xdy where x,y integers):
"""
@client.command(name='roll',
                description='Rolls one or more random dice in XdY(dW) format',
                brief = 'Rolls random die',
                aliases=['diceroll', 'dice-roll','dice_roll'],
                pass_context = True)
async def roll(context, dice):
    dicedata = dice.split('d')
    message = ""
    res = []
    if len(dicedata) == 2:
        message += "{"
        for i in range(int(dicedata[0]) - 1):
            res.append(random.randrange(int(dicedata[1])))
            message += str(res[-1]) + "+"
        res.append(random.randrange(int(dicedata[1])))
        message += str(res[-1]) + "} "
        await client.say(context.message.author.mention + " Rolled: " +dicedata[0]+"d"+dicedata[1]+" result: "+message)
    else:
        await client.say("Give me dice in XdY format")
#/HLIAS

"""
list_servers
background task, prints on running terminal the current servers the bot is logged in
"""
async def list_servers():
	await client.wait_until_ready()
	while not client.is_closed:
		print("Current servers:")
		for server in client.servers:
			print(server)
		await asyncio.sleep(600)

client.loop.create_task(list_servers())
client.run(TOKEN)


#fortune cookie: done
#weather: done
#dictionary definition
#diceroller: done
#remind me, reminder after some time: done