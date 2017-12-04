import sqlite3
import Globals
g = Globals

connSum = sqlite3.connect('Summoner.db')

curSum = connSum.cursor()

def setupSummonerDb():
	curSum.execute("""CREATE TABLE summoners (
					name text,
					tier text,
					rank text,
					value real
					)""")

	connSum.commit()

def uploadSummoner(name, tier, rank, value):
	curSum.execute("INSERT INTO summoners VALUES (:name, :tier, :rank, :value)", {"name":name, "tier":tier, "rank":rank, "value":value})
	connSum.commit()

def getSummoner(summonerName):
	curSum.execute("SELECT * FROM summoners WHERE name=:summonerName", {"summonerName" : summonerName})
	records = curSum.fetchall()
	print('DbCalls records:', records)
	try:
		summoner = records[0]
		print(summoner)
	except:
		return False

	name = summoner[0]
	tier = summoner[1]
	rank = summoner[2]
	value = summoner[3]
	
	return g.Summoner(name, tier, rank, value)