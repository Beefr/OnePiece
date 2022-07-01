
from message import Message

from equipage import Equipage




class Island(object):


	def __init__(self, name, level, ennemies):
		self._name=name
		self._level=level
		self._ennemies=ennemies
		self._pirates=Equipage.generateEnnemies(level, ennemies)



	def __str__(self):
		return Message(self._name+", il y a "+str(self._pirates.numberOfPirates)+" pirates de niveau "+str(self._level))



	@property
	def name(self):
		return self._name



	@property
	def level(self):
		return self._level



	@property
	def pirates(self):
		return self._pirates


	@pirates.setter
	def pirates(self, joueur):
		self._pirates=joueur


	def regenerate(self):
		self._pirates=Equipage.generateEnnemies(self._level, self._ennemies)