

from island import Island
from multiLineMessage import MultiLineMessage
from message import Message
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

		availableIslands=InteractBDD.availableIslands(currentIslandName)
		for ile in availableIslands: # it's only their names
			array+ Message(str(compteur)+": " +ile, False, "rouge")
			compteur+=1

		availableArchipels=InteractBDD.availableArchipels(currentIslandName)
		for ile in availableArchipels: # it's only their names
			array+ Message(str(compteur)+": " +ile, False, "rouge")
			compteur+=1

		return array

	@staticmethod
	def nextIslandsAsArray(currentIslandName):
		array= []
		availableIslands=InteractBDD.availableIslands(currentIslandName)
		for ile in availableIslands:
			array.append(ile)

		availableArchipels=InteractBDD.availableArchipels(currentIslandName)
		for archipel in availableArchipels:
			ile = InteractBDD.ilePrincipale(archipel)
			array.append(ile)

		return array



	@staticmethod
	def showMap(currentIslandName):
		array= MultiLineMessage()

		array+ "Vous êtes actuellement à"
		array* Message(currentIslandName, True, True, "rouge")

		array+ Message("Les iles à proximité sont:", False, True)
		ilesProches=InteractBDD.availableIslands(currentIslandName)
		for ile in ilesProches:
			array+ Message(ile, False, False, "rouge")

		array+ Message("Les archipels à proximité sont:")
		archipelsProches=InteractBDD.availableArchipels(currentIslandName)
		for archipel in archipelsProches:
			array+ Message(archipel, False, False, "rouge")

		return array

















