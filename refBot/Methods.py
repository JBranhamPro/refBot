import APICalls
a = APICalls
import DbCalls
d = DbCalls
import Globals
g = Globals
from itertools import combinations

def draft(draftType):
	g.draft.dType = draftType
	dType = g.draft.dType

	if dType == 'MANUAL':
		manualDraft()
	elif dType == 'MATCHMADE':
		matchmadeDraft()
	elif dType == 'RANDOM':
		randomDraft()

def matchmadeDraft():
	bestTeamA = []
	bestTeamB = []
	prevValDiff = 100
	newValDiff = 0
	playerList = len(g.activePlayers)
	teamSize = int(playerList/2)

	for team in combinations(g.activePlayers, teamSize):
		players = g.activePlayers.copy()
		teamA = []
		teamB = []
		valueA = 0
		valueB = 0

		for player in team:
			summonerValue = player.value
			valueA += summonerValue
			teamA.append(player)
			players.remove(player)

		for player in players:
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

	newTeamA = g.Team(bestTeamA, 0, 0, [])
	newTeamB = g.Team(bestTeamB, 0, 0, [])
	g.activeTeams.append(newTeamA)
	g.activeTeams.append(newTeamB)

	msgTeamA = 'Team A is:\n\n'
	i = 0
	for summoner in bestTeamA:
		i+=1
		msgTeamA += str(i) + '. ' + summoner.name + '\n'
	print(msgTeamA)

	msgTeamB = 'Team B is:\n\n'
	i = 0
	for summoner in bestTeamB:
		i+=1
		msgTeamB += str(i) + '. ' + summoner.name + '\n'
	print(msgTeamB)

	responseMsg = msgTeamA + '\n\n\n' + msgTeamB
	print(responseMsg)
	return responseMsg

def onAddCmd(summonerName):
	summonerData = a.getSummonerData(summonerName)
	summonerDetails = summonerData["details"]
	rankInfo = summonerData["rank"]

	name = summonerDetails["name"]
	tier = rankInfo["tier"]
	rank = rankInfo["rank"]
	value = placeSummoner(rankInfo)

	if d.getSummoner(summonerName) is None:
		response = d.uploadSummoner(name, tier, rank, value)
		return response

def onAyeCmd(summonerName):
	if summonerName.upper() == 'ALL':
		testAye()
		return 'ALL command complete'

	summoner = d.getSummoner(summonerName)
	print('Methods, Summoner is: ', summoner)
	if summoner != None:
		g.activePlayers.append(summoner)
		return summoner.name + ' has joined the active players group.'
	elif summoner is None:
		onAddCmd(summonerName)
		addedSummoner = d.getSummoner(summonerName)
		g.activePlayers.append(summoner)
		return addedSummoner.name + ' was not found in the LittleLeague Summoner database. They have been added and are now an active player.'
	else:
		print('Mistakes were truly made: ', summoner)

def onByeCmd(summonerName):
	if activePlayers.count(summonerName) > 0:
		del g.activePlayers[summonerName]
		return 'Catch you later, ' + summonerName + '!'
	else:
		return 'Sorry, but ' + summonerName + ' is not an active player.'

def onGetCmd(summonerName):
	summoner = d.getSummoner(summonerName)
	
	name = summoner.name
	tier = summoner.tier
	rank = summoner.rank
	value = summoner.value

	responseMsg = name + ': ' + tier + ' ' + rank + ' (' + str(value) + ')'
	return responseMsg

def onRollCallCmd():
	rollCallMsg = ''
	i = 0
	for summoner in g.activePlayers:
		i+=1
		rollCallMsg += str(i) + '. ' + summoner.name + '\n'

	return rollCallMsg

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

def randomLanes():	
	roles = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
	playersDrafted = 0

	while len(roles) > 0:
		draftedRole = randint(0,len(roles) - 1)
		roleOrder.append(roles[draftedRole])
		del roles[draftedRole]

def setDraftOptions(option, value):
	g.draft.option = value

def testAye():
	testSet = ['The Real N3lo', 'Zaraedaria', 'bobmicbiong', 'llamamalicious', 'Alkiiron', 'Broken Leg Fish', 'TheUnsungHeroPt2', 'semland258', 'Gundâm','Zazul']
	for summoner in testSet:
		onAyeCmd(summoner)	