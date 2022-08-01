

import random
from multiLineMessage import MultiLineMessage
from utils import Utils
from equipage import Equipage
from pirate import Pirate
from world import World
from interactBDD import InteractBDD
from island import Island
from message import Message


class Joueur(object):

	villeDeDepart='Village de Fuchsia'

	def __init__(self, username):		
		self._username= username
		self._equipage= self.getMyCrew()
		self._position= self.getMyLocation()
		self._availableToFight=True
		self._gameid=-1
		

	def showMenu(self, output):
		self._equipage= self.getMyCrew()
		self._position= self.getMyLocation()
		
		output.team+ "Voici ton équipage:"
		output.team+ Message("___________________________________________________", False, True)
		output.team+ self._equipage.asMessageArray()

		output.map+ World.showMap(self._position.name)
		
		output.content+ "Vous êtes actuellement ici: " 
		output.content+ Message(str(self._position), True, True, "vert")
		output.content+ Message("Dans quelle ile/archipel veux-tu aller maintenant?", True, False, "rouge")
		output.content+ World.nextIslandsAsMessage(self._position.name)

	def isinstance(self):
		return "Joueur"

	def resetCrew(self):
		InteractBDD.deleteUserProgress(self._username, self._gameid)
		self._equipage=Equipage([Pirate(1, True, self._username)])
		self._position= Island(Joueur.villeDeDepart)
		InteractBDD.setMyCrew(self._username, Joueur.villeDeDepart, self._equipage.team, 1, self._gameid)
		self._availableToFight=True


	def increaseCrewLevel(self):
		InteractBDD.increasePirateLevel(self._username, self._gameid)

	def goingToNextIsland(self, value, output):
		self._position=Island(World.next(self._position.name, value))
		self._equipage.regenerateHealth()

		isThereOtherPlayer=InteractBDD.checkPlayer(self._position.name, self._gameid) # returns the username or None
		InteractBDD.setMyLocation(self._username, self._position.name, self._gameid)
		if isThereOtherPlayer!=None:
			self.fightOtherPlayer(isThereOtherPlayer, output)
		else:
			self.fightPNJ(output)

		output.content+ self.cleanUpDeadPirates()

		output.team+ "Voici ton équipage:"
		output.team+ "___________________________________________________"
		output.team+ self._equipage.asMessageArray()

		output.map+ World.showMap(self._position.name)

	def fightOtherPlayer(self, isThereOtherPlayer, output):
		ennemies=[]
		txtPirates=InteractBDD.getMyCrew(isThereOtherPlayer, self._gameid)
		for txt in txtPirates:
			ennemy=Utils.load(txt)
			ennemies.append(ennemy)
		otherPlayer=Joueur(isThereOtherPlayer)
		otherPlayer.equipage=Equipage(ennemies)
		otherPlayer.position=self._position
		output.content+ "Aie c'est le bordel sur "
		output.content* self._position.name
		output.content* ","
		output.content+ Message(isThereOtherPlayer, True, False, "rouge")
		output.content* " et son équipage sont présents sur l'ile,"
		output.content+ "le combat est inévitable."
		output.content+self.fight(otherPlayer)
		otherPlayer.cleanUpDeadPirates()
		if otherPlayer.availableToFight==False:
			otherPlayer.resetCrew()
			# TODO eventuellement rajouter un petit message quand le gars se reconnecte?

	def fightPNJ(self, output):
		ennemies=Equipage.generateEnnemies(InteractBDD.averagePirateLevel(self._username, self._gameid), max(self._equipage.numberOfPirates,4))
		isThereBoss=InteractBDD.checkBoss(self._position.name)
		if isThereBoss!=None:
			ennemies.newFighter(Utils.load(isThereBoss))
		
		output.content+ "Arrivé sur "
		output.content* self._position.name
		output.content* ", tu fais face à de nombreux pirates hostiles."
		output.content+ self.fight(ennemies)



	def fight(self, entry2):		
		array= MultiLineMessage()
		first=random.randint(0,1)
		turnsCount=0
		while self.availableToFight and entry2.availableToFight:
			array+ Message("Tour "+str(turnsCount), True, False, "rouge")
			array+ self.phraseDeCombat(entry2, first)
			array+ self.phraseDeCombat(entry2, 1-first)
			turnsCount+=1

		if self.availableToFight:
			self.increaseCrewLevel()
			array+ Joueur.phraseDeVictoire(self)
			InteractBDD.deallocateFruitsFromCrew(entry2, self._gameid)
		else:
			if entry2.isinstance()=="Joueur":
				entry2.increaseCrewLevel()
			array+ Joueur.phraseDeVictoire(entry2)
			InteractBDD.deallocateFruitsFromCrew(self, self._gameid)
		return array


	def phraseDeCombat(self, entryB, first):
		output = MultiLineMessage()
		output+ Joueur.intro(self, entryB, first)
		output+ self.attaque(entryB, first)
		self.updateStatus()
		entryB.updateStatus()
		return output

	def updateStatus(self):
		self._equipage.updateStatus()

	def attaque(self, entryB, first):
		output = MultiLineMessage()
		if first==1: # entryB attacks
			output+ self.isAttacked(entryB.attaquant())

		else: # we attack
			output+ entryB.isAttacked(self.attaquant()) 

		return output

	def isAttacked(self, attaquant):
		return self._equipage.isAttacked(attaquant)

	def attaquant(self):
		return self._equipage.attaquant()

	@staticmethod
	def intro(entryA, entryB, first):
		attaquant="PNJ"
		boolean=False
		if first==1 and entryB.isinstance()=="Joueur":
			attaquant="de "+entryB.username
			boolean=True
		elif first==0: # self est forcement un joueur
			attaquant="de "+entryA.username
			boolean=True
		intro="Tour de l'équipage {} d'attaquer:".format(attaquant)
		return Message(intro, boolean)

	@staticmethod
	def phraseDeVictoire(entry):
		if entry.isinstance()=="Joueur":
			output= MultiLineMessage()
			output+ Message("L'équipage de "+entry.username+" remporte le combat, ils remportent tous un niveau:", True, True, "rouge")
			output+ entry.equipage.asMessageArray()
			return output
		elif entry.isinstance()=="Equipage":
			return Message("L'équipage PNJ remporte le combat!", True, True, "rouge")


	def recrutement(self, output, piratesID, value=0):
		
		if int(value)<len(piratesID):
			newPirate=piratesID[int(value)] # now it's not a pirate, it's an id
			truePirate=Utils.load(InteractBDD.getMyPirate(newPirate))
			self._equipage.newFighter(truePirate)
			InteractBDD.addNewFighter(self._username, truePirate, self._gameid) # i dont fking want to create a method that updates the owner's name
		self.showMenu(output)


	def cleanUpDeadPirates(self):
		if len(self._equipage.dead)==0:
			return Message("")
		array=[[Message("Ces pirates sont tombés au combat:", True, False, "rouge")]]
		for pirate in self._equipage.dead:
			InteractBDD.removeFighter(self._username, pirate, self._gameid)
			array.extend(pirate.asMessageArray())
		self._equipage.cleanUpDeadArray()
		return array



	def askForRecruitment(self, output):
		InteractBDD.deletePirates("recrutement"+self._username, self._gameid) # clean up precedent recrutement
		crewMinLevel=InteractBDD.getMyCrewMinLevel(self._username, self._gameid)
		number=5
		start=0
		output.content+ Message("Des pirates sont disponibles au recrutement.", True, False, "rouge")

		obj=InteractBDD.getDrop(self._position.name, self._username)
		if obj!=None:
			[isThereBoss, drop]=obj
			percent = random.randint(0,100)
			if percent<=drop:
				start=1
				boss=Utils.load(isThereBoss)
				boss.level=crewMinLevel
				boss.qualite=0
				InteractBDD.addNewFighter("recrutement"+self._username, boss, self._gameid)
				output.content+ "Choix 0:"
				output.content+ boss.asMessageArray()

		for i in range(start,number):
			pirate=Pirate(crewMinLevel)
			InteractBDD.addNewFighter("recrutement"+self._username, pirate, self._gameid)
			output.content+ "Choix "
			output.content* Message(str(i))
			output.content* ": "
			output.content+ pirate.asMessageArray()
		output.content+ Message("Lequel voulez-vous recruter?", True, False, "rouge")
		return None

	@property
	def position(self):
		self._position= self.getMyLocation()
		return self._position

	@property
	def username(self):
		return self._username

	@property
	def equipage(self):
		return self._equipage

	@property
	def availableToFight(self):
		self._availableToFight=self._equipage.availableToFight
		return self._availableToFight

	@property
	def gameid(self):
		return self._gameid

	@gameid.setter
	def gameid(self, gid):
		self._gameid=gid

	@username.setter
	def username(self, username):
		self._username=username

	@position.setter
	def position(self, position):
		self._position=position

	@equipage.setter
	def equipage(self, equipage):
		self._equipage=equipage

	@availableToFight.setter
	def availableToFight(self, av):
		self._availableToFight=av


	def getMyCrew(self):
		txtPirates=InteractBDD.getMyCrew(self._username, self._gameid)
		if len(txtPirates)==0:
			pirate=Pirate(1, True, self._username)
			InteractBDD.setMyCrew(self._username, Joueur.villeDeDepart, [pirate],1, self._gameid)
			return Equipage([pirate])

		else:
			pirates=[]
			for txt in txtPirates:
				pirate=Utils.load(txt)
				pirates.append(pirate)
			return Equipage(pirates)


	def getMyLocation(self):
		island = InteractBDD.getMyLocation(self._username, self._gameid)
		if island!="":
			return Island(island)
		else:
			InteractBDD.setMyLocation(self._username, Joueur.villeDeDepart, self._gameid)
			return Island(Joueur.villeDeDepart)
	

















