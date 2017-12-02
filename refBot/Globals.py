class DraftOptions:

	def __init__(self, dType, rChamps, rLanes):
		self.dType = dType
		self.rChamps = rChamps
		self.rlanes = rLanes

class Summoner:

	def __init__(self, name, tier, rank, value):
		self.name = name
		self.tier = tier
		self.rank = rank
		self.value = value

# class Team:

# 	def __init__(self, p1, p2, p3, p4, p5):
# 		self.p1 = 'player one'
# 		self.p2 = 'player two'
# 		self.p3 = 'player three'
# 		self.p4 = 'player four'
# 		self.p5 = 'player five'

Team = []

activePlayers = {}

draft = DraftOptions(False, False, False)
