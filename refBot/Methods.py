import APICalls
a = APICalls
import DbCalls
d = DbCalls
import Globals
g = Globals
from itertools import permutations

def draft(draftType):
	g.draft.dType = draftType
	dType = g.draft.dType

	if dType == 'MANUAL':
		manualDraft()
	elif dType == 'MATCHMADE':
		matchmadeDraft()
	elif dType == 'RANDOM':
		randomDraft()

def getSummonerData(summonerName):
	summonerDetails = a.getSummonerDetails(summonerName)
	summonerRank = a.getRank(summonerName)
	summonerData = {"details": summonerDetails, "rank": summonerRank}
	return summonerData

def matchmadeDraft():
	teamA = []
	teamB = []
	valueA = 0
	valueB = 0
	prevValDiff = 100
	newValDiff = 0

	for permutation in permutations(g.activePlayers):
		valueA = 0
		valueB = 0

		i = 0
		while i < 10:
			summoner = permutation[i]
			summonerValue = summoner.value
			if i < 5:
				valueA += summonerValue
			else:
				valueB += summonerValue
			i += 1

		newValDiff = abs(valueA - valueB)
		if newValDiff < prevValDiff:
			prevValDiff = newValDiff

			i = 0
			for summoner in permutation:
				if i < 5:
					teamA.append(summoner)
				else:
					teamB.append(summoner)

	newTeamA = g.Team(teamA)
	newTeamB = g.Team(teamB)
	g.activeTeams.append(newTeamA, newTeamB)

	msgTeamA = 'Team A is:\n\n'
	i = 0
	for summoner in teamA:
		i+=1
		msgToAppend = str(i) + '. ' + summoner.name + '\n'
		teamA += msgToAppend

	msgTeamA = 'Team B is:\n\n'
	i = 0
	for summoner in teamB:
		i+=1
		msgToAppend = str(i) + '. ' + summoner.name + '\n'
		teamB += msgToAppend

def onAddCmd(summonerName):
	summonerData = getSummonerData(summonerName)
	summonerDetails = summonerData["details"]
	name = summonerDetails["name"]
	rankInfo = summonerData["rank"]
	tier = rankInfo["tier"]
	rank = rankInfo["rank"]
	value = placeSummoner(rankInfo)

	if d.getSummoner(summonerName) is None:
		d.uploadSummoner(name, tier, rank, value)

def onAyeCmd(summonerName):
	summoner = d.getSummoner(summonerName)
	print('Methods, Summoner is: ', summoner)
	if summoner != True:
		g.activePlayers.append(summoner)
		return summoner.name + ' has joined the active players group.'
	elif summoner == False:
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
		msgToAppend = str(i) + '. ' + summoner.name + '\n'
		rollCallMsg += msgToAppend

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