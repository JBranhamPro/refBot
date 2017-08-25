import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)
import asyncio

import random
from random import randint
import operator
import requests
import json
from itertools import permutations

import apiCalls
import secrets

refBot = commands.Bot(command_prefix="!")
playerNames = apiCalls.playerNames
littleLeaguers = apiCalls.littleLeaguers

#_DRAFT_#####################################################################################################
@refBot.command()
async def draft():	
	roles = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
	playersDrafted = 0
	roleOrder = []

	while len(roles) > 0:
		draftedRole = randint(0,len(roles) - 1)
		roleOrder.append(roles[draftedRole] + '\n')
		del roles[draftedRole]

	draftOrder = "".join(roleOrder)
	
	await refBot.say(draftOrder)
#_RANDOMCHAMPS_##############################################################################################
@refBot.command()
async def rChamps(x):
	n = int(x)
	champList = apiCalls.getChampList()
	draftedChamps = []

	if n > len(champList):
		n = len(champList)

	champsDrafted = 0
	while champsDrafted < n:
		champion = randint(0,len(champList) - 1)
		draftedChamps.append(champList[champion] + '\n')
		del champList[champion]
		champsDrafted += 1

	randomChampsMsg = "".join(draftedChamps)

	await refBot.say(randomChampsMsg)
#_AYE_#######################################################################################################
@refBot.command()
async def aye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	try:
		rawSummonerData = apiCalls.getSummoner(summonerName)
		summoner = rawSummonerData["name"]
	except:
		await refBot.say('\"' + summonerName + '\"' + ' is an invalid summoner name.')
		return

	if playerNames.count(summoner) > 0:
		await refBot.say('STOP RIGHT THERE! You can only enter your name in the roster once!')
	else:	
		playerNames.append(summoner)

	if len(playerNames) > 9:
		await refBot.say('We now have ten players, tell me to !rollCall for the roster and we can get started.')
	return playerNames
#_BYE_#######################################################################################################
@refBot.command()
async def bye(*args):
	summonerName = ''
	for ar in args:
		summonerName += ar

	if summonerName == 'all':
		playerNames.clear()
		littleLeaguers.clear()
		print('All deleted')
	else:
		try:
			rawSummonerData = apiCalls.getSummoner(summonerName)
			summoner = rawSummonerData["name"]
			playerNames.remove(summoner)
		except:
			print('\"' + summonerName + '\"' + ' is an invalid summoner name.')
			playerNames.remove(summonerName)
		try:
			del littleLeaguers[summonerName]
		except:
			print(summonerName + ' was not placed.')
	return playerNames
#_ROLLCALL_##################################################################################################
@refBot.command()
async def rollCall():
	playerList = []
	for i in playerNames:
		plyrNum = playerNames.index(i) + 1
		playerList.append(str(plyrNum) + '. ' + i + '\n')
	playing = "".join(playerList)
	await refBot.say(playing)
#_APLACE#####################################################################################################
@refBot.command()
async def aPlace():
	user = requests.get('https://discordapp.com/api/users/@me')
	print(user)
#_ROSTER_#####################################################################################################
@refBot.command()
async def roster():
	rosterMsg = ''
	for k,v in littleLeaguers.items():
		rosterMsg += (k + ' = ' + str(v) + '\n')
	await refBot.say(rosterMsg)
#_AUTODRAFT_###################################################################################################
@refBot.command()
async def autoDraft():
	teamA = []
	teamB = []
	bestA = []
	bestB = []
	valueA = 0
	valueB = 0
	prevVal = 100
	newVal = 0

	for name in playerNames:
		if name in littleLeaguers:
			print("Validated " + name + " as a Little Leaguer.")
		else:
			apiCalls.placeSumm(name)
			print(name + " has been placed.")

	for permutation in permutations(playerNames, 5):
		print(permutation)
		teamA.clear()
		teamB.clear()
		valueA = 0
		valueB = 0
		tempRoster = littleLeaguers.copy()
		for name in permutation:
			teamA.append(name)
			valueA += tempRoster[name]
			del tempRoster[name]
		for k, v in tempRoster.items():
			teamB.append(k)
			valueB += v
		newVal = abs(valueA - valueB)
		if newVal < prevVal:
			prevVal = newVal
			bestA = teamA.copy()
			bestB = teamB.copy()

	teamA.clear()
	for player in bestA:
		teamA.append(player + '\n')
	await refBot.say('Team A is:\n\n' + "".join(teamA) + 'with a value of: ' + str(valueA))

	teamB.clear()
	for player in bestB:
		teamB.append(player + '\n')
	await refBot.say('Team B is:\n\n' + "".join(teamB) + 'with a value of: ' + str(valueB))
#_FOR MAX_######################################################################################################
@refBot.command()
async def fuqU():
	await refBot.say("What the fuck did you just fucking say about me, you little bitch? I\'ll have you know I graduated top of my class in the Navy Seals, and I\’ve been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I\’m the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You\’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that\’s just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \“clever\” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn\’t, you didn\’t, and now you\’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You\’re fucking dead, kiddo.")

refBot.run(secrets.botToken)
