
import random

from bdd import InteractBDD

class FruitDemon(object):

	def __init__(self, name, power):
		self._name=name
		self._power=power


	@property
	def power(self):
		return self._power


	@property
	def name(self):
		return self._name



	@power.setter
	def power(self, power):
		self._power=power


	@name.setter
	def name(self, name):
		self._name=name

	def __str__(self):
		return '{"type": "FruitDemon", "name": \"'+self._name+'\","power": '+str(self._power)+'}'
	


class FruitFactory(object):

	@staticmethod
	def allocateFruit(percentages, gameid):
		fruitBool=random.randint(0,100)<=percentages[0]
		if fruitBool:
			availableFruits=InteractBDD().countAvailableFruits(gameid)
			if availableFruits==0:
				return FruitDemon("None",[0,0,0,0])

			fruitsNumber=random.randint(0,availableFruits-1)
			fruitsName=InteractBDD().notAllocatedFruits(gameid)[fruitsNumber]
			InteractBDD().allocateFruit(fruitsName, gameid)
			power=InteractBDD().fruitsPower(fruitsName) 
			return FruitDemon(fruitsName,power)
					
		return FruitDemon("None",[0,0,0,0])


	@staticmethod
	def giveThatFruit(fruitsName, gameid, boss=False):
		if fruitsName=="None":
			return FruitDemon("None",[0,0,0,0])
		if not boss: 
			InteractBDD().allocateFruit(fruitsName, gameid) # TODO deallocate...?
		power=InteractBDD().fruitsPower(fruitsName) 
		return FruitDemon(fruitsName, power)

	@staticmethod
	def giveAFruit(gameid):
		availableFruits=InteractBDD().countAvailableFruits(gameid)
		if availableFruits==0:
			return FruitDemon("GumGum",[30,40,30,0])
		fruitsNumber=random.randint(0,availableFruits-1)
		fruitsName=InteractBDD().notAllocatedFruits(gameid)[fruitsNumber]
		InteractBDD().allocateFruit(fruitsName, gameid)
		power=InteractBDD().fruitsPower(fruitsName) 
		return FruitDemon(fruitsName,power)


























