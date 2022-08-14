

from multiLineMessage import MultiLineMessage
from message import Message
#from bdd import InteractBDD
from interactBDD import InteractBDD

class World(object):

	@staticmethod
	def next(currentIslandName, choix=0):
		availableIslands=World.nextIslandsAsArray(currentIslandName)
		try:
			return availableIslands[int(choix)]
		except:
			return availableIslands[0]


	@staticmethod
	def nextIslandsAsMessage(currentIslandName):
		array= MultiLineMessage()
		compteur=0

		availableIslands=InteractBDD().availableIslandsInCurrentArchipel(currentIslandName)
		for ile in availableIslands: # it's only their names
			array+ Message(str(compteur)+": " +ile, False, False, "rouge")
			compteur+=1

		availableArchipels=InteractBDD().availableIslandsInAvailableArchipels(currentIslandName)
		for arch in availableArchipels: # it's only their names
			array+ Message(str(compteur)+": " +arch, False, False, "rouge")
			compteur+=1

		return array

	@staticmethod
	def nextIslandsAsArray(currentIslandName):
		array= []
		availableIslands=InteractBDD().availableIslandsInCurrentArchipel(currentIslandName)
		for ile in availableIslands:
			array.append(ile)

		availableArchipels=InteractBDD().availableArchipels(currentIslandName)
		for archipel in availableArchipels:
			ile = InteractBDD().ilePrincipale(archipel)
			array.append(ile)

		return array



	@staticmethod
	def showMap(currentIslandName):
		array= MultiLineMessage()

		array+ "Vous êtes actuellement à"
		array* Message(currentIslandName, True, True, "rouge")
		array+ Message("", False, True)

		array+ Message("Les iles à proximité sont:", False, True)
		ilesProches=InteractBDD().availableIslandsInCurrentArchipel(currentIslandName)
		for ile in ilesProches:
			array+ Message(ile, False, True, "rouge")
		array+ Message("", False, True)

		array+ Message("Les archipels à proximité sont:", False, True)
		archipelsProches=InteractBDD().availableArchipels(currentIslandName)
		for archipel in archipelsProches:
			array+ Message(archipel, False, True, "rouge")

		return array

















