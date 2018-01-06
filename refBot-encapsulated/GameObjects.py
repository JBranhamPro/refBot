import requests
import json
import uuid
import DbCalls as db
import Secrets as s
apiKey = s.apiKey

############################################################################################################
##																										  ##
##											SUMMONER OBJECT												  ##
##																										  ##
############################################################################################################

class Summoner:

	def __init__(self, summonerName):
		summonerData = self.getSummonerData(summonerName)
		if summonerData:
			summonerDetails = summonerData["details"]
			rankInfo = summonerData["rank"]

			self.id = summonerDetails["id"]
			self.name = summonerDetails["name"]
			self.tier = rankInfo["tier"]
			self.rank = rankInfo["rank"]
			self.value = self.getRankValue(rankInfo)
			self.primary = 'FILL'
			self.secondary = 'FILL'
			self.gameId = 'inactive'
		else:
			print(summonerData)
			return 'A summoner with the name, ' + str(summonerName) + ', could not be found.'

	def getId(self, summonerName):
		summonerDetails = self.getSummonerDetails(summonerName)
		return summonerDetails["id"]

	def getRank(self, summonerName):
		summonerDetails = self.getSummonerDetails(summonerName)
		summonerId = str(summonerDetails["id"])
		
		rankInfoUrl = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + summonerId + '?api_key=' + apiKey
		rankInfoApiRequest = requests.get(rankInfoUrl)
		rawRankJson = rankInfoApiRequest.json()

		soloQData = None
		flexQData = None

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

	def getSummonerData(self, summonerName):
		summonerDetails = self.getSummonerDetails(summonerName)
		summonerRank = self.getRank(summonerName)
		summonerData = {"details": summonerDetails, "rank": summonerRank}
		return summonerData

	def getSummonerDetails(self, summonerName):
		summonerUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + '?api_key=' + apiKey
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
		self.startTime = None
		self.activeSummoners = []
		self.activeTeams = []
		self.draft = Draft(self)
		self.type = 'MANUAL'
		self.rChamps = 0
		self.rlanes = False

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

			rollCallMsg += placeStr + s.name + ': ' + rankStr + ' ' + roleStr + '\n'

		return rollCallMsg

	def setOption(self, option, optValue = 15):
		option = option.upper()
		dType = self.dType

		if option == 'MANUAL':
			dType = 'MANUAL'
		elif option == 'MATCHMADE':
			dType = 'MATCHMADE'
		elif option == 'RANDOM':
			dType = 'RANDOM'
		elif option == 'RLANES':
			self.rLanes = True
		elif option == 'RCHAMPS':
			self.rChamps = True
			self.rChampsNum = optValue
		else:
			print(option + ' is not a valid draft option.')

	def start(self):
		dType = self.dType

		if dType == 'MANUAL':
			self.manualDraft()
		elif dType == 'MATCHMADE':
			self.matchmadeDraft()
		elif dType == 'RANDOM':
			self.randomDraft()

	def __str__(self):
		return self.id

############################################################################################################
##																										  ##
##												DRAFT OBJECT											  ##
##																										  ##
############################################################################################################

class Draft:
	
	def __init__(self, game):
		self.Game = game

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

	def matchmadeDraft(self):
		game = self.Game
		activeSummoners = game.activeSummoners
		activeTeams = game.activeTeams
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

		# newTeamA = g.Team(bestTeamA, 0, 0, [])
		# newTeamB = g.Team(bestTeamB, 0, 0, [])
		# activeTeams.append(newTeamA)
		# activeTeams.append(newTeamB)

		msgTeamA = 'Team A is:\n\n'
		i = 0
		for summoner in bestTeamA:
			i+=1
			msgTeamA += str(i) + '. ' + summoner.name + '\n'

		if game.rChamps:
			msgTeamA += 'The champion pool for Team A is: ' + '\n' + randomChamps(rChamps)
		print(msgTeamA)

		msgTeamB = 'Team B is:\n\n'
		i = 0
		for summoner in bestTeamB:
			i+=1
			msgTeamB += str(i) + '. ' + summoner.name + '\n'

		if game.rChamps:
			msgTeamB += 'The champion pool for Team B is: ' + '\n' + randomChamps(rChamps)
		print(msgTeamB)

		responseMsg = msgTeamA + '\n\n\n' + msgTeamB
		print(responseMsg)
		return responseMsg

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