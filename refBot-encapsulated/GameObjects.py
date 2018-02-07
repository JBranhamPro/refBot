import requests
import json
import uuid
from itertools import combinations
import time
import DbCalls as db
import Secrets as s
apiKey = s.apiKey

############################################################################################################
##																										  ##
##											SUMMONER OBJECT												  ##
##																										  ##
############################################################################################################

class Summoner:

	def __init__(self, summonerId):
		summonerData = db.getSummonerData(summonerId)
		
		if summonerData:
			self.id = summonerId
			self.name = summonerData[1]
			self.tier = summonerData[2]
			self.rank = summonerData[3]
			self.value = summonerData[4]
			self.primary = summonerData[5]
			self.secondary = summonerData[6]
			self.gameId = summonerData[7]

		elif summonerData is None:
			summonerData = self.getSummonerData(summonerId)
			summonerDetails = summonerData["details"]
			rankInfo = summonerData["rank"]

			self.id = summonerId
			self.name = summonerDetails["name"]
			self.tier = rankInfo["tier"]
			self.rank = rankInfo["rank"]
			self.value = self.getRankValue(rankInfo)
			self.primary = 'FILL'
			self.secondary = 'FILL'
			self.gameId = 'inactive'
		else:
			print(summonerData)
			return False, 'A summoner with the name, ' + str(summonerName) + ', could not be found.'


	def getRank(self, summonerId):		
		rankInfoUrl = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + summonerId + '?api_key=' + apiKey
		rankInfoApiRequest = requests.get(rankInfoUrl)
		rawRankJson = rankInfoApiRequest.json()

		soloQData = None
		flexQData = None

		print('GameObjects --> Summoner.getRank : ', rawRankJson)

		for queueData in rawRankJson:
			if queueData["queueType"] == 'RANKED_SOLO_5x5':
				soloQData = queueData
			elif queueData["queueType"] == 'RANKED_FLEX_SR':
				flexQData = queueData

		if soloQData:
			rankInfo = soloQData
		elif flexQData:
			rankInfo = flexQData
		else:
			rankInfo = {'tier':'UNRANKED', 'rank': '', 'leaguePoints': 0}

		return rankInfo

	def getRankValue(self, rankInfo):
		tier = rankInfo["tier"]
		rank = rankInfo["rank"]

		if tier == 'UNRANKED':
			rankValue = 0.00
		elif tier == "BRONZE":
			if rank == "V":
				rankValue = 0.00
			elif rank == "IV":
				rankValue = 4.46
			elif rank == "III":
				rankValue = 9.36
			elif rank == "II":
				rankValue = 14.89
			elif rank == "I": 
				rankValue = 20.85
		elif tier == "SILVER":
			if rank == "V":
				rankValue = 26.36
			elif rank == "IV":
				rankValue = 37.45
			elif rank == "III":
				rankValue = 45.90
			elif rank == "II":
				rankValue = 54.08
			elif rank == "I": 
				rankValue = 61.52
		elif tier == "GOLD":
			if rank == "V":
				rankValue = 66.33
			elif rank == "IV":
				rankValue = 75.75
			elif rank == "III":
				rankValue = 80.18
			elif rank == "II":
				rankValue = 83.72
			elif rank == "I": 
				rankValue = 86.13
		elif tier == "PLATINUM":
			if rank == "V":
				rankValue = 89.68
			elif rank == "IV":
				rankValue = 93.03
			elif rank == "III":
				rankValue = 94.73
			elif rank == "II":
				rankValue = 96.17
			elif rank == "I": 
				rankValue = 97.30
		elif tier == "DIAMOND":
			if rank == "V":
				rankValue = 97.89
			elif rank == "IV":
				rankValue = 99.20
			elif rank == "III":
				rankValue = 99.58
			elif rank == "II":
				rankValue = 99.78
			elif rank == "I": 
				rankValue = 99.89
		elif tier == "MASTER":
			rankValue = 99.97
		elif tier == "CHALLENGER":
			rankValue = 100

		rankValue += rankInfo["leaguePoints"] * .0001
		return rankValue

	def getSummonerData(self, summonerId):
		summonerId = str(summonerId)
		summonerDetails = self.getSummonerDetails(summonerId)
		summonerRank = self.getRank(summonerId)
		summonerData = {"details": summonerDetails, "rank": summonerRank}
		return summonerData

	def getSummonerDetails(self, summonerId):
		summonerUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/' + str(summonerId) + '?api_key=' + apiKey
		summonerApiRequest = requests.get(summonerUrl)
		summonerDetails = summonerApiRequest.json()
		return summonerDetails

	def setRoles(self, primary, secondary):
		self.primary = primary
		self.secondary = secondary

	def __str__(self):
		return self.name

