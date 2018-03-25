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

class Instance(object):
	"""docstring for Instance"""
	def __init__(self, server):
		super(Instance, self).__init__()
		self.id = server.id
		self.name = server.name
		self.server = server
		self.currentPlayers = {}
		self.activeGames = []

instances = {}

refBot = commands.Bot(command_prefix="!")

async def addToTeam(ctx, teamIndex, role, nameInput):
	instance = getInstance(ctx)
	author = ctx.message.author
	role = role.upper()
	summonerName = buildName(nameInput)
	summonerId = getSummonerId(summonerName)

	async def addSummoner(game, summoner):
		try:
			team = game.activeTeams[teamIndex]
		except:
			game.activeTeams.insert(teamIndex, [])
			team = game.activeTeams[teamIndex]

		if team.captain == author:
			callback = team.add(summoner, role)
			print(callback)
			await refBot.say("```{summonerName} is now {role} for {teamName}```".format(summonerName=summoner.name, role=role, teamName=team.name))
		else:
			await refBot.say("{}, you are not currently the captain of {}".format(author, team.name))

	for game in instance.activeGames:
		activeSummoners = game.activeSummoners
		for summoner in activeSummoners:
			if summoner.id == summonerId:
				await addSummoner(game, summoner)
				break

def buildName(nameInput):
	summonerName = ''
	for part in nameInput:
		summonerName += part
	return summonerName

def getInstance(ctx):
	server = ctx.message.server
	instance = instances[server.id]
	return instance

def getSummonerId(summonerName):
	try:
		requestUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'.format(summonerName, Secrets.apiKey)
		getRequest = requests.get(requestUrl)
		summonerDetails = getRequest.json()
		return summonerDetails["id"]
	except:
		return False

def getSummonerFromMember(memberId):
	memberData = db.getMember(memberId)
	if memberData:
		summonerId = memberData[1]
		return summonerId
	else:
		print('Member could not be found')
		return None

@refBot.command(pass_context=True)
async def a(ctx, role, *nameInput):
	teamIndex = 0
	await addToTeam(ctx, teamIndex, role, nameInput)

@refBot.command(pass_context=True)
async def aye(ctx, *nameInput):
	instance = getInstance(ctx)
	activeGames = instance.activeGames
	currentPlayers = instance.currentPlayers

	if len(activeGames) < 1:
		await refBot.say('```There are currently no active games to join. Use the open command to start a new game.```')
		return

	if nameInput:
		summonerName = buildName(nameInput)
		summonerId = getSummonerId(summonerName)
		if summonerId == False:
			await refBot.say('A summoner with the name, `{}`, could not be found.'.format(summonerName))
			return
	else:
		member = ctx.message.author
		summonerId = getSummonerFromMember(member.id)

	if summonerId in currentPlayers:
		await refBot.say('`{}` is already an active player.'.format(summonerName))
		return

	summoner = go.Summoner(summonerId)
	if type(summoner) == str:
		# The Summoner object fail response is a string
		await refBot.say('```{}```'.format(summoner))

	for game in activeGames:
		activeSummoners = game.activeSummoners
		if len(activeSummoners) < 10:
			added = game.addSummoner(summoner)
			if added:
				currentPlayers[summoner.id] = game.name
				index = activeGames.index(game)
				await refBot.say('`{}` has been added to `Game {}`'.format(summoner.name, index))
			else:
				await refBot.say('Something went wrong with adding the summoner to game, {}.'.format(game.name))
			break

@refBot.command(pass_context=True)
async def b(ctx, role, *nameInput):
	teamIndex = 1
	await addToTeam(ctx, teamIndex, role, nameInput)

@refBot.command(pass_context=True)
async def bye(ctx, *nameInput):
	instance = getInstance(ctx)
	activeGames = instance.activeGames
	currentPlayers = instance.currentPlayers

	if nameInput:
		summonerName = buildName(nameInput)
		summonerId = getSummonerId(summonerName)
		failResponse = '`{}` is not currently an active player.'.format(summonerName)
	else:
		member = ctx.message.author
		summonerId = getSummonerFromMember(member.id)
		failResponse =	'`{}` is not currently an active player.'.format(member.nick)

	if summonerId not in currentPlayers:
		await refBot.say('{}'.format(failResponse))
	else:
		gameName = currentPlayers[summonerId]
		for game in activeGames:
			if game.name == gameName:
				response = game.rmSummoner(summonerId)
				del currentPlayers[summonerId]
				await refBot.say("{}".format(response))
				return
			else:
				await refBot.say("{}".format(failResponse))

@refBot.command(pass_context=True)
async def captain(ctx, gameIndex, team):
	instance = getInstance(ctx)
	author = ctx.message.author
	game = instance.activeGames[int(gameIndex)]
	team = team.upper()
	
	if team == 'A':
		teamIndex = 0
	elif team == 'B':
		teamIndex = 1
	else:
		await refBot.say("```An invalid team was provided. Please select either A or B.```")
	
	team = game.activeTeams[teamIndex]
	team.captain = author

	await refBot.say("```{} is now the captain for {}.```".format(team.captain, team.name))

@refBot.command(pass_context=True)
async def close(ctx, gameIndex):
	instance = getInstance(ctx)
	activeGames = instance.activeGames
	currentPlayers = instance.currentPlayers

	try:
		game = activeGames[int(gameIndex)]
		playersToRemove = []

		for summonerId, gameName in currentPlayers.items():
			if gameName == game.name:
				playersToRemove.append(summonerId)

		for summonerId in playersToRemove:
			del currentPlayers[summonerId]

		del activeGames[int(gameIndex)]
		await refBot.say('```Game {} has been closed. You may give the open command if you would like to start a new one.```'.format(str(gameIndex)))
	except:
		await refBot.say('```The game in question could not be found.```')

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
	await refBot.say("```{}```".format(response))

