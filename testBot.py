import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)

botToken = 'INSERT BOT TOKEN HERE'
testBot = commands.Bot(command_prefix="/")

@testBot.command()
async def rollCall(subset = 'a'):
	if subset == 'b':
		await testBot.say('!aye TheRealN3lo')
		await testBot.say('!aye ECAEN')
		await testBot.say('!aye HumbleDiligent')
		await testBot.say('!aye FlameFlameFlame')
		await testBot.say('!aye Xyeles')
		await testBot.say('!aye BrokenLegFish')
		await testBot.say('!aye TheBigSpence')
		await testBot.say('!aye Bobmicbiong')
		await testBot.say('!aye AnnieBot')
		await testBot.say('!aye TheUnsungHeroPt2')
	else:
		await testBot.say('!aye TheRealN3lo')
		await testBot.say('!aye Ickyrus')
		await testBot.say('!aye Bobmicbiong')
		await testBot.say('!aye BrokenLegFish')
		await testBot.say('!aye TheUnsungHeroPt2')
		await testBot.say('!aye llamamalicious')
		await testBot.say('!aye ParadoxCycle')
		await testBot.say('!aye Zaraedaria')
		await testBot.say('!aye TheBigSpence')
		await testBot.say('!aye Xyeles')

	await testBot.say('!rollCall')

@testBot.command()
async def on():
	await testBot.say('!on matchmade')
	await testBot.say('!on rChamps')
	await testBot.say('!on rLanes')
