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

activeGames = []

refBot = commands.Bot(command_prefix="!")

def getSummonerId(summonerName):
	requestUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + '?api_key=' + Secrets.apiKey
	getRequest = requests.get(requestUrl)
	summonerDetails = getRequest.json()
	return summonerDetails["id"]

@refBot.command()
async def aye(*nameInput):
	summonerName = ''
	gameIndex = None
	for part in nameInput:
		summonerName += part

	if len(activeGames) < 1:
		await refBot.say('There are currently no active games to join. Use the open command to start a new game.')
		return

	summonerId = getSummonerId(summonerName)

	for game in activeGames:
		activeSummoners = game.activeSummoners
		for summoner in activeSummoners:
			if summoner.id == summonerId:
				await refBot.say(summoner.name + ' is already an active player.')
				return

	summoner = go.Summoner(summonerId)

	for game in activeGames:
		activeSummoners = game.activeSummoners
		if len(activeSummoners) < 10:
			added = game.addSummoner(summoner)
			if added:
				response = db.uploadSummoner(summoner)
				await refBot.say(response)
				return
			else:
				await refBot.say('Something went wrong :( . Refer to the console for more details.')
			break

@refBot.command()
async def bye(*nameInput):
	summonerName = ''
	for part in nameInput:
		summonerName += part

	failResponse = summonerName + ' is not currently an active player.'

	summonerId = getSummonerId(summonerName)
	summonerData = db.getSummonerData(summonerId)
	if summonerData:
		gameId = summonerData[7]
	else:
		await refBot.say(failResponse)
		return

	if gameId:
		for game in activeGames:
			if game.id == gameId:
				response = game.rmSummoner(summonerId)
				await refBot.say(response)
				return
	else:
		await refBot.say(failResponse)

@refBot.command()
async def close(gameIndex):
	try:
		del activeGames[gameIndex]
		await refBot.say('Game ' + gameIndex + ' has been closed. You may give the open command if you would like to start a new one.')
	except:
		await refBot.say('The game in question could not be found.')

@refBot.command()
async def get(*nameInput):
	summonerName = ''
	for part in nameInput:
		summonerName += part

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
	game = go.Game()

	activeGames.append(game)

	print('Controller --> open: ', game)

	await refBot.say('@everyone A new game is open to enrollment! Type "!aye YourSummonerName" into the "RollCall" chat to join the game.')

@refBot.command()
async def options(option, value):
	m.setDraftOptions(option, value)

@refBot.command()
async def roles(primary, secondary, *nameInput):
	summonerName = ''
	for part in nameInput:
		summonerName += part

	summonerId = getSummonerId(summonerName)
	primary = primary.upper()
	secondary = secondary.upper()

	def invalidRole(role):
		if role == 'TOP':
			return None
		elif role == 'JNG':
			return None
		elif role == 'MID':
			return None
		elif role == 'ADC':
			return None
		elif role == 'SUP':
			return None
		elif role == 'FILL':
			return None
		else:			
			return role

	primaryInvalid = invalidRole(primary)
	secondaryInvalid = invalidRole(secondary)

	if primaryInvalid or secondaryInvalid:
		invalidRoles = ''
		if primaryInvalid:
			invalidRoles += primaryInvalid
			if secondaryInvalid:
				invalidRoles += ', ' + secondaryInvalid
		else:
			invalidRoles += secondaryInvalid
		await refBot.say('The following roles were not recognized: \" ' + invalidRoles + '\ ". Please use only the following in the roles command: TOP, JNG, MID, ADC, SUP, FILL')
		return
	
	else:
		db.updateSummonerRoles(summonerId, primary, secondary)

		summonerData = db.getSummonerData(summonerId)
		name = summonerData[1]
		primary = summonerData[5]
		secondary = summonerData[6]
		gameId = summonerData[7]

		if gameId:
			for game in activeGames:
				if game.id == gameId:
					activeSummoners = game.activeSummoners
					for summoner in activeSummoners:
						if summoner.id == summonerId:
							summoner.setRoles(primary, secondary)
					break

		response = name + ' : ' + primary + '/' + secondary
		await refBot.say(response)

@refBot.command()
async def rollCall():
	if activeGames:
		response = ''
		for game in activeGames:
			response += 'Game ' + str(activeGames.index(game)) + ' -->\n'
			response += game.rollCall()
			response += '\n\n\n'

		await refBot.say(response)
	else:
		await refBot.say('There are no games currently open. Give the open command to start a new one.')

@refBot.command()
async def setupDb():
	db.setupDb()

@refBot.command()
async def test():
	print(activeGames[0])

refBot.run(Secrets.botToken)