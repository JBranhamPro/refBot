import sqlite3
import Globals
g = Globals
import Methods
m = Methods
import APICalls
a = APICalls

conn = sqlite3.connect('LittleLeague.db')
#conn = sqlite3.connect(':memory:')

cur = conn.cursor()

def checkForSummoner(name, tier, rank, value):
	summoner = getSummoner(name)
	print('d.checkForSummoner', summoner)

	if summoner is None:
		return None
	else:
		updateSummoner(name, tier, rank, value)
		return True

def getSummoner(summonerName):
	actualName = a.getSummonerName(summonerName)

	cur.execute("SELECT * FROM summoners WHERE name=:summonerName", {"summonerName" : actualName})
	records = cur.fetchall()
	print('d.getSummoner :: DbCalls records:', records)

	try:
		summoner = records[0]

		name = summoner[0]
		tier = summoner[1]
		rank = summoner[2]
		value = summoner[3]
	
		return g.Summoner(name, tier, rank, value)
	except:
		return None

def insertTestData():
	testSummoners = ['The Real N3lo', 'Zaraedaria', 'bobmicbiong', 'llamamalicious', 'Alkiiron', 'Broken Leg Fish', 'TheUnsungHeroPt2', 'semland258', 'Gundâm','Zazul']
	for summoner in testSummoners:
		m.onAddCmd(summoner)

def setupDb():
	cur.execute("""CREATE TABLE summoners (
					name text,
					tier text,
					rank text,
					value real 
					)""")

	cur.execute("""CREATE TABLE teams (
					teamName text,
					teamValue real,

					topName text,
					topTier text,
					topRank text,
					topValue real,
					
					jngName text,
					jngTier text,
					jngRank text,
					jngValue real,
					
					midName text,
					midTier text,
					midRank text,
					midValue real,
					
					adcName text,
					adcTier text,
					adcRank text,
					adcValue real,
					
					supName text,
					supTier text,
					supRank text,
					supValue real
					)""")

	conn.commit()

def updateSummoner(name, tier, rank, value):
	summoner = getSummoner(name)
	if summoner.tier != tier:
		summoner.tier = tier
	if summoner.rank !=rank:
		summoner.rank = rank
	if summoner.value != value:
		summoner.value = value

	print('d.updateSummoner', summoner)

def uploadSummoner(name, tier, rank, value):
	existingSummoner = checkForSummoner(name, tier, rank, value)

	if existingSummoner is None:
		cur.execute("INSERT INTO summoners VALUES (:name, :tier, :rank, :value)", {"name":name, "tier":tier, "rank":rank, "value":value})
		conn.commit()
		print('d.uploadSummoner :: added record values:', (name, tier, rank, value))
		return name + ' has been added to the LittleLeague database.'
	elif existingSummoner:
		updateSummoner(name, tier, rank, value)
		return name + ' was already in the LittleLeague database. Their information has been updated.'
	else:
		return 'd.uploadSummoner :: something went terribly wrong'