############################################################################################################
##																										  ##
##												GAME OBJECT												  ##
##																										  ##
############################################################################################################

class Game:

	def __init__(self):
		self.id = str(uuid.uuid4())
		self.name = db.createGameName(self.id)
		self.startTime = None
		self.activeSummoners = []
		self.activeTeams = []
		self.draft = Draft()

		self.activeTeams = [Team('A'), Team('B')]

	def addSummoner(self, summoner):
		activeSummoners = self.activeSummoners

		for player in activeSummoners:
			if player.id == summoner.id:
				print(player.id, summoner.id)
				return False

		activeSummoners.append(summoner)
		summoner.gameId = self.id
		db.updateSummoner(summoner)
		return True

	def rmSummoner(self, summonerId):
		activeSummoners = self.activeSummoners

		for summoner in activeSummoners:
			if summoner.id == summonerId:
				activeSummoners.remove(summoner)
				summoner.gameId = 'inactive'
				db.updateSummoner(summoner)
				return 'Catch you later, ' + summoner.name + '!'

	def rollCall(self):
		rollCallMsg = ''
		i = 0
		for summoner in self.activeSummoners:
			i+=1
			s = summoner 
			
			placeStr = str(i) + '. '
			rankStr = s.tier + ' ' + s.rank + ' '
			roleStr = '(' + s.primary + '/' + s.secondary + ')'

			rollCallMsg += placeStr + s.name + ' : ' + rankStr + ' ' + roleStr + '\n'

		return rollCallMsg

	def setOption(self, option, optValue = 15):
		option = option.upper()
		draft = self.draft

		if option == 'MANUAL' or option == 'MATCHMADE' or option == 'RANDOM':
			draft.type = option
		
		elif option == 'RLANES':
			draft.rLanes = True
		elif option == 'RCHAMPS':
			draft.rChamps = optValue
		else:
			print(option + ' is not a valid draft option.')

	def start(self):
		dType = self.draft.type

		if dType == 'MANUAL':
			self.draft.manual()

		elif dType == 'MATCHMADE':
			teams = self.draft.matchmade(self.activeSummoners)

			i = 0
			for team in self.activeTeams:
				for summoner in teams[i]:
					team.add(summoner)
				i+=1

			return True

		elif dType == 'RANDOM':
			draftMsg = self.random()

	def __str__(self):
		return self.name

############################################################################################################
##																										  ##
##												DRAFT OBJECT											  ##
##																										  ##
############################################################################################################

class Draft:
	
	def __init__(self):
		self.rChamps = 0
		self.rLanes = False
		self.type = 'MANUAL'

	def getChampList(self):
		champUrl = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false&api_key=' + apiKey
		champApiRequest = requests.get(champUrl)
		rawChampData = champApiRequest.json()
		champData = rawChampData["data"]
		champList = []

		for champEntry in champData:
			champ = champData[champEntry]
			champList.append(champ["name"])

		return champList

	def matchmade(self, activeSummoners):
		bestTeamA = []
		bestTeamB = []
		prevValDiff = 100
		newValDiff = 0
		numOfSumms = len(activeSummoners)
		teamSize = int(numOfSumms/2)

		for team in combinations(activeSummoners, teamSize):
			players = activeSummoners.copy()
			teamA = []
			teamB = []
			valueA = 0
			valueB = 0

			for player in team:
				print(player.name)
				summonerValue = player.value
				valueA += summonerValue
				teamA.append(player)
				players.remove(player)

			for player in players:
				print(player.name)
				summonerValue = player.value
				valueB += summonerValue
				teamB.append(player)

			newValDiff = abs(valueA - valueB)
			if newValDiff < prevValDiff:
				prevValDiff = newValDiff

				bestTeamA.clear()
				bestTeamB.clear()

				bestTeamA = teamA
				bestTeamB = teamB

		return (bestTeamA, bestTeamB)

	def randomChamps(self, poolSize):
		from random import randint

		champList = self.getChampList()
		champPool = []

		champsDrafted = 0
		while champDrafted < poolSize:
			champ = champList[randint(0, len(champList))]
			champPool.append(champ)
			champList.remove(champ)
			champsDrafted+=1

		responseMsg = ''

		for champ in champPool:
			champ += '\n'
			responseMsg += champ

############################################################################################################
##																										  ##
##												TEAM OBJECT											  	  ##
##																										  ##
############################################################################################################

class Team:
	"""docstring for Team"""
	def __init__(self, teamPos):
		self.id = str(uuid.uuid4())
		self.name = 'New Team ' + teamPos
		self.summoners = {}
		self.top = 'open'
		self.jng = 'open'
		self.mid = 'open'
		self.adc = 'open'
		self.sup = 'open'

	def add(self, summoner):
		self.summoners[summoner.id] = summoner