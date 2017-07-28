import discord
from discord.ext import commands

import logging
logging.basicConfig(level=logging.INFO)

import asyncio

from random import randint
import requests
import json

refBot = commands.Bot(command_prefix="!")
apiKey = ''
playerNames = []
###########################################################################################################
@refBot.command()
async def draft():	
	roles = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
	playersDrafted = 0
	roleOrder = []

	while playersDrafted < 5:
		draftedRole = randint(0,4)
		try:
			roleOrder.append(roles[draftedRole] + '\n')
			del roles[draftedRole]
			playersDrafted +=1
		except:
			continue

	draftOrder = "".join(roleOrder)
	
	await refBot.say(draftOrder)
###########################################################################################################
@refBot.command()
async def test():
	await refBot.say('What am I?')
###########################################################################################################
@refBot.command()
async def randomChamps(x):
	n = int(x)
	champUrl = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false&api_key=' + apiKey
	champApiRequest = requests.get(champUrl)
	rawChampData = champApiRequest.json()
	champData = rawChampData["data"]
	champList = []

	for champEntry in champData:
		champ = champData[champEntry]
		champList.append(champ["name"])

	champsDrafted = 0
	draftedChamps = []

	if n > len(champList):
		n = len(champList)

	while champsDrafted < n:
		champion = randint(0,len(champList) - 1)
		try:
			draftedChamps.append(champList[champion] + '\n')
			del champList[champion]
			champsDrafted += 1
		except:
			continue

	randomChampsMsg = "".join(draftedChamps)

	await refBot.say(randomChampsMsg)
###########################################################################################################
@refBot.command()
async def rank(summoner):
	summonerUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summoner + '?api_key=' + apiKey
	summonerApiRequest = requests.get(summonerUrl)
	rawSummonerData = summonerApiRequest.json()
	summonerId = str(rawSummonerData["id"])

	rankInfoUrl = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + summonerId + '?api_key=' + apiKey
	rankInfoApiRequest = requests.get(rankInfoUrl)
	rawRankInfoData = rankInfoApiRequest.json()
	rawRankInfo = rawRankInfoData[0]
	rankInfo = rawSummonerData["name"] + " = " + rawRankInfo["tier"] + " " + rawRankInfo["rank"] + " " + str(rawRankInfo["leaguePoints"]) + " LP"

	await refBot.say(rankInfo)
###########################################################################################################
@refBot.command()
async def aye(summonerName):
	playerNames.append(summonerName)
	if len(playerNames) > 9:
		await refBot.say('We now have ten players, tell me to !roleCall for the roster and we can get started.')
	return playerNames
###########################################################################################################
@refBot.command()
async def bye(summonerName):
	if summonerName == 'all':
		n = 0
		while n < len(playerNames):
			del playerNames[n]
			n += 1
		print('All deleted')
	else:
		playerNames.remove(summonerName)
	return playerNames
###########################################################################################################
@refBot.command()
async def roleCall():
	playerList = []
	for i in playerNames:
		plyrNum = playerNames.index(i)
		playerList.append(str(plyrNum + 1) + '. ' + i + '\n')
	playing = "".join(playerList)
	await refBot.say(playing)
###########################################################################################################
@refBot.command()
async def fuqU():
	await refBot.say("What the fuck did you just fucking say about me, you little bitch? I\'ll have you know I graduated top of my class in the Navy Seals, and I\’ve been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I\’m the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You\’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that\’s just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \“clever\” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn\’t, you didn\’t, and now you\’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You\’re fucking dead, kiddo.")
###########################################################################################################
refBot.run('')
