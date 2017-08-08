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

refBot = commands.Bot(command_prefix="!")
apiKey = ''
botToken = ''
playerNames = []
littleLeaguers = {}

def getSummoner(summoner):
	summonerUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summoner + '?api_key=' + apiKey
	summonerApiRequest = requests.get(summonerUrl)
	rawSummonerData = summonerApiRequest.json()
	return rawSummonerData

def getRank(summoner):
	rawSummonerData = getSummoner(summoner)
	summonerId = str(rawSummonerData["id"])
	try:
		rankInfoUrl = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + summonerId + '?api_key=' + apiKey
		rankInfoApiRequest = requests.get(rankInfoUrl)
		rawRankInfoData = rankInfoApiRequest.json()
		rawRankInfo = rawRankInfoData[0]
	except:
		rawRankInfo = {'tier':'UNRANKED', 'rank': '', 'leaguePoints': 0}
	return rawRankInfo

def placeSumm(summoner):
	rawRankInfo = getRank(summoner)
	rawSummonerData = getSummoner(summoner)
	tier = rawRankInfo["tier"]
	rank = rawRankInfo["rank"]

	if tier == 'UNRANKED':
		playerRank = 0
	elif tier == "BRONZE":
		playerRank = 1
	elif tier == "SILVER":
		playerRank = 2
	elif tier == "GOLD":
		playerRank = 3
	elif tier == "PLATINUM":
		playerRank = 4
	elif tier == "DIAMOND":
		playerRank = 5
	elif tier == "MASTER":
		playerRank = 6
	elif tier == "CHALLENGER":
		playerRank = 7
	else:
		print("No tier information available")

	if rank == "V":
		playerRank += .0
	elif rank == "IV":
		playerRank += .1
	elif rank == "III":
		playerRank += .2
	elif rank == "II":
		playerRank += .3
	elif rank == "I":
		playerRank += .4
	else:
		print("No rank available")

	playerRank += rawRankInfo["leaguePoints"] * .001

	littleLeaguers[rawSummonerData["name"]] = playerRank
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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
#_TEST_######################################################################################################
@refBot.command()
async def test():
	await refBot.say('What am I?')
#_RANDOMCHAMPS_##############################################################################################
@refBot.command()
async def randomChamps(x):
	n = int(x)
	champUrl = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false&api_key=' + apiKey
	champApiRequest = requests.get(champUrl)
	rawChampData = champApiRequest.json()
	champData = rawChampData["data"]
	champList = []
	draftedChamps = []

	for champEntry in champData:
		champ = champData[champEntry]
		champList.append(champ["name"])

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
#_RANK_######################################################################################################
@refBot.command()
async def rank(summoner):
	rawRankInfo = getRank(summoner)
	rawSummonerData = getSummoner(summoner)
	rankInfo = rawSummonerData["name"] + " = " + rawRankInfo["tier"] + " " + rawRankInfo["rank"] + " " + str(rawRankInfo["leaguePoints"]) + " LP"

	await refBot.say(rankInfo)
#_AYE_#######################################################################################################
@refBot.command()
async def aye(summonerName):
	
	try:
		rawSummonerData = getSummoner(summonerName)
		summoner = rawSummonerData["name"]
	except:
		await refBot.say('\"' + summonerName + '\"' + ' is an invalid summoner name.')
		return

	if playerNames.count(summoner) > 0:
		await refBot.say('STOP RIGHT THERE! You can only enter your name in the roster once!')
	else:	
		playerNames.append(summoner)

	if len(playerNames) > 9:
		await refBot.say('We now have ten players, tell me to !rolCall for the roster and we can get started.')
	return playerNames
#_BYE_#######################################################################################################
@refBot.command()
async def bye(summonerName):
	if summonerName == 'all':
		playerNames.clear()
		print('All deleted')
	else:
		try:
			rawSummonerData = getSummoner(summonerName)
			summoner = rawSummonerData["name"]
			playerNames.remove(summoner)
		except:
			print('\"' + summonerName + '\"' + ' is an invalid summoner name.')
			playerNames.remove(summonerName)
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
#_PLACE_#####################################################################################################
@refBot.command()
async def place(summoner):
	if summoner == 'all':
		for name in playerNames:
			placeSumm(name)
		print('All ' + len(playerNames) + ' players have been placed and added to littleLeaguers.')
	else:
		placeSumm(summoner)
#_APLACE#####################################################################################################
@refBot.command()
async def aPlace():
	user = requests.get('https://discordapp.com/api/users/@me')
	print(user)
	summoner = user['username']
	#placeSumm(summoner)
	print(summoner)
	self.place(summoner)
#_ROSTER_#####################################################################################################
@refBot.command()
async def roster():
	rosterMsg = ''
	for k,v in littleLeaguers.items():
		rosterMsg += (k + ' = ' + str(v) + '\n')
	await refBot.say(rosterMsg)
#_ADRAFT_#####################################################################################################
@refBot.command()
async def aDraft():
	tempRoster = littleLeaguers.copy()
	teamA = []
	teamB = []
	rosterA = []
	rosterB = []
	total = 0
	units = 0

	for k, v in tempRoster.items():
		total += v
		units += 1

	average = total / units
	print(average)

	n = units / 2
	def draftTeam():
		teamValue = 0
		over = False
		x = 0
		while x < n:
			draftedPlayer = random.choice(list(tempRoster.keys()))
			playerValue = tempRoster[draftedPlayer]
			if a == True:
				while over == True:
					draftedPlayer = random.choice(list(tempRoster.keys()))
					playerValue = tempRoster[draftedPlayer]
					if playerValue < average:
						over = False
				teamA.append(draftedPlayer)
				teamValue += playerValue
				del tempRoster[draftedPlayer]
			else:
				teamB.append(draftedPlayer)
				teamValue += playerValue
				del tempRoster[draftedPlayer]
			if playerValue > average:
				over = True
			x += 1
		print(teamValue)

	a = True
	draftTeam()
	a = False
	draftTeam()

	for i in teamA:
		rosterA.append((str(teamA.index(i) + 1) + '. ' + i + '\n'))
	msgTeamA = "".join(rosterA)

	for i in teamB:
		rosterB.append((str(teamB.index(i) + 1) + '. ' + i + '\n'))
	msgTeamB = "".join(rosterB)

	await refBot.say(msgTeamA + '\n' + '\n' + msgTeamB)
#_FUQU_######################################################################################################
@refBot.command()
async def fuqU():
	await refBot.say("What the fuck did you just fucking say about me, you little bitch? I\'ll have you know I graduated top of my class in the Navy Seals, and I\’ve been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I\’m the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You\’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that\’s just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \“clever\” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn\’t, you didn\’t, and now you\’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You\’re fucking dead, kiddo.")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
refBot.run(botToken)