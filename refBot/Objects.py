class DraftOptions:

	def __init__(self, auto, matchmade, rChamps, rLanes):
		self.auto = auto
		self.matchmade = matchmade
		self.rChamps = rChamps
		self.rlanes = rLanes

class Summoner:

	def __init__(self, name, tier, rank, value):
		self.name = name
		self.tier = tier
		self.rank = rank
		self.value = value

activePlayers = {}