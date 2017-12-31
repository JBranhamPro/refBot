# Imports required for Discord view
import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
import asyncio
# Imports of required Python modules
import requests
import json
# Imports of all refBot files
import DbCalls as db
from Draft import Draft
import Secrets
import Summoner

game = GameObjects.Game()

refBot = commands.Bot(command_prefix="!")

def getSummonerId(summonerName):
	requestUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + '?api_key=' + Secrets.apiKey
	getRequest = requests.get(summonerUrl)
	summonerDetails = getRequest.json()
	return summonerDetails["id"]

@refBot.command()
async def aye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	summoner = GameObjects.Summoner(summonerName)
	activePlayers = game.activeSummoners

	for player in activeSummoners:
		if player.id == summoner.id:
			await refBot.say(summoner.name + ' is already an active player.')
			return print(player.id, summoner.id)

	activeSummoners.append(summoner)

	response = db.uploadSummoner(summoner)
	await refBot.say(response)

@refBot.command()
async def bye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	summonerId = getSummonerId(summonerName)

	for player in game.activePlayers:
		if player.id == summonerId:
			summoner = player

	response = game.rmActiveSummoner(summoner)
	await refBot.say(response)

@refBot.command()
async def get(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	summonerId = getSummonerId(summonerName)

	summonerData = db.getSummonerData(summoner)
	
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

refBot.run(Secrets.botToken)