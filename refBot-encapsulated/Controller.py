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

currentPlayers = {}

activeGames = []

refBot = commands.Bot(command_prefix="!")

def addToTeam(teamIndex, nameInput):
	summonerName = buildName(nameInput)
	summonerId = getSummonerId(summonerName)

	def addSummoner(game, summoner):
		try:
			team = game.activeTeams[teamIndex]
		except:
			game.activeTeams.insert(teamIndex, [])
			team = game.activeTeams[teamIndex]

		team.add(summoner)

	for game in activeGames:
		activeSummoners = game.activeSummoners
		for summoner in activeSummoners:
			if summoner.id == summonerId:
				addSummoner(game, summoner)
				break

def buildName(nameInput):
	summonerName = ''
	for part in nameInput:
		summonerName += part
	return summonerName

def getSummonerId(summonerName):
	try:
		# requestUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + '?api_key=' + Secrets.apiKey
		requestUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'.format(summonerName, Secrets.apiKey)
		getRequest = requests.get(requestUrl)
		summonerDetails = getRequest.json()
		return summonerDetails["id"]
	except:
		return False

@refBot.command()
async def a(*nameInput):
	addToTeam(0, nameInput)

@refBot.command()
async def aye(*nameInput):
	summonerName = buildName(nameInput)

	if len(activeGames) < 1:
		await refBot.say('There are currently no active games to join. Use the open command to start a new game.')
		return

	summonerId = getSummonerId(summonerName)
	if summonerId == False:
		await refBot.say('A summoner with the name, {}, could not be found.'.format(summonerName))
		return

	if summonerId in currentPlayers:
		await refBot.say('{} is already an active player.'.format(summonerName))
		return

	summoner = go.Summoner(summonerId)
	if type(summoner) == str:
		# The Summoner object fail response is a string
		await refBot.say(summoner)

	for game in activeGames:
		activeSummoners = game.activeSummoners
		if len(activeSummoners) < 10:
			added = game.addSummoner(summoner)
			if added:
				currentPlayers[summoner.id] = game.name
				response = db.uploadSummoner(summoner)
				await refBot.say(response)
				return
			else:
				await refBot.say('Something went wrong with adding the summoner to game, {}.'.format(game.name))
			break

@refBot.command()
async def b(*nameInput):
	addToTeam(1, nameInput)

@refBot.command()
async def bye(*nameInput):
	summonerName = buildName(nameInput)

	failResponse = '{} is not currently an active player.'.format(summonerName)

	summonerId = getSummonerId(summonerName)
	
	if summonerId not in currentPlayers:
		await refBot.say(failResponse)
	else:
		gameName = currentPlayers[summonerId]
		for game in activeGames:
			if game.name == gameName:
				response = game.rmSummoner(summonerId)
				del currentPlayers[summonerId]
				await refBot.say(response)
				return
			else:
				await refBot.say(failResponse)

@refBot.command()
async def close(gameIndex):
	try:
		game = activeGames[int(gameIndex)]
		playersToRemove = []

		for summonerId, gameName in currentPlayers.items():
			if gameName == game.name:
				playersToRemove.append(summonerId)

		for summonerId in playersToRemove:
			del currentPlayers[summonerId]

		del activeGames[int(gameIndex)]
		await refBot.say('Game {} has been closed. You may give the open command if you would like to start a new one.'.format(str(gameIndex)))
	except:
		await refBot.say('The game in question could not be found.')

@refBot.group(pass_context=True)
async def draft(context):
	if context.invoked_subcommand is None:
		await refBot.say('Invalid draft command passed...')

@refBot.command()
async def games():
	games = db.getGames()

	names = []
	for game in games:
		names.append(game[1])

	response = ''
	i = 0

	for name in names:
		i+=1
		response += str(i) + '. ' + name + '\n'

	await refBot.say(response)

