import APICalls
a = APICalls
import DbCalls
d = DbCalls
import Objects
o = Objects

def addSummonerToGame(summonerData):
	summonerName = summonerData

def getSummonerData(summonerName):
	summonerData = d.getSummoner(summonerName)
	return summonerData

def getSummonerDetails(summonerName):
	summonerData = a.getSummoner(summonerName)
	summonerRank = a.getRank(summonerName)
	summonerDetails = {"data": summonerData, "rank": summonerRank}
	return summonerDetails

def onAddCmd(summonerName):
	summonerDetails = getSummonerDetails(summonerName)
	rankInfo = summonerDetails["rank"]
	tier = rankInfo["tier"]
	rank = rankInfo["rank"]
	value = placeSummoner(rankInfo)

	#summoner = [(summonerName, tier, rank, value)]
	d.uploadSummoner(summonerName, tier, rank, value)
	#summoner = o.Summoner(summonerName, tier, rank, value)
	#d.uploadSummoner(summoner)

def onAyeCmd(summonerName):
	summonerData = getSummonerData(summonerName)
	if(summonerData):
		addSummonerToGame(summonerData)
		return summonerName + ' has joined the active players group.'
	else:
		addNewSummoner(summonerName)
		return summonerName + ' was not found in the LittleLeague Summoner database. They have been added. Run the !aye command again to add them as an active player.'

def onByeCmd(summonerName):
	if activePlayers.count(summonerName) > 0:
		del o.activePlayers[summonerName]
		return 'Catch you later, ' + summonerName + '!'
	else:
		return 'Sorry, but ' + summonerName + ' is not an active player.'

def placeSummoner(rankInfo):
	tier = rankInfo["tier"]
	rank = rankInfo["rank"]

	if tier == 'UNRANKED':
		summonerValue = 0.00
	elif tier == "BRONZE":
		if rank == "V":
			summonerValue = 0.00
		elif rank == "IV":
			summonerValue = 4.46
		elif rank == "III":
			summonerValue = 9.36
		elif rank == "II":
			summonerValue = 14.89
		elif rank == "I": 
			summonerValue = 20.85
	elif tier == "SILVER":
		if rank == "V":
			summonerValue = 26.36
		elif rank == "IV":
			summonerValue = 37.45
		elif rank == "III":
			summonerValue = 45.90
		elif rank == "II":
			summonerValue = 54.08
		elif rank == "I": 
			summonerValue = 61.52
	elif tier == "GOLD":
		if rank == "V":
			summonerValue = 66.33
		elif rank == "IV":
			summonerValue = 75.75
		elif rank == "III":
			summonerValue = 80.18
		elif rank == "II":
			summonerValue = 83.72
		elif rank == "I": 
			summonerValue = 86.13
	elif tier == "PLATINUM":
		if rank == "V":
			summonerValue = 89.68
		elif rank == "IV":
			summonerValue = 93.03
		elif rank == "III":
			summonerValue = 94.73
		elif rank == "II":
			summonerValue = 96.17
		elif rank == "I": 
			summonerValue = 97.30
	elif tier == "DIAMOND":
		if rank == "V":
			summonerValue = 97.89
		elif rank == "IV":
			summonerValue = 99.20
		elif rank == "III":
			summonerValue = 99.58
		elif rank == "II":
			summonerValue = 99.78
		elif rank == "I": 
			summonerValue = 99.89
	elif tier == "MASTER":
		summonerValue = 99.97
	elif tier == "CHALLENGER":
		summonerValue = 100

	summonerValue += rankInfo["leaguePoints"] * .0001
	return summonerValue
