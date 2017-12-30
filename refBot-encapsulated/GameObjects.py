import requests
import json
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
		else:
			print(summonerData)
			return 'A summoner with the name, ' + str(summonerName) + ', could not be found.'

	def getId(self, summonerName=self.name):
		summonerDetails = self.getSummonerDetails(summonerName)
		return summonerDetails["id"]

	def getRank(self, summonerName=self.name):
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

		summonerValue += rankInfo["leaguePoints"] * .0001
		return summonerValue

	def getSummonerData(self, summonerName=self.name):
		summonerDetails = self.getSummonerDetails(summonerName)
		summonerRank = self.getRank(summonerName)
		summonerData = {"details": summonerDetails, "rank": summonerRank}
		return summonerData

	def getSummonerDetails(self, summonerName=self.name):
		summonerUrl = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summonerName + '?api_key=' + apiKey
		summonerApiRequest = requests.get(summonerUrl)
		summonerDetails = summonerApiRequest.json()
		return summonerDetails

	def setRoles(self, primary, *secondary):
		primary = primary.upper()

		def errorReport(userInput):
			return str(userInput) + ' is not a valid option. Please select one of the following: TOP, JNG, MID, ADC, SUP'

		def changeRole(choice, role)
			if choice == 'TOP':
				role = choice
			elif choice == 'JNG':
				role = choice
			elif choice == 'MID':
				role = choice
			elif choice == 'ADC':
				role = choice
			elif choice == 'SUP':
				role = choice
			else:
				return errorReport(choice)

		changeRole(primary, self.primary)

		if secondary:
			secondary = secondary.upper()
			changeRole(secondary, self.secondary)

	def __str__(self):
		return self.name

############################################################################################################
##																										  ##
##												GAME OBJECT												  ##
##																										  ##
############################################################################################################

class Game:
	from Draft import draft

	def __init__(self):
		self.startTime = None
		self.activeSummoners = []
		self.activeTeams = []
		self.draft = draft(self)
		self.type = 'MANUAL'
		self.rChamps = 0
		self.rlanes = False

	# def addActiveSummoner(self, summoner):
	# 	activeSummoners = self.activeSummoners

	# 	print('Methods, Summoner is: ', summoner)

	# 	if summoner:
	# 		activeSummoners.append(summoner)
	# 		return summoner.name + ' has joined the active players group.'
	# 	elif summoner is None:
	# 		onAddCmd(summonerName)
	# 		addedSummoner = d.getSummoner(summonerName)
	# 		activeSummoners.append(addedSummoner)
	# 		return addedSummoner.name + ' was not found in the LittleLeague Summoner database. They have been added and are now an active player.'
	# 	else:
	# 		print('Mistakes were truly made: ', summoner)

	def rmActiveSummoner(self, summoner):
		activeSummoners = self.activeSummoners

		if activeSummoners.count(summoner) > 0:
			self.activeSummoners.remove(summoner)
			return 'Catch you later, ' + summoner.name + '!'
		else:
			return summoner.name + ' is not currently an active player.'

	def rollCall(self):
		rollCallMsg = ''
		i = 0
		for summoner in self.activeSummoners:
			i+=1
			rollCallMsg += str(i) + '. ' + summoner.name + '\n'

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