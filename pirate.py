from name import Name
from fruitdemon import FruitFactory, FruitDemon
import random
from bdd import InteractBDD
from statsPirate import StatsPirate
from message import Message

class Pirate(object):


	def __init__(self, gameid, level, capitaine=False, name=None, pnj=False):
		if capitaine:
			self._qualite=0
			self._fruit=FruitFactory.giveAFruit(gameid)
		elif pnj==False: # pour le recrutement
			self._qualite=Pirate.generateQualite([1,10,50,100])
			self._fruit=FruitFactory.allocateFruit([1,100], gameid)
		else: # pnj = True
			self._qualite=Pirate.generateQualite([0,10,50,100])
			self._fruit= FruitDemon("None",[0,0,0,0])

		self._name=str(Name.generateNewName(name))
		self._level=level
		[self._vie, self._atk, self._dfs]=StatsPirate.generateStats(self._level, self._qualite, self._fruit.power)
		self._mort=False


	@property
	def name(self):
		return self._name

	@property
	def vie(self):
		return self._vie

	@property
	def atk(self):
		return self._vie

	@property
	def dfs(self):
		return self._dfs

	@property
	def fruit(self):
		return self._fruit

	@property
	def level(self):
		return self._level

	@property
	def qualite(self):
		return self._qualite
		
	@property
	def mort(self):
		if self._vie<=0:
			self._mort=True
		return self._mort


	@name.setter
	def name(self, name):
		self._name=name

	@qualite.setter
	def qualite(self, qualite):
		self._qualite=qualite
		[self._vie, self._atk, self._dfs]=StatsPirate.generateStats(self._level, self._qualite, self._fruit.power)

	@fruit.setter
	def fruit(self, frui):
		self._fruit=frui
		[self._vie, self._atk, self._dfs]=StatsPirate.generateStats(self._level, self._qualite, self._fruit.power)


	@level.setter
	def level(self, lvl):
		self._level=lvl


	def takeDamages(self, degats):
		self._vie=self._vie-abs(degats)

	def isAttacked(self, pirate):
		if pirate is None:
			return Message("Cet équipage n'a plus personne de vivant. Fin du combat.", True, True)
		# c'est pirate qui attaque self
		degats=int(pirate.atk-self._dfs)
		phrase=InteractBDD().phraseDeCombat(pirate.name)

		if degats<=0: #aucun degat reçu
			texte=(pirate.name+phrase+self._name+", mais celui-ci ne prend aucun degats et garde ses "+str(self._vie)+"pts de vie")
			return Message(texte)
		
		self.takeDamages(degats)
		texte=(pirate.name+phrase+self._name+" pour un total de "+str(degats)+"degats, il ne lui reste plus que "+str(self._vie)+"pts de vie")
		if phrase=="attaque":
			return Message(texte)
		return Message(texte, True, False)

		
	
	@staticmethod
	def generateQualite(percentageQualite):
		
		percent = random.randint(0,100)
		if percent<=percentageQualite[0]:
			qualite=1
		elif percent<=percentageQualite[1]:
			qualite=2
		elif percent<=percentageQualite[2]:
			qualite=3
		else:
			qualite=4

		return qualite


	def asMessageArray(self):
		array=[]
		array.append([Message(self._name, True)])
		array.append([Message("niveau: "+str(self._level)+" | qualité: "+str(self._qualite)+" | fruit: "+self._fruit.name, True)])
		array.append([Message('vie: '+str(int(self._vie))+" | dps: "+str(int(self._atk))+" | def: "+str(int(self._dfs)))])
		array.append([Message("___________________________________________________", False, True)])
		return array



	def __str__(self):
		return self._name+" 	-lvl:"+str(self._level)+" 	-qual:"+str(self._qualite)+" 	-fruit:"+self._fruit.name+" 	-stats"+str([self._vie, self._atk, self._dfs])





class Legende(Pirate):

	def __init__(self, gameid, nom, level, fruit, qualite):
		self._gameid=gameid
		self._qualite=qualite
		self._fruit=fruit
		self._name=nom
		self._level=level
		[self._vie, self._atk, self._dfs]=StatsPirate.generateStats(self._level, self._qualite, self._fruit.power)
		self._mort=False


