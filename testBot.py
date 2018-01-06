import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
import time

botToken = 'MzQwNzQ4MDY0Mzc5NzY0NzM3.DTGcTw.ABR-Kb5IqAV4la03Y0RA_I9LuGc'
testBot = commands.Bot(command_prefix="?")

@testBot.command()
async def rollCall(subset = 'a'):
	if subset == 'b':
		b = ['GP IS OP', 'Annie Bot', 'HumbleDiligent', 'IamHondaCivic', 'Greasy Turkey', 'Gundâm', 'Caution Fruit', 'Disciple13', 'Rob Bombadil', 'EthanD']
		i = 0
		for summoner in b:
			await testBot.say('!aye ' + b[i])
			time.sleep(2)
			i+=1
	else:
		a = ['TheRealN3lo', 'Ickyrus', 'Bobmicbiong', 'BrokenLegFish', 'NotAnAnimeProtag', 'llamamalicious', 'ParadoxCycle', 'Zaraedaria', 'TheBigSpence', 'Xyeles']
		i = 0
		for summoner in a:
			await testBot.say('!aye ' + a[i])
			time.sleep(2)
			i+=1

@testBot.command()
async def on():
	await testBot.say('!on matchmade')
	await testBot.say('!on rChamps')
	await testBot.say('!on rLanes')

testBot.run(botToken)