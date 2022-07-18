
import random

from interactBDD import InteractBDD

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
	

class FruitFactoryMeta(type):

	_instances = {}

	def __call__(cls, *args, **kwargs):
		"""
		Possible changes to the value of the `__init__` argument do not affect
		the returned instance.
		"""
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]



class FruitFactory(metaclass=FruitFactoryMeta):

	@staticmethod
	def allocateFruit(percentages):
		fruitBool=random.randint(0,100)<=percentages[0]
		if fruitBool:
			availableFruits=InteractBDD.countAvailableFruits()
			if availableFruits==0:
				return FruitDemon("None",[0,0,0,0])

			fruitsNumber=random.randint(0,availableFruits-1)
			fruitsName=InteractBDD.notAllocatedFruits()[fruitsNumber]
			InteractBDD.allocateFruit(fruitsName)
			string=InteractBDD.fruitsPower(fruitsName) #1,2,3,4
			array=string.split(",")
			return FruitDemon(fruitsName,array)
					
		return FruitDemon("None",[0,0,0,0])


	@staticmethod
	def giveThatFruit(fruitsName):
		if fruitsName=="None":
			return FruitDemon("None",[0,0,0,0])
		InteractBDD.allocateFruit(fruitsName)
		string=InteractBDD.fruitsPower(fruitsName) #1,2,3,4
		array=string.split(",")
		return FruitDemon(fruitsName, array)

	@staticmethod
	def giveAFruit():
		availableFruits=InteractBDD.countAvailableFruits()
		if availableFruits==0:
			return FruitDemon("None",[0,0,0,0])
		fruitsNumber=random.randint(0,availableFruits-1)
		fruitsName=InteractBDD.notAllocatedFruits()[fruitsNumber]
		InteractBDD.allocateFruit(fruitsName)
		string=InteractBDD.fruitsPower(fruitsName) #1,2,3,4
		array=string.split(",")
		return FruitDemon(fruitsName,array)


























