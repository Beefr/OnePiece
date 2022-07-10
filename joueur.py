
from utils import Utils
from equipage import Equipage
from pirate import Pirate
from world import World
from interactBDD import InteractBDD
from island import Island
from message import Message


class Joueur(object):


	def __init__(self, username, password=None):
		if password!=None:
			password=Utils.hashPassword(password)
			self.createNewUser(username, password) 
		
		self._username= username
		self._equipage= self.getMyCrew()
		self._position= self.getMyLocation()
		self._availableToFight=True
		self._world= World()

		

	def showMenu(self, output):
		self._equipage= self.getMyCrew()
		self._position= self.getMyLocation()
		
		output.team+ "Voici ton équipage:"
		output.team+ Message("___________________________________________________", False, True)
		output.team+ self._equipage.asMessageArray()

		output.map+ self._world.showMap(self._position.name)
		
		output.content+ "Vous êtes actuellement ici: " 
		output.content+ Message(str(self._position), True, True, "vert")
		output.content+ Message("Dans quelle ile veux-tu aller maintenant?", True, False, "rouge")
		output.content+ self._world.getNextStage(self._position.name)

	def isinstance(self):
		return "Joueur"

	def resetCrew(self):
		InteractBDD.deleteUserProgress(self._username)
		InteractBDD.setMyCrew(self._username, self._world.carte()[0].islands[0].name, [Pirate(1, True, self._username)])
		self._equipage= self.getMyCrew()
		self._position= self.getMyLocation()
		self._availableToFight=True


	def increaseCrewLevel(self):
		InteractBDD.increasePirateLevel(self._username)

	def goingToNextIsland(self, value, output):
		self._position=self._world.next(self._position.name, value)
		self._equipage.regenerateHealth()

		isThereOtherPlayer=InteractBDD.checkPlayer(self._position.name) # returns the username or None
		InteractBDD.setMyLocation(self._username, self._position.name)
		if isThereOtherPlayer!=None:
			ennemies=[]
			txtPirates=InteractBDD.getMyCrew(isThereOtherPlayer)
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
			output.content+Utils.fight(self, otherPlayer)
			otherPlayer.cleanUpDeadPirates()
			if otherPlayer.availableToFight==False:
				otherPlayer.resetCrew()
				# TODO eventuellement rajouter un petit message quand le gars se reconnecte?

		else:
			output.content+ "Arrivé sur "
			output.content* self._position.name
			output.content* ", tu fais face à de nombreux pirates hostiles."
			output.content+ Utils.fight(self, self._position.pirates)


		output.content+self.cleanUpDeadPirates()

		output.team+ "Voici ton équipage:"
		output.team+ "___________________________________________________"
		output.team+ self._equipage.asMessageArray()

		output.map+ self._world.showMap(self._position.name)

	def recrutement(self, number, output, pirates=[], value=0):
		
		if int(value)<number:
			newPirate=pirates[int(value)]
			self._equipage.newFighter(newPirate)
			InteractBDD.addNewFighter(self._username, newPirate)
		self.showMenu(output)


	def cleanUpDeadPirates(self):
		if len(self._equipage.dead)==0:
			return Message("")
		array=[[Message("Ces pirates sont tombés au combat:", True, False, "rouge")]]
		for pirate in self._equipage.dead:
			InteractBDD.removeFighter(self._username, pirate)
			array.extend(pirate.asMessageArray())
		self._equipage.cleanUpDeadArray()
		return array



	def askForRecruitment(self, output):
		pirates=[]
		number=5
		output.content+ Message("Des pirates sont disponibles au recrutement.", True, False, "rouge")
		for i in range(0,number):
			pirate=Pirate(self._position.level)
			pirates.append(pirate)
			output.content+ "Choix "
			output.content* Message(str(i))
			output.content* ": "
			output.content+ pirate.asMessageArray()

		output.content+ Message("Lequel voulez-vous recruter?", True, False, "rouge")
		return pirates

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




	def createNewUser(self, username, password):
		return InteractBDD.createUser(username, password)


	def checkPassword(self, username, password):
		return InteractBDD.checkPassword(username, password)


	def getMyCrew(self):
		txtPirates=InteractBDD.getMyCrew(self._username)
		if len(txtPirates)==0:
			pirate=Pirate(1, True, self._username)
			InteractBDD.setMyCrew(self._username, self._world.carte()[0].islands[0].name, [pirate])
			return Equipage([pirate])

		else:
			pirates=[]
			for txt in txtPirates:
				pirate=Utils.load(txt)
				pirates.append(pirate)
			return Equipage(pirates)


	def getMyLocation(self):
		island = InteractBDD.getMyLocation(self._username)
		if island!="":
			return Island(island,0,0)
		else:
			InteractBDD.setMyLocation(self._username, self._world.carte()[0].islands[0].name)
			return Island(self._world.carte()[0].islands[0].name,0,0)
	

















