

class StatsPirate(object):



	@staticmethod
	def generateStats(level, qualite, fruitpower):
		level=int(level)
		qualite=int(qualite)
		fruitpower=list(map(int, fruitpower )) # ['1','2','3','4'] -> [1,2,3,4]

		vie=100*level*(5-qualite)
		degats=20*level*(5-qualite)
		defense=10*level*(5-qualite)
		fatigue=100*(5-qualite)
		return [vie*(100+fruitpower[0])/100, degats*(100+fruitpower[1])/100, defense*(100+fruitpower[2])/100, fatigue*(100+fruitpower[3])/100]

