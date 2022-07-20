
from abc import abstractmethod
from fruitdemon import FruitFactory
import random
from interactBDD import InteractBDD
from statsPirate import StatsPirate
from message import Message

class Pirate(object):


	def __init__(self, level, capitaine=False, name=None):
		if capitaine:
			self._qualite=1
			self._fruit=FruitFactory.giveAFruit()
		else:
			self._qualite=self.generateQualite([1,10,50,100])
			self._fruit=FruitFactory.allocateFruit([1,100])

		self._name=self.generateNewName(name)
		self._level=level
		self._stats=StatsPirate.generateStats(self._level, self._qualite, self._fruit.power)
		self._availableToFight=True
		self._mort=False


	@property
	def name(self):
		return self._name

	@property
	def stats(self):
		return self._stats

	@property
	def availableToFight(self):
		return self._availableToFight

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
		if self._stats[0]<=0:
			self._mort=True
		return self._mort


	@name.setter
	def name(self, name):
		self._name=name

	@qualite.setter
	def qualite(self, qualite):
		self._qualite=qualite
		self._stats=StatsPirate.generateStats(self._level, self._qualite, self._fruit.power)

	@fruit.setter
	def fruit(self, frui):
		self._fruit=frui
		self._stats=StatsPirate.generateStats(self._level, self._qualite, self._fruit.power)


	@stats.setter
	def stats(self, st):
		self._stats=st

	@staticmethod
	def regenerateHealth(level, qualite):
		return 100*level*(5-qualite)

	def defense(self):
		return self._stats[2]
	
	def attaque(self):
		return self._stats[1]


	def vie(self):
		return int(self._stats[0])

	def takeDamages(self, degats):
		self._stats[0]=self._stats[0]-degats

	def fatigue(self):
		return self._stats[3]

	def increaseFatigue(self):
		self._stats[3]-=1
		if self._stats[3]<=0:
			self._availableToFight=False

	def is_instance(self):
		return "Pirate"

	def updateStatus(self):
		self._mort=self.mort
		self._availableToFight= self._stats[3]>0
		return self._mort

	def isAttacked(self, pirate):
		if pirate is None:
			return Message("Cet équipage n'a plus personne de vivant. Fin du combat.", True, True)
		# c'est pirate qui attaque self
		degats=int(pirate.attaque()-self.defense())
		phrase=InteractBDD.phraseDeCombat(pirate.name)
		if phrase!=None:
			if degats<=0: #aucun degat reçu
				texte=(pirate.name+" {} "+self.name+", mais celui-ci ne prend aucun degats et garde ses "+str(self.vie())+"pts de vie").format(phrase)
				return Message(texte)
			
			self.takeDamages(degats)
			texte=(pirate.name+" {} "+self.name+" pour un total de "+str(degats)+"degats, il ne lui reste plus que "+str(self.vie())+"pts de vie").format(phrase)
			return Message(texte, True, False)
		else:
			if degats<=0: #aucun degat reçu
				return Message(pirate.name+" attaque "+self.name+", mais celui-ci ne prend aucun degats et garde ses "+str(self.vie())+"pts de vie")
			
			self.takeDamages(degats)
			return Message(pirate.name+" inflige "+str(degats)+"pts de degats à "+self.name+", il ne lui reste plus que "+str(self.vie())+"pts de vie")


	def generateNewName(self, name):
		if name==None:
			return Firstname()+Secondname()
		return name
		


	def giveAFruit(self, fruit):
		if fruit=="":
			return FruitFactory.giveAFruit()
		else:
			return FruitFactory.giveThatFruit(fruit)

	

	def generateQualite(self, percentageQualite):
		
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


	def generateDemonBool(self, percentageDemonBool):
		percent = random.randint(0,100)	
		if percent<=percentageDemonBool[0]:
			demonBool=True
		else:
			demonBool=False

		return demonBool


	def asMessageArray(self):
		array=[]
		array.append([Message(self._name, True)])
		array.append([Message("niveau: "+str(self._level)+" | qualité: "+str(self._qualite)+" | fruit: "+self._fruit.name, True)])
		array.append([Message('vie: '+str(int(self._stats[0]))+" | dps: "+str(int(self._stats[1]))+" | def: "+str(int(self._stats[2]))+" | fatigue: "+str(int(self._stats[3])))])
		array.append([Message("___________________________________________________", False, True)])
		return array






class Name(object):


	def __init__(self, name):
		self._name=name


	@abstractmethod
	def generateName(self):
		raise NotImplementedError("Hey, Don't forget to implement")


	@property
	def name(self):
		return self._name




class Firstname(Name):

	def __init__(self):
		firstname=self.generateName()
		super().__init__(firstname)


	def generateName(self):
		dictionnaire=["Kevin", "Roger", "Tiburce", "Gertrude", "Berthe", "Robert", "Blaise", "Titeuf", "Bob", "Berenice", "Benedicte", "Sbleurgh", "Adelaide", "Isidore", "Magdalena", "Augustin", "Mayeul", "Rodrigue", "Denis", "Eude"]
		index=random.randint(0,len(dictionnaire)-1)
		return dictionnaire[index]


	def __add__(self, secondname):
		return self._name+" "+secondname.name






class Secondname(Name):

	def __init__(self):
		secondname=self.generateName()
		super().__init__(secondname)


	def generateName(self):
		dictionnaire=["Tapedur", "Tankfor", "Grossbarb", "Epeenmousse", "Lechauv", "Coursurpat", "Penkibit", "Grofiak", "Moudujnou", "Potremalin", "Barbkipik", "Sendeloin", "Vendecarpet", "Aleuilkidifukalotr", "Couymol", "Persondentier"]
		index=random.randint(0,len(dictionnaire)-1)
		return dictionnaire[index]


class Legende(Pirate):

	def __init__(self, nom, level, fruit, qualite):
		self._qualite=qualite
		self._fruit=FruitFactory.giveThatFruit(fruit)
		self._name=nom
		self._level=level
		self._stats=StatsPirate.generateStats(self._level, self._qualite, self._fruit.power)
		self._availableToFight=True
		self._mort=False

	def is_instance(self):
		return "Legende"

	'''
	def isAttacking(self, pirate):
		# c'est pirate qui attaque self
		degats=self._stats[1]-pirate.defense()
		if degats<=0: #aucun degat reçu
			texte=(pirate.name+" {} "+self.name()+", mais celui-ci ne prend aucun degats et garde ses "+str(self.vie())+"pts de vie").format(InteractBDD.phraseDeCombat(pirate.name))
			return Message(texte)
		
		self.takeDamages(self, degats)
		texte=(pirate.name+" {} "+self.name()+" pour un total de "+str(degats)+"degats, il ne lui reste plus que "+str(self.vie())+"pts de vie").format(InteractBDD.phraseDeCombat(pirate.name))
		return Message(texte, True, False)
		'''
