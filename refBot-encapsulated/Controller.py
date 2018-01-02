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
import Secrets
import GameObjects as go 

game = go.Game()

refBot = commands.Bot(command_prefix="!")

def getSummonerId(summonerName):
	requestUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + '?api_key=' + Secrets.apiKey
	getRequest = requests.get(requestUrl)
	summonerDetails = getRequest.json()
	return summonerDetails["id"]

@refBot.command()
async def aye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	summoner = go.Summoner(summonerName)
	activeSummoners = game.activeSummoners

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

	summonerData = db.getSummonerData(summonerId)
	
	name = summonerData[1]
	tier = summonerData[2]
	rank = summonerData[3]
	value = summonerData[4]
	primary = summonerData[5]
	secondary = summonerData[6]

	response = name + ': ' + tier + ' ' + rank + ' (' + str(value) + ') ' + primary + '/' + secondary
	await refBot.say(response)

@refBot.command()
async def open():
	await refBot.say('@everyone I am now online and Little League is open to enrollment! Type "!aye YourSummonerName" into the "RollCall" chat to join the game.')

@refBot.command()
async def options(option, value):
	m.setDraftOptions(option, value)

@refBot.command()
async def roles(summonerName, primary, secondary):
	summonerId = getSummonerId(summonerName)
	primary = primary.upper()
	secondary = secondary.upper()
	db.updateSummonerRoles(summonerId, primary, secondary)

	summonerData = db.getSummonerData(summonerId)
	name = summonerData[1]
	primary = summonerData[5]
	secondary = summonerData[6]

	response = name + ' : ' + primary + '/' + secondary

	return response

@refBot.command()
async def rollCall():
	response = draft.rollCall()
	await refBot.say(response)

@refBot.command()
async def setupDb():
	db.setupDb()

refBot.run(Secrets.botToken)