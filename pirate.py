
from abc import abstractmethod
from fruitdemon import FruitFactory
import random
from interactBDD import InteractBDD
from statsPirate import StatsPirate

class Pirate(object):

	debug=False

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


	@staticmethod
	def regenerateHealth(level, qualite):
		return 100*level*(5-qualite)

	
	def increaseLevel(self):
		if self._fruit.name=="None":
			increase=1
		else:
			increase=3
		self._level=InteractBDD.increasePirateLevel(self, increase)
		self._stats=StatsPirate.generateStats(self._level, self._qualite, self._fruit.power)


	def attaque(self):
		return self._stats[1]


	def fatigue(self):
		return self._stats[3]

	def increaseFatigue(self):
		self._stats[3]-=1
		if self._stats[3]<=0:
			self._availableToFight=False


	def updateStatus(self):
		self._mort=self.mort
		self._availableToFight= self._stats[3]>0
		return self._mort

	def getAttackedBy(self, pirate):
		degats=pirate.attaque()-self._stats[2]
		if degats<=0: #aucun degat reçu
			txt=self._name+" reçoit 0 pts de degats de la part de "+pirate.name+", il garde ses "+str(self._stats[0])+"pts de vie"
			pirate.increaseFatigue()
			return txt
		self._stats[0]=self._stats[0]-degats

		txt=self._name+" reçoit "+str(degats)+"pts de degats de la part de "+pirate.name+", il ne lui reste plus que "+str(self._stats[0])+"pts de vie"
		pirate.increaseFatigue()
		if self._stats[0]<=0:
			self._availableToFight=False
			self._mort=True
		return txt

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


	def __str__(self):
		if Pirate.debug:
			txt=self._name+"\n"
			txt=txt+"niveau: "+str(self._level)+" | qualité: "+str(self._qualite)+" | fruit: "+self._fruit.name+"\n"
			txt=txt+"vie: "+str(self._stats[0])+" | dps: "+str(self._stats[1])+" | def: "+str(self._stats[2])+" | fatigue: "+str(self._stats[3])+"\n"
			txt=txt+"___________________________________________________\n"
			return txt
		else:
			txt='<p><span style="color:red;"><b>'+self._name+"<b><br>"
			txt=txt+"niveau: "+str(self._level)+" | qualité: "+str(self._qualite)+" | fruit: "+self._fruit.name+"</span><br>"
			txt=txt+'<span style="color:green;">vie: '+str(self._stats[0])+" | dps: "+str(self._stats[1])+" | def: "+str(self._stats[2])+" | fatigue: "+str(self._stats[3])+"</span><br>"
			txt=txt+"___________________________________________________<br></p>"
			return txt






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






