# Imports required for Discord integration
import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
import asyncio
# Imports of all refBot files
from APICalls import riotApi
from DbCalls import littleLeagueDb
db = littleLeagueDb
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
	
	name = summoner.name
	tier = summoner.tier
	rank = summoner.rank
	value = summoner.value

	response = name + ': ' + tier + ' ' + rank + ' (' + str(value) + ')'
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