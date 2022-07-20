

class StatsPirate(object):
	'''
	def __init__(self, level, qualite, fruitpower):
		array=StatsPirate.generateStats(level, qualite, fruitpower)
		self._vie= array[0]
		self._atk= array[1]
		self._dfs= array[2]
		self._ftg= array[3]


	@property
	def vie(self):
		return self._vie


	@property
	def atk(self):
		return self._atk


	@property
	def dfs(self):
		return self._dfs


	@property
	def ftg(self):
		return self._ftg



	@vie.property
	def vie(self, am):
		self._vie=am


	@atk.property
	def atk(self, am):
		self._atk=am


	@dfs.property
	def dfs(self, am):
		self._dfs=am


	@ftg.property
	def ftg(self, am):
		self._ftg=am
	'''

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

	def __str__(self):
		return str(self._amount)


class Vie(Stat):
	pass

class Atk(Stat):
	pass

class Def(Stat):
	pass

class Ftg(Stat):
	pass