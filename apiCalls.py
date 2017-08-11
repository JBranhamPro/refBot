import random
from random import randint
import operator
import requests
import json
import secrets
apiKey = secrets.apiKey

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