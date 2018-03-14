import sqlite3
import requests
import json
import Secrets as s
apiKey = s.apiKey

conn = sqlite3.connect('LittleLeague.db')

c = conn.cursor()

def checkForGame(gameId):
	c.execute("SELECT * FROM games WHERE id=:gameId", {"gameId" : gameId})
	records = c.fetchall()

	try:
		gameData = records[0]
	
		return gameData
	except:
		return None

def checkForSummoner(summonerId):
	summonerData = getSummonerData(summonerId)

	if summonerData is None:
		return None
	else:
		print(summonerData)
		return summonerData

def createGameName(gameId):
	existingGame = checkForGame(gameId)

	if existingGame:
		return 'Fail'
	else:
		games = getGames()
		if games:
			latestGameIndex = len(games) - 1
			latestGame = games[latestGameIndex]
			latestGameName = latestGame[1]
			newName = int(latestGameName) + 1
			newName = str(newName)
			print(newName)
			return newName
		else:
			name = '000001'
			print(int(name))
			return name

def getGames():
	c.execute("SELECT * FROM games")
	games = c.fetchall()
	return games

def getSummonerData(summonerId):

	c.execute("SELECT * FROM summoners WHERE id=:summonerId", {"summonerId" : summonerId})
	records = c.fetchall()

	try:
		summonerData = records[0]
	
		return summonerData
	except:
		return None

def saveGame(game):
	existingGame = checkForGame(game.id)

	if existingGame:
		c.execute("""UPDATE
					games
					SET
					teamA = :teamA,
					teamB = :teamB,
					draftType = :type,
					randomChamps = :rChamps,
					randomLanes = :rLanes
					WHERE
					id = :id""", 
					{'teamA':game.activeTeams[0], 'teamB':game.activeTeams[1], 'type':game.draft.type, 
					'randomChamps':game.draft.rChamps, 'randomLanes':game.draft.rLanes,'id':game.id})
	
		conn.commit()

		return True
	else:
		c.execute("INSERT INTO games VALUES (:id, :name, :teamA, :teamB, :draftType, :randomChamps, :randomLanes)",
		{'id':game.id, 'name':game.name, 'teamA':game.activeTeams[0].id, 'teamB':game.activeTeams[1].id,
		'draftType':game.draft.type, 'randomChamps':game.draft.rChamps, 'randomLanes':game.draft.rLanes})

		conn.commit()

		return False

def setupDb():
	c.execute("""CREATE TABLE summoners (
					id int,
					name text,
					tier text,
					rank text,
					value real,
					primaryRole text,
					secondaryRole text
					)""")

	c.execute("""CREATE TABLE games (
					id text,
					name text,
					teamA text,
					teamB text,
					draftType text,
					randomChamps int,
					randomLanes boolean
					)""")

	c.execute("""CREATE TABLE teams (
					id text,
					name text,
					wins int,
					losses int,

					topId int,
					topTier text,
					topRank text,
					
					jngId int,
					jngTier text,
					jngRank text,
					
					midId int,
					midTier text,
					midRank text,
					
					adcId int,
					adcTier text,
					adcRank text,
					
					supId int,
					supTier text,
					supRank text
					)""")

	c.execute("""CREATE TABLE members (
					id int,
					summonerId int
					)""")

	conn.commit()
	print('DbCalls --> setupDb : database has been established')

def updateSummoner(summoner):
	summonerData = getSummonerData(summoner.id)

	if summonerData:
		with conn:
			if summonerData[1] != summoner.name:
				c.execute("""UPDATE summoners SET name = :name WHERE id = :id""", 
					{'name': summoner.name, 'id': summoner.id})
			
			if summonerData[2] != summoner.tier:
				c.execute("""UPDATE summoners SET tier = :tier WHERE id = :id""", 
					{'tier': summoner.tier, 'id': summoner.id})
			
			if summonerData[3] != summoner.rank:
				c.execute("""UPDATE summoners SET rank = :rank WHERE id = :id""", 
					{'rank': summoner.rank, 'id': summoner.id})
			
			if summonerData[4] != summoner.value:
				c.execute("""UPDATE summoners SET value = :value WHERE id = :id""", 
					{'value': summoner.value, 'id': summoner.id})
			
	else:
		print('DbCalls --> updateSummoner : No summoner data available for ' + summoner.name)

def updateSummonerRoles(summonerId, primary, secondary):
	with conn:
		c.execute("""UPDATE summoners SET primaryRole = :primary WHERE id = :id""", 
			{'primary': primary, 'id': summonerId})

		c.execute("""UPDATE summoners SET secondaryRole = :secondary WHERE id = :id""", 
			{'secondary': secondary, 'id': summonerId})

def uploadMember(memberId, summonerId):
	existingMemberData = checkForMember(memberId)

	if existingMemberData:
		updateMemberData(memberId)
	else:
		with conn:
			c.execute("INSERT INTO members VALUES (:id, :summonerId)", {"id" : memberId, "summonerId" : summonerId}

def uploadSummoner(summoner):
	existingSummonerData = checkForSummoner(summoner.id)
	s = summoner

	if existingSummonerData is None:
		with conn:
			c.execute("INSERT INTO summoners VALUES (:id, :name, :tier, :rank, :value, :primaryRole, :secondaryRole)", 
				{"id":summoner.id, "name":summoner.name, "tier":summoner.tier, "rank":summoner.rank, "value":summoner.value, "primaryRole":summoner.primary, "secondaryRole":summoner.secondary})

		return summoner.name + ' has been added to the LittleLeague database.'

	elif existingSummonerData:
		updateSummoner(summoner)
		return summoner.name + ' was already in the LittleLeague database. Their information has been updated.'
	
	else:
		return 'DbCalls --> uploadSummoner : Summoner neither updated nor uploaded'