@refBot.command(pass_context=True)
async def init(ctx):
	server = ctx.message.server
	instance = Instance(server)
	instances[server.id] = instance
	await refBot.say('New instance created for {}.'.format(server.name))
	print(instances)

@refBot.command(pass_context=True)
async def me(ctx, *nameInput):
	member = ctx.message.author
	summonerName = buildName(nameInput)
	summonerId = getSummonerId(summonerName)
	callback = db.uploadMember(member.id, summonerId)
	success = "`{member}` is now tied to the summoner, `{summoner}`.".format(member=member.nick, summoner=summonerName)
	failure = "```Could not tie member, {member}, to a summoner with the name, {summoner}```".format(member=member.nick, summoner=summonerName)

	if callback:
		print(callback)
		await refBot.say(success)
	else:
		await refBot.say(failure)

@refBot.command(pass_context=True)
async def open(ctx):
	instance = getInstance(ctx)
	activeGames = instance.activeGames
	game = go.Game()

	if len(activeGames) > 0:
		activeGames.append(game)
	else:
		activeGames.insert(1, game)

	print('Controller --> open: ', game)

	db.saveGame(game)

	await refBot.say('@everyone A new game is open to enrollment! Type "!aye YourSummonerName" into the "RollCall" chat to join the game.')

@refBot.command(pass_context=True)
async def option(ctx, gameIndex, opt, *optValue):
	instance = getInstance(ctx)
	game = instance.activeGames[int(gameIndex)]
	game.setOption(opt, optValue)

@refBot.command(pass_context=True)
async def roles(ctx, primary, secondary, *nameInput):
	instance = getInstance(ctx)
	activeGames = instance.activeGames
	currentPlayers = instance.currentPlayers
	primary = primary.upper()
	secondary = secondary.upper()

	if nameInput:
		summonerName = buildName(nameInput)
		summonerId = getSummonerId(summonerName)
	else:
		member = ctx.message.author
		summonerId = getSummonerFromMember(member.id)

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
		await refBot.say("```The following roles were not recognized: \"{}\". Please use only the following in the roles command: TOP, JNG, MID, ADC, SUP, FILL```".format(invalidRoles))
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

@refBot.command(pass_context=True)
async def rollCall(ctx):
	instance = getInstance(ctx)
	activeGames = instance.activeGames

	if activeGames:
		response = ''
		for game in activeGames:
			response += 'Game {} -->\n'.format(str(activeGames.index(game)))
			response += game.rollCall()
			response += '\n\n\n'

		await refBot.say("```{}```".format(response))
	else:
		await refBot.say("```There are no games currently open. Give the open command to start a new one.```")

@refBot.command(pass_context=True)
async def save(ctx, gameIndex):
	instance = getInstance(ctx)
	game = instance.activeGames[int(gameIndex)]
	db.saveGame(game)

@refBot.command()
async def setupDb():
	db.setupDb()

@refBot.command(pass_context=True)
async def start(ctx, gameIndex):
	instance = getInstance(ctx)
	activeGames = instance.activeGames
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
			msgTeamB += '{}. {}\n'.format(str(i), summoner.name)

		if game.draft.rChamps:
			msgTeamB += 'The champion pool for Team B is: ' + '\n' + randomChamps(rChamps)
		print(msgTeamB)

		response = msgTeamA + '\n\n\n' + msgTeamB

		await refBot.say("```{}```".format(response))

	elif draftType == 'MANUAL':
		async def getTeamRoster(team):
			players = team.getPlayers()
			roster = ''
			for role, summoner in players.items():
				try:
					summonerName = summoner.name
				except:
					summonerName = summoner
				roster += '{}: {}\n'.format(role, summonerName)
			await refBot.say("```{} -->\n\n{}```".format(team.name, roster))


		teamA = game.activeTeams[0]
		teamB = game.activeTeams[1]
		await getTeamRoster(teamA)
		await getTeamRoster(teamB)

	# asyncio.sleep(900)
	# try:
	# 	# requestUrl = 'https://na1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/' + str(summonerId) + '?api_key=' + Secrets.apiKey
	# 	requestUrl = 'https://na1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/{}?api_key={}'.format(str(summonerId), Secrets.apiKey)
	# 	getRequest = requests.get(requestUrl)
	# 	lolGame = getRequest.json()
	# 	print(lolGame)
	# 	await refBot.say(lolGame["gameId"])
	# except:
	# 	print('No game started... yet')

@refBot.command(pass_context=True)
async def test(ctx):
	channel = ctx.message.channel
	author = ctx.message.author
	server = ctx.message.server
	color = discord.Colour('#aa0d0d')
	em = discord.Embed(title='My Embed Title', description='My Embed Content.', colour=0xDEADBF)
	msg = 'Hello world!'
	await refBot.say('me:' + str(author.id))
	print('Server Name:', server.name, 'Server ID :', server.id, 'Channel :', channel, 'Author :', author, 'Nickname :', author.nick)
	await refBot.send_message(channel, msg, tts=False, embed=em)

@refBot.command(pass_context=True)
async def users(ctx):
	client = discord.Client()
	members = client.get_all_members()
	member = iter(members)
	print('Next member :', member)
	print('Client Object :', client, '\nMembers :', members)

@refBot.command()
async def newTable():
	db.addTable()

@refBot.command(pass_context=True)
async def key(ctx, newKey):
	author = ctx.message.author
	apiKey = Secrets.apiKey
	admin = Secrets.admin

	if int(author.id) == admin:
		apiKey = newKey
		print('New API key provided :' + Secrets.apiKey)
	else:
		await refBot.say('You do not have the proper permissions for this command.')

refBot.run(Secrets.botToken)