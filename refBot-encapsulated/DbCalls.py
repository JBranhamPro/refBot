import sqlite3
import requests
import json
import Secrets as s
apiKey = s.apiKey

conn = sqlite3.connect('LittleLeague.db')
#conn = sqlite3.connect(':memory:')

c = conn.cursor()

def checkForSummoner(summonerId):
	summonerData = getSummonerData(summonerId)
	print('d.checkForSummoner', summoner)

	if summoner is None:
		return None
	else:
		print(summoner)
		return summonerData

def getSummonerData(summonerId):

	c.execute("SELECT * FROM summoners WHERE id=:summonerId", {"summonerId" : summonerId})
	records = c.fetchall()
	print('d.getSummoner :: DbCalls records:', records)

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
					primary text,
					secondary text
					)""")

	c.execute("""CREATE TABLE teams (
					teamId int,
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

def updateSummoner(summoner):
	summonerData = getSummonerData(summoner.name)
	
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

	if summonerData[5] != summoner.primary:
		c.execute("""UPDATE summoners SET primary = :primary WHERE id = :id""", 
			{'primary': summoner.primary, 'id': summoner.id})

	if summonerData[6] != summoner.secondary:
		c.execute("""UPDATE summoners SET secondary = :secondary WHERE id = :id""", 
			{'secondary': summoner.secondary, 'id': summoner.id})

	print('d.updateSummoner', summoner)

def uploadSummoner(summoner):
	existingSummoner = checkForSummoner(summoner.id)
	s = summoner

	if existingSummoner is None:
		with conn:
			c.execute("INSERT INTO summoners VALUES (:id, :name, :tier, :rank, :value, :primary, :secondary)", 
				{"id":summoner.id, "name":summoner.name, "tier":summoner.tier, "rank":summoner.rank, "value":summoner.value, "primary":summoner.primary, "secondary":summoner.secondary})

		print('d.uploadSummoner :: added record values:', (s.id, s.name, s.tier, s.rank, s.value, s.primary, s.secondary))
		return summoner.name + ' has been added to the LittleLeague database.'
	elif existingSummoner:
		updateSummoner(existingSummoner)
		return summoner.name + ' was already in the LittleLeague database. Their information has been updated.'
	else:
		return 'd.uploadSummoner :: something went terribly wrong'