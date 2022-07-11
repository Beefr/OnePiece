

from island import Island
from multiLineMessage import MultiLineMessage
from stage import Stage
from message import Message
from interactBDD import InteractBDD

class World(object):
			
	world = []
	avancee = {}


	def __init__(self):
		self.initWorld()

	@staticmethod
	def carte():
		return World.world

	@staticmethod
	def next(currentIslandName, choix=0):
		choix=int(choix)
		availableIslands=World.availableIslands(currentIslandName)
		World.getIsland(currentIslandName).regenerate()
		if choix<=len(availableIslands)-1 and choix>=0: # TODO verify user input

			try:
				island=availableIslands[int(choix)]
			except:
				island=availableIslands[0]
		else:
			return None
		return island


	@staticmethod
	def getIsland(currentIslandName):
		index=World.avancee[currentIslandName]
		stage=World.world[index]
		for island in stage.islands:
			if island.name==currentIslandName:
				return island

	@staticmethod
	def availableIslands(currentIslandName):
		maxIndex=len(World.world)-1
		minIndex=1
		index=World.avancee[currentIslandName]
		availableStages=[]
		for i in range(index-1,index+2): #it takes values index-1, index, index+1
			if i>=minIndex and i<=maxIndex:
				availableStages.append(World.world[i])
		availableIslands=[]
		for stage in availableStages:
			for island in stage.islands:
				if island.name!=currentIslandName:
					availableIslands.append(island)
		return availableIslands

	@staticmethod
	def getNextStage(currentIslandName):
		availableIslands=World.availableIslands(currentIslandName)
		return Stage(availableIslands).asMessageArray()


	def initWorld(self):
		worldsDatas=InteractBDD.initWorld()
		numberOfStages=InteractBDD.getNumberOfStages()
		World.world=[Stage([])] * int(numberOfStages)

		for islandData in worldsDatas:
			island=Island(islandData[0], int(islandData[3]), int(islandData[2]))
			test=World.world[int(islandData[1])]
			test2=test+island
			World.world[int(islandData[1])]=test2

			World.avancee[islandData[0]] = int(islandData[1])


	@staticmethod
	def has(name):
		for stage in World.world:
			for island in stage.islands:
				if island.name==name:
					return True
		return False

	@staticmethod
	def showMap(currentIslandName):
		array= MultiLineMessage()
		for stage in World.world:
			array+ Message('------------------------------------------------------------', False, True) #60
			#1 20 20
			#2 5 55 55 5
			spaceLength=60/(len(stage.islands)+1) -10
			for island in stage.islands:

				for i in range(int(spaceLength)):
					array+ Message(" ", False, False)

				array+ Message('|', False, False)
				if island.name!=currentIslandName:
					array+ Message(island.name, False, False)
				else:
					array+ Message(island.name, True, False, "rouge")
				array+ Message('|', False, False)

				for i in range(int(spaceLength)):
					array+ Message(" ", False, False)


				array+ Message(" ", False, True)

		return array

















