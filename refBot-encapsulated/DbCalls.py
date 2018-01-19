import sqlite3
import requests
import json
import Secrets as s
apiKey = s.apiKey

# conn = sqlite3.connect('LittleLeague.db')
conn = sqlite3.connect(':memory:')

c = conn.cursor()

def checkForSummoner(summonerId):
	summonerData = getSummonerData(summonerId)
	print('DbCalls --> checkForSummoner : ', summonerData)

	if summonerData is None:
		return None
	else:
		print(summonerData)
		return summonerData

def getSummonerData(summonerId):

	c.execute("SELECT * FROM summoners WHERE id=:summonerId", {"summonerId" : summonerId})
	records = c.fetchall()
	print('DbCalls --> getSummonerData : ', records)

	try:
		summonerData = records[0]
	
		return summonerData
	except:
		return None

def setupDb():
	c.execute("""CREATE TABLE summoners (
					id int,
					name text,
					tier text,
					rank text,
					value real,
					primaryRole text,
					secondaryRole text,
					gameId text
					)""")

	c.execute("""CREATE TABLE teams (
					gameId text,
					teamId text,
					teamName text,
					teamValue real,

					topId int,
					topName text,
					topTier text,
					topRank text,
					topValue real,
					
					jngId int,
					jngName text,
					jngTier text,
					jngRank text,
					jngValue real,
					
					midId int,
					midName text,
					midTier text,
					midRank text,
					midValue real,
					
					adcId int,
					adcName text,
					adcTier text,
					adcRank text,
					adcValue real,
					
					supId int,
					supName text,
					supTier text,
					supRank text,
					supValue real
					)""")

	conn.commit()
	print('DbCalls --> setupDb : database has been established')

def updateSummoner(summoner):
	summonerData = getSummonerData(summoner.id)

	if summonerData:
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

		if summonerData[7] != summoner.gameId:
			c.execute("""UPDATE summoners SET gameId =:gameId WHERE id = :id""",
				{'gameId': summoner.gameId, 'id': summoner.id})

		print('d.updateSummoner -->', summoner)
	else:
		print('DbCalls --> updateSummoner : No summoner data available for ' + summoner.name)

def updateSummonerRoles(summonerId, primary, secondary):
	c.execute("""UPDATE summoners SET primaryRole = :primary WHERE id = :id""", 
		{'primary': primary, 'id': summonerId})

	c.execute("""UPDATE summoners SET secondaryRole = :secondary WHERE id = :id""", 
		{'secondary': secondary, 'id': summonerId})

def uploadSummoner(summoner):
	existingSummonerData = checkForSummoner(summoner.id)
	s = summoner

	if existingSummonerData is None:
		with conn:
			c.execute("INSERT INTO summoners VALUES (:id, :name, :tier, :rank, :value, :primaryRole, :secondaryRole, :gameId)", 
				{"id":summoner.id, "name":summoner.name, "tier":summoner.tier, "rank":summoner.rank, "value":summoner.value, "primaryRole":summoner.primary, "secondaryRole":summoner.secondary, "gameId":summoner.gameId})

		print('d.uploadSummoner --> added record values:', (s.id, s.name, s.tier, s.rank, s.value, s.primary, s.secondary))
		return summoner.name + ' has been added to the LittleLeague database.'

	elif existingSummonerData:
		updateSummoner(summoner)
		return summoner.name + ' was already in the LittleLeague database. Their information has been updated.'
	
	else:
		return 'DbCalls --> uploadSummoner : something went terribly wrong'