
import random
import numpy as np
from utils import Utils
from pirate import Pirate

class Equipage(object):



	def __init__(self, pirates):
		self._team=pirates
		self._turn=Turn(pirates)
		self._availableToFight=True
		self._numberOfPirates=len(self._team)


	@property
	def team(self):
		return self._team

	@property
	def availableToFight(self):
		for pirate in self._team:
			if pirate.mort==False and pirate.availableToFight:
				return True
		return False

	@property
	def numberOfPirates(self):
		return self._numberOfPirates


	def attaque(self, equipage):
		pirate=self._turn.next()
		if pirate==None:
			return "Cet équipage n'a plus personne de vivant. Fin du combat."
		txt=equipage.whoIsGonnaTankThatHit().getAttackedBy(pirate)
		return txt

	def whoIsGonnaTankThatHit(self):
		alive=self.availableToTank()
		who=random.randint(0, self._numberOfPirates-1)
		return alive[who]
	
	def availableToTank(self):
		alive=[]
		for pirate in self._team:
			if pirate.mort==False:
				alive.append(pirate)
		self._numberOfPirates=len(alive)
		if self._numberOfPirates==0:
			self._availableToFight=False
		return alive



	def updateStatus(self):
		temp=[]
		for pirate in self._team:
			if pirate.updateStatus():
				print(pirate.name+" meurt au combat. RIP")
				self._turn.removePirate()
			else:
				temp.append(pirate)
		self._team=temp
		self._numberOfPirates=len(self._team)
		if self._numberOfPirates==0:
			self._availableToFight=False

	def regenerateHealth(self):
		for pirate in self._team:
			pirate.regenerateHealth()

	def increaseCrewLevel(self):
		for pirate in self._team:
			pirate.increaseLevel()


	def removeFighter(self):
		self._turn.removeCurrent()

	def newFighter(self, pirate):
		self._team.append(pirate)
		self._turn.add(pirate)

	def __str__(self):
		txt=""
		for pirate in self._team:
			txt=txt+ str(pirate)
		return txt

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
		print(self._pirates)


	def removePirate(self):
		temp=[]
		for pirate in self._pirates:
			if pirate.mort==False:
				temp.append(pirate)
		self._pirates=temp


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


































