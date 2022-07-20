
import random
from utils import Utils
from pirate import Pirate


class Equipage(object):



	def __init__(self, pirates):
		self._team=pirates
		self._turn=Turn(pirates)
		self._availableToFight=True
		self._numberOfPirates=len(self._team)
		self._dead=[]

	@property
	def team(self):
		return self._team

	@property
	def availableToFight(self):
		self.updateTurn()
		for pirate in self._team:
			if pirate.mort==False and pirate.availableToFight:
				return True
		return False

	@property
	def numberOfPirates(self):
		self._numberOfPirates=len(self._team)
		return self._numberOfPirates


	@property
	def dead(self):
		return self._dead


	def updateTurn(self):
		self._turn=Turn(self._team)

	def cleanUpDeadArray(self):
		self._dead=[]

	def attaquant(self):
		pirate=self._turn.next()
		if pirate==None:
			return None
		pirate.increaseFatigue()
		return pirate

	def isAttacked(self, attaquant):
		self.countAvailableToTank()
		who=random.randint(0, self._numberOfPirates-1)
		count=0
		for i in range(len(self._team)):
			if self._team[i].mort==False:
				if who==count:
					return self._team[i].isAttacked(attaquant)
				count+=1

	
	def countAvailableToTank(self):
		count=0
		for pirate in self._team:
			if pirate.mort==False:
				count+=1
		self._numberOfPirates=count
		if self._numberOfPirates==0:
			self._availableToFight=False


	def isinstance(self):
		return "Equipage"

	def updateStatus(self):
		temp=[]
		for pirate in self._team:
			if pirate.updateStatus():
				self._dead.append(pirate)
				self._turn.removePirate()
			else:
				temp.append(pirate)
		self._team=temp
		self._numberOfPirates=len(self._team)
		if self._numberOfPirates==0:
			self._availableToFight=False

	def regenerateHealth(self):
		for pirate in self._team:
			pirate.regenerateHealth(pirate.level, pirate.qualite)


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
	def generateEnnemies(level, ennemies):
		pirates=[]
		for i in range(ennemies):
			pirates.append(Pirate(level))
		return Equipage(pirates)

class Turn(object):

	def __init__(self, pirates):
		self._pirates=Utils.shuffle(pirates)
		self._turnCount=0
		self._numberOfPirates=len(self._pirates)


	def add(self, pirate):
		self._numberOfPirates+=1
		place=random.randint(0,self._numberOfPirates)
		if place==0:
			temp=[pirate]

			for p in self._pirates:
				temp.append(p)

			self._pirates=temp
		elif place==self._numberOfPirates:
			self._pirates.append(pirate)
		else:
			temp=[]
			for p in self._pirates[0:place]:
				temp.append(p)
			
			temp.append(pirate)
			
			for p in self._pirates[place+1:len(self._pirates)-1]:
				temp.append(p)

			self._pirates=temp

	def removeCurrent(self):
		self._numberOfPirates-=1
		self._pirates=Utils.removeElement(self._pirates, self._turnCount)


	def removePirate(self):
		temp=[]
		for pirate in self._pirates:
			if pirate.mort==False:
				temp.append(pirate)
		self._pirates=temp
		self._numberOfPirates=len(self._pirates)


	def next(self):
		if len(self._pirates)==0:
			return None
		self.increaseTurnCount()
		pirate = self._pirates[self._turnCount]
		while pirate.availableToFight==False or pirate.mort:
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


































