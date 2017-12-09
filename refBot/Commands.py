# Imports required for Discord integration
import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
import asyncio
# Imports of all refBot files
import APICalls
a = APICalls
import Methods
m = Methods
import DbCalls
d = DbCalls
import Secrets

refBot = commands.Bot(command_prefix="!")

@refBot.command()
async def add(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	respone = m.onAddCmd(summonerName)
	await refBot.say(respone)

@refBot.command()
async def aye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	response = m.onAyeCmd(summonerName)
	await refBot.say(response)

@refBot.command()
async def bye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	response = m.onByeCmd(summonerName)
	await refBot.say(response)

@refBot.command()
async def draft(typeOpt):
	draftType = typeOpt.upper()

	response = m.draft(draftType)
	await refBot.say(response)

@refBot.command()
async def get(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	responseMsg = m.onGetCmd(summonerName)
	await refBot.say(responseMsg)

@refBot.command()
async def open():
	await refBot.say('@everyone I am now online and Little League is open to enrollment! Type "!aye YourSummonerName" into the "RollCall" chat to join the game.')

@refBot.command()
async def options(option, value):
	m.setDraftOptions(option, value)

@refBot.command()
async def rollCall():
	rollCallMsg = m.onRollCallCmd()
	await refBot.say(rollCallMsg)

@refBot.command()
async def setupDb():
	d.setupDb()

@refBot.command()
async def testDb():
	d.insertTestData()

refBot.run(Secrets.botToken)