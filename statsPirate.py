

class StatsPirate(object):

	@staticmethod
	def generateStats(level, qualite, fruitpower):
		level=int(level)
		qualite=int(qualite)

		vie=100*level*(5-qualite)
		degats=20*level*(5-qualite)
		defense=10*level*(5-qualite)
		fatigue=100*(5-qualite)
		return [vie*(100+fruitpower[0])/100, degats*(100+fruitpower[1])/100, defense*(100+fruitpower[2])/100, fatigue*(100+fruitpower[3])/100]

