import random
from random import randint
import operator
import requests
import json
import secrets
from itertools import permutations
apiKey = secrets.apiKey

playerNames = []
littleLeaguers = {}
champsA = []
champsB = []
teamA = []
teamB = []
roleOrder = []

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
		try: 
			rawRankInfo = rawRankInfoData[1]
		except: 
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

def getChampList():
	champUrl = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false&api_key=' + apiKey
	champApiRequest = requests.get(champUrl)
	rawChampData = champApiRequest.json()
	champData = rawChampData["data"]
	champList = []

	for champEntry in champData:
		champ = champData[champEntry]
		champList.append(champ["name"])

	return champList

def rLanes():	
	roles = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
	playersDrafted = 0

	while len(roles) > 0:
		draftedRole = randint(0,len(roles) - 1)
		roleOrder.append(roles[draftedRole])
		del roles[draftedRole]

def rChamps(x):
	n = int(x)
	champList = getChampList()

	if n > len(champList):
		n = len(champList)

	def pullChamps(team):
		champsDrafted = 0
		while champsDrafted < n:
			champion = randint(0,len(champList) - 1)
			if team == 'a':
				champsA.append('                ' + str(champsDrafted + 1) + '. ' + champList[champion] + '\n')
			else:
				champsB.append('                ' + str(champsDrafted + 1) + '. ' + champList[champion] + '\n')
			del champList[champion]
			champsDrafted += 1

	pullChamps('a')
	pullChamps('b')

def autoDraft():
	print('autoDraft has started')
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
			placeSumm(name)
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
		teamA.append(player)

	teamB.clear()
	for player in bestB:
		teamB.append(player)
