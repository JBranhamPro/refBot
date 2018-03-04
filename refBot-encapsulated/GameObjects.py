import requests
import json
import uuid
from itertools import combinations
from random import randint
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
		else:
			print(summonerData)
			return 'A summoner with the name, {}, could not be found.'.format(str(summonerName))


	def getRank(self, summonerId):		
		rankInfoUrl = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/{}?api_key={}'.format(str(summonerId), apiKey)
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
		summonerUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/{}?api_key={}'.format(str(summonerId), apiKey)
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
				return 'Catch you later, {}!'.format(summoner.name)

	def rollCall(self):
		rollCallMsg = ''
		i = 0
		for summoner in self.activeSummoners:
			i+=1
			s = summoner
			msgToAdd = '{place}. {name} : ( {primary} / {secondary} ) {tier} {rank}\n'.format(place=i, name=s.name, primary=s.primary, secondary=s.secondary, tier=s.tier, rank=s.rank)

			print(msgToAdd)

			rollCallMsg += msgToAdd

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
			# self.draft.manual()
			return True

		elif dType == 'MATCHMADE':
			teams = self.draft.matchmade(self.activeSummoners)

			i = 0
			for team in self.activeTeams:
				for summoner in teams[i]:
					team.add(summoner)
				i+=1

			return True

		elif dType == 'RANDOM':
			draftMsg = self.draft.random(activeSummoners)

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

	def random(self, summoners):
		summoners = [summoners]
		top = []
		jng = []
		mid = []
		adc = []
		sup = []
		roles = {'TOP':top, 'JNG':jng, 'MID':mid, 'ADC':adc, 'SUP':sup}

		def roleDraft(role, pool):
			primaries = []
			secondaries = []
			primFills = []
			secFills = []
			
			for summoner in summoners:
				if summoner.primary == role:
					primaries.append(summoner)
				elif summoner.secondary == role:
					secondaries.append(summoner)
				elif summoner.primary == 'FILL':
					primFills.append(summoner)
				elif summoner.secondary == 'FILL':
					secFills.append(summoner)
			
			while len(pool) < 2:
				def pullFrom(category):
					end = len(category) - 1
					randomIndex = randint(0, end)
					summoner = category[randIndex]
					pool.append(summoner)
					category.remove(summoner)
					summoners.remove(summoner)

				if len(primaries) > 1:
					pullFrom(primaries)
				elif len(secondaries) > 1:
					pullFrom(secondaries)
				elif len(primFills) > 1:
					pullFrom(primFills)
				elif len(secFills) > 1:
					pullFrom(secFills)
				else:
					return 'There are not enough summoners who have selected {} or FILL to place in this role.'.format(role)

		def buildTeam(teamPos, index):
			team = Team(teamPos)
			team.top = top[randint(0,1)]
			team.jng = jng[randint(0,1)]
			team.mid = mid[randint(0,1)]
			team.adc = adc[randint(0,1)]
			team.sup = sup[randint(0,1)]
			teammates = [team.top, team.jng, team.mid, team.adc, team.sup]

			for teammate in teammates:
				team.add(teammate)

		for role, pool in roles.items():
			roleDraft(role, pool)

		teamA = buildTeam('A')
		teamB = buildTeam('B')
		return teamA, teamB

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
		self.captain = None
		self.summoners = {}
		self.top = 'open'
		self.jng = 'open'
		self.mid = 'open'
		self.adc = 'open'
		self.sup = 'open'

	def add(self, summoner, role=None):
		self.summoners[summoner.id] = summoner
		if role:
			role = role.upper()
			if role == 'TOP':
				self.top = summoner
				return True
			elif role == 'JNG':
				self.jng = summoner
				return True
			elif role == 'MID':
				self.mid = summoner
				return True
			elif role == 'ADC':
				self.adc = summoner
				return True
			elif role == 'SUP':
				self.sup = summoner
				return True
			else:
				return False, 'invalid role'
		else:
			return True

	def getPlayers(self):
		players = {}
		players['TOP'] = self.top
		players['JNG'] = self.jng
		players['MID'] = self.mid
		players['ADC'] = self.adc
		players['SUP'] = self.sup
		return players