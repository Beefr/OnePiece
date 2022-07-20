

class StatsPirate(object):



	@staticmethod
	def generateStats(level, qualite, fruitpower):
		level=int(level)
		qualite=int(qualite)

		vie=100*level*(5-qualite)
		degats=20*level*(5-qualite)
		defense=10*level*(5-qualite)
		fatigue=100*(5-qualite)
		return [Vie(vie*(100+fruitpower[0])/100), Atk(degats*(100+fruitpower[1])/100), Def(defense*(100+fruitpower[2])/100), Ftg(fatigue*(100+fruitpower[3])/100)]





class Stat(object):

	def __init__(self, amount):
		self._amount=amount

	
	@property
	def amount(self):
		return self._amount

	@amount.setter
	def amount(self, am):
		self._amount=am

	def __sub__(self, val):
		self._amount=self._amount-val

	def __hash__(self):
		return self._amount

	def __eq__(self, val):
		return self._amount==val

	def __cmp__(self, val):
		return self._amount-val


class Vie(Stat):
	pass

class Atk(Stat):
	pass

class Def(Stat):
	pass

class Ftg(Stat):
	pass