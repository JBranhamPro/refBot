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
	
	try:
		rankInfoUrl = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + summonerId + '?api_key=' + apiKey
		rankInfoApiRequest = requests.get(rankInfoUrl)
		rawRankInfoData = rankInfoApiRequest.json()
		if rawSummonerData[1]:
			rawRankInfo = rawRankInfoData[1]
		else: 
			rawRankInfo = rawRankInfoData[0]
	except:
		rawRankInfo = {'tier':'UNRANKED', 'rank': '', 'leaguePoints': 0}

	return rawRankInfo

def getSummoner(summonerName):
	summonerUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + '?api_key=' + apiKey
	summonerApiRequest = requests.get(summonerUrl)
	rawSummonerData = summonerApiRequest.json()
	return rawSummonerData