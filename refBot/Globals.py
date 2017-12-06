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

class Team:

	def __init__(self, summoners, wins, losses, champions):
		self.summoners = []
		self.wins = wins
		self.losses = losses
		self.champions = champions

activePlayers = []
activeTeams = []

draft = DraftOptions('MANUAL', False, False)