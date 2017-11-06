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
	flexQData = rawRankInfoData[0]
	soloQData = rawRankInfoData[1]
	if soloQData:
		print(soloQData)
		rawRankInfo = soloQData
	elif flexQData: 
		print(flexQData)
		rawRankInfo = flexQData
	else:
		rawRankInfo = {'tier':'UNRANKED', 'rank': '', 'leaguePoints': 0}

	return rawRankInfo

def getSummoner(summonerName):
	summonerUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + '?api_key=' + apiKey
	summonerApiRequest = requests.get(summonerUrl)
	rawSummonerData = summonerApiRequest.json()
	return rawSummonerData