@refBot.command()
async def get(*nameInput):
	summonerName = buildName(nameInput)

	summonerId = getSummonerId(summonerName)

	summonerData = db.getSummonerData(summonerId)
	
	name = summonerData[1]
	tier = summonerData[2]
	rank = summonerData[3]
	value = summonerData[4]
	primary = summonerData[5]
	secondary = summonerData[6]

	# response = name + ': ' + tier + ' ' + rank + ' (' + str(value) + ') ' + primary + '/' + secondary
	response = '{} : {} {}  ({}) {}/{}'.format(name, tier, rank, str(value), primary, secondary)
	await refBot.say(response)

@refBot.command()
async def open():
	game = go.Game()

	activeGames.append(game)

	print('Controller --> open: ', game)

	db.saveGame(game)

	await refBot.say('@everyone A new game is open to enrollment! Type "!aye YourSummonerName" into the "RollCall" chat to join the game.')

@refBot.command()
async def option(gameIndex, opt, *optValue):
	game = activeGames[int(gameIndex)]
	game.setOption(opt, optValue)

@refBot.command()
async def roles(primary, secondary, *nameInput):
	summonerName = buildName(nameInput)

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
		await refBot.say('The following roles were not recognized: \"{}\". Please use only the following in the roles command: TOP, JNG, MID, ADC, SUP, FILL'.format(invalidRoles))
		return
	
	else:
		db.updateSummonerRoles(summonerId, primary, secondary)
		summonerData = db.getSummonerData(summonerId)
		name = summonerData[1]
		primary = summonerData[5]
		secondary = summonerData[6]

		if summonerId in currentPlayers:
			gameName = currentPlayers[summonerId]

			for game in activeGames:
				if game.name == gameName:
					activeSummoners = game.activeSummoners
					for summoner in activeSummoners:
						if summoner.id == summonerId:
							summoner.setRoles(primary, secondary)
							break
					break

		# response = name + ' : ' + primary + '/' + secondary
		response = '{} : {}/{}'.format(name, primary, secondary)
		await refBot.say(response)

@refBot.command()
async def rollCall():
	if activeGames:
		response = ''
		for game in activeGames:
			response += 'Game {} -->\n'.format(str(activeGames.index(game)))
			response += game.rollCall()
			response += '\n\n\n'

		await refBot.say(response)
	else:
		await refBot.say('There are no games currently open. Give the open command to start a new one.')

@refBot.command()
async def save(gameIndex):
	game = activeGames[int(gameIndex)]
	db.saveGame(game)

@refBot.command()
async def setupDb():
	db.setupDb()

@refBot.command()
async def start(gameIndex):
	game = activeGames[int(gameIndex)]
	draftType = game.draft.type
	success = game.start()

	if success:
		pass
	else:
		print('There was an issue with the draft and it failed to start.')
		return

	if draftType == 'MATCHMADE':
		teams = game.draft.matchmade(game.activeSummoners)

	teamA = teams[0]
	msgTeamA = 'Team A is:\n\n'
	i = 0
	for summoner in teamA:
		i+=1
		msgTeamA += str(i) + '. ' + summoner.name + '\n'

	if game.draft.rChamps:
		msgTeamA += 'The champion pool for Team A is: ' + '\n' + randomChamps(rChamps)
	print(msgTeamA)

	teamB = teams[1]
	msgTeamB = 'Team B is:\n\n'
	i = 0
	for summoner in teamB:
		i+=1
		msgTeamB += str(i) + '. ' + summoner.name + '\n'

	if game.draft.rChamps:
		msgTeamB += 'The champion pool for Team B is: ' + '\n' + randomChamps(rChamps)
	print(msgTeamB)

	response = msgTeamA + '\n\n\n' + msgTeamB

	await refBot.say(response)

	asyncio.sleep(900)
	try:
		# requestUrl = 'https://na1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/' + str(summonerId) + '?api_key=' + Secrets.apiKey
		requestUrl = 'https://na1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/{}?api_key={}'.format(str(summonerId), Secrets.apiKey)
		getRequest = requests.get(requestUrl)
		lolGame = getRequest.json()
		print(lolGame)
		await refBot.say(lolGame["gameId"])
	except:
		print('No game started... yet')

@refBot.command()
async def test():
	print(discord.Client)
	client = discord.Client()
	print(refBot)

refBot.run(Secrets.botToken)