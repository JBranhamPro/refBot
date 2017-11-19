import requests
import json
import Secrets
s = Secrets
apiKey = s.apiKey

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

def getRank(summonerName):
	rawSummonerData = getSummoner(summonerName)
	summonerId = str(rawSummonerData["id"])
	
	rankInfoUrl = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + summonerId + '?api_key=' + apiKey
	rankInfoApiRequest = requests.get(rankInfoUrl)
	rawRankInfoData = rankInfoApiRequest.json()

	for queueData in rawRankInfoData:
		if queueData["queueType"] == 'RANKED_SOLO_5x5':
			soloQData = queueData
		elif queueData["queueType"] == 'RANKED_FLEX_SR':
			flexQData = queueData

	if soloQData:
		rawRankInfo = soloQData
	elif flexQData:
		rawRankInfo = flexQData
	else:
		rawRankInfo = {'tier':'UNRANKED', 'rank': '', 'leaguePoints': 0}

	return rawRankInfo

def getSummonerDetails(summonerName):
	summonerUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + '?api_key=' + apiKey
	summonerApiRequest = requests.get(summonerUrl)
	summonerDetails = summonerApiRequest.json()
	return summonerDetails
