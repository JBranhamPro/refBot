import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)

botToken = ''
testBot = commands.Bot(command_prefix="/")

@testBot.command()
async def aDraft():
	await testBot.say('!place TheRealN3lo')
	await testBot.say('!place Ickyrus')
	await testBot.say('!place Bobmicbiong')
	await testBot.say('!place BrokenLegFish')
	await testBot.say('!place TheUnsungHeroPt2')
	await testBot.say('!place llamamalicious')
	await testBot.say('!place ParadoxCycle')
	await testBot.say('!place Zaraedaria')
	await testBot.say('!place TheBigSpence')
	await testBot.say('!place Xyeles')

@testBot.command()
async def rollCall():
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

testBot.run(botToken)
