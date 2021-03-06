
from utils import Utils
from equipage import Equipage
from pirate import Pirate
from world import World
from interactBDD import InteractBDD
from island import Island

class Joueur(object):

	debug=False


	def __init__(self, username=0, password=0):
		InteractBDD.cleanUpDB()
		if Joueur.debug:
			self._username= username
			self._equipage= self.getMyCrew()
			self._position= self.getMyLocation()
			self._availableToFight=True
			
		elif username==0 and password==0:

			self._availableToFight=True
		else:
			if self.existInDB(username):
				if not InteractBDD.checkPassword(username, password):
					
					self._username= None
					
			else:
				self.createNewUser(username, password)
				InteractBDD.setMyCrew(username, World.carte()[0].islands[0].name, [Pirate(1, True, username)]) 
			self._username= username
			self._equipage= self.getMyCrew()
			self._position= self.getMyLocation()
			self._availableToFight=True
			

	def showMenu(self):
		if Joueur.debug:
			Utils.clear()
			print("Voici ton équipage:\n"+str(self._equipage)+"\n")
			print("Vous êtes actuellement ici: "+str(self._position)+"\n")
			World.showMap(self._position.name)
			nextIsland=World.next(self._position.name)
			if nextIsland==None:
				print("GG t'es devenu le roi des pirates")
				return None

			self._position=nextIsland
			self._equipage.regenerateHealth()
			Utils.fight(self._equipage, self._position.pirates)
			if self._equipage.availableToFight:
				self.recrutement(5)
			else:
				self._equipage= self.getMyCrew()
				self._position= self.getMyLocation()

				playagain= input("Ton équipage est mort, il va falloir recommencer du début pour devenir le roi des pirates. y/n \n" )
				while playagain!="y":
					playagain= input("Ton équipage est mort, il va falloir recommencer du début pour devenir le roi des pirates. y/n \n" )
				


			Utils.clear()
			self.showMenu()

		else:
			txt="Voici ton équipage:<br>"+str(self._equipage)+"<br>"
			txt=txt+"Vous êtes actuellement ici: "+str(self._position)+"<br>"
			txt=txt+World.showMap(self._position.name)
			
			txt=txt+"Dans quelle ile veux-tu aller maintenant? <br>"
			txt=txt+World.getNextStage(self._position.name)
			return txt

	def isinstance(self):
		return "Joueur"

	def resetCrew(self):
		InteractBDD.deleteUserProgress(self._username)
		InteractBDD.setMyCrew(self._username, World.carte()[0].islands[0].name, [Pirate(1, True, self._username)])


	def increaseCrewLevel(self):
		self._equipage.increaseCrewLevel()

	def goingToNextIsland(self, value):
		self._position=World.next(self._position.name, value)
		self._equipage.regenerateHealth()

		isThereOtherPlayer=InteractBDD.checkPlayer(self._position.name) # returns the username or None
		InteractBDD.setMyLocation(self._username, self._position.name)
		if isThereOtherPlayer!=None:
			ennemies=[]
			txtPirates=InteractBDD.getMyCrew(isThereOtherPlayer)
			for txt in txtPirates:
				ennemy=Utils.load(txt)
				ennemies.append(ennemy)
			otherPlayer=Joueur()
			otherPlayer.username=isThereOtherPlayer
			otherPlayer.equipage=Equipage(ennemies)
			otherPlayer.position=self._position
			txt="Aie c'est le bordel sur "+self._position.name+", "+isThereOtherPlayer+" et son équipage sont présents sur l'ile, le combat est inévitable.<br>"
			txt=txt+Utils.fight(self, otherPlayer)
			otherPlayer.cleanUpDeadPirates()
			if otherPlayer.availableToFight==False:
				otherPlayer.resetCrew()
				# TODO eventuellement rajouter un petit message quand le gars se reconnecte?

		else:
			txt="Arrivé sur "+self._position.name+", tu fais face à de nombreux pirates hostiles.<br>"
			txt=txt+Utils.fight(self, self._position.pirates)


		txt=txt+self.cleanUpDeadPirates()
		return txt

	def recrutement(self, number, pirates=[], value=0):
		if Joueur.debug:
			pirates=[]
			print("Des pirates sont disponibles au recrutement.\n")
			for i in range(0,number):
				pirate=Pirate(self._position.level)
				pirates.append(pirate)
				print("Choix "+str(i)+": "+str(pirate))
			value = int(input("Lequel voulez-vous recruter?\n"))
			if value<number:
				self._equipage.newFighter(pirates[value])

		else:
			if int(value)<number:
				newPirate=pirates[int(value)]
				self._equipage.newFighter(newPirate)
				InteractBDD.addNewFighter(self._username, newPirate)
			return self.showMenu()


	def cleanUpDeadPirates(self):
		if len(self._equipage.dead)==0:
			return ""
		txt="<br>Ces pirates sont tombés au combat:<br>"
		for pirate in self._equipage.dead:
			InteractBDD.removeFighter(self._username, pirate)
			txt=txt+str(pirate)+"<br>"
		txt=txt+"<br><br>"
		self._equipage.cleanUpDeadArray()
		return txt



	def askForRecruitment(self):
		pirates=[]
		number=5
		txt="Des pirates sont disponibles au recrutement.<br>"
		for i in range(0,number):
			pirate=Pirate(self._position.level)
			pirates.append(pirate)
			txt=txt+"Choix "+str(i)+": "+str(pirate)

		txt=txt+"Lequel voulez-vous recruter?<br>"
		return [txt, pirates]

	@property
	def position(self):
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


	@username.setter
	def username(self, username):
		self._username=username

	@position.setter
	def position(self, position):
		self._position=position

	@equipage.setter
	def equipage(self, equipage):
		self._equipage=equipage

	def existInDB(self, username):
		if Joueur.debug:
			return True
		else:
			return InteractBDD.existInDB(username)


	def createNewUser(self, username, password):
		if Joueur.debug:
			pass
		else:
			return InteractBDD.createUser(username, password)


	def checkPassword(self, username, password):
		if Joueur.debug:
			return True
		else:
			return InteractBDD.checkPassword(username, password)


	def getMyCrew(self):
		if Joueur.debug:
			return Equipage([Pirate(1, True)])
		else:
			txtPirates=InteractBDD.getMyCrew(self._username)
			if len(txtPirates)==0:
				pirate=Pirate(1, True, self._username)
				InteractBDD.setMyCrew(self._username, World.carte()[0].islands[0].name, [pirate])
				return Equipage([pirate])

			else:
				pirates=[]
				for txt in txtPirates:
					pirate=Utils.load(txt)
					pirates.append(pirate)
				return Equipage(pirates)


	def getMyLocation(self):
		if Joueur.debug:
			return World.carte()[0].islands[0]
		else:
			return Island(InteractBDD.getMyLocation(self._username),0,0)
	

















