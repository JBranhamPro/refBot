import requests
import json
import Secrets
s = Secrets
apiKey = s.apiKey

class Draft:
	
	def __init__(self, game):
		
		self.game = game

	game = self.game

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

	def matchmadeDraft(self, game):
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