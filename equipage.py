
import random
from utils import Utils
from pirate import Pirate
from message import Message

class Equipage(object):



	def __init__(self, pirates):
		self._team=pirates
		self._turn=Turn(pirates)
		self._availableToFight=True
		self._dead=[]

	@property
	def team(self):
		return self._team

	@property
	def availableToFight(self):
		self._turn=Turn(self._team)
		for pirate in self._team:
			if pirate.mort==False:
				return True
		return False

	@property
	def numberOfPirates(self):
		return len(self._team)

	@property
	def dead(self):
		return self._dead

	def cleanUpDeadArray(self):
		self._dead=[]

	def attaquant(self):
		pirate=self._turn.next()
		if pirate==None:
			return None
		return pirate

	def isAttacked(self, attaquant):
		defenseur=self.defenseur()
		if defenseur==None:
			return Message("Cet équipage n'a plus personne de vivant. Fin du combat.", True, True)
		return defenseur.isAttacked(attaquant)


	def defenseur(self):
		self.updateStatus() 
		if len(self._team)<=0:
			return None
		elif len(self._team)==1:
			return self._team[0]
		who=random.randint(0, len(self._team)-1)
		count=0
		for i in range(len(self._team)):
			if self._team[i].mort==False:
				if who==count:
					return self._team[i]
				count+=1

	


	def isinstance(self):
		return "Equipage"

	def updateStatus(self):
		for count in range(len(self._team)-1,-1,-1):
			if self._team[count].mort:
				self._dead.append(self._team[count])
				self._team.pop(count)
		self._turn.removePirate()
		if len(self._team)==0:
			self._availableToFight=False



	def removeFighter(self):
		self._turn.removeCurrent()

	def newFighter(self, pirate):
		self._team.append(pirate)
		self._turn.add(pirate)

	def asMessageArray(self):
		array=[]
		for pirate in self._team:
			array.extend(pirate.asMessageArray())
		return array


	@staticmethod
	def generateEnnemies(level, ennemies, gameid):
		pirates=[]
		for _ in range(ennemies):
			pirates.append(Pirate(gameid, level, False, None, True))
		return Equipage(pirates)

class Turn(object):

	def __init__(self, pirates):
		self._pirates=Utils.shuffle(pirates)
		self._turnCount=0


	def add(self, pirate):
		place=random.randint(0,len(self._pirates)+1)
		self._pirates.insert(place,pirate)

	def removeCurrent(self):
		self._pirates.pop(self._turnCount)


	def removePirate(self):
		if len(self._pirates)==0:
			return None
		for count in range(len(self._pirates)-1,-1,-1):
			if self._pirates[count].mort:
				self._pirates.pop(count)


	def next(self):
		if len(self._pirates)==0:
			return None
		self.increaseTurnCount()
		pirate = self._pirates[self._turnCount]
		while pirate.mort:
			self.removeCurrent()
			if len(self._pirates)==0:
				return None
			self.increaseTurnCount()
			pirate = self._pirates[self._turnCount]

		return pirate


	def increaseTurnCount(self):
		self._turnCount+=1
		if self._turnCount>=len(self._pirates):
			self._turnCount=0


































