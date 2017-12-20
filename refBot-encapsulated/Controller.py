# Imports required for Discord integration
import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
import asyncio
# Imports of all refBot files
import DbCalls
db = DbCalls
from Draft import draft
import Secrets
from Summoner import summoner

draft = draft()

refBot = commands.Bot(command_prefix="!")

@refBot.command()
async def add(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	summonerName = riotApi.getSummonerName(summonerName)
	summonerData = riotApi.getSummonerData(summonerName)
	summoner = summoner(summonerName, summonerData)

	if db.getSummoner(summonerName) is None:
		response = db.uploadSummoner(name, tier, rank, value)
		return response

@refBot.command()
async def aye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	response = draft.addActiveSummoner(summonerName)
	await refBot.say(response)

@refBot.command()
async def bye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	response = draft.rmActiveSummoner(summonerName)
	await refBot.say(response)

@refBot.command()
async def start():
	response = draft.start()
	await refBot.say(response)

@refBot.command()
async def get(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	summoner = db.getSummonerData(summonerName)
	
	name = summonerData[1]
	tier = summonerData[2]
	rank = summonerData[3]
	value = summoner[4]
	primary = summoner[5]
	secondary = summoner[6]

	response = name + ': ' + tier + ' ' + rank + ' (' + str(value) + ') ' + primary + '/' + secondary
	await refBot.say(response)

@refBot.command()
async def open():
	await refBot.say('@everyone I am now online and Little League is open to enrollment! Type "!aye YourSummonerName" into the "RollCall" chat to join the game.')

@refBot.command()
async def options(option, value):
	m.setDraftOptions(option, value)

@refBot.command()
async def rollCall():
	response = draft.rollCall()
	await refBot.say(response)

@refBot.command()
async def setupDb():
	db.setupDb()

@refBot.command()
async def testDb():
	db.insertTestData()

refBot.run(Secrets.botToken)