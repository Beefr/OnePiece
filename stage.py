from message import Message

class Stage(object):

	def __init__(self, islands):
		self._islands=islands


	@property
	def islands(self):
		return self._islands

	def __add__(self, island):
		self._islands.append(island)


	def asMessageArray(self):
		array=[[Message("Les prochaines iles sont:")]]
		count=0
		for island in self._islands:
			array.append([Message("Choix "+str(count)+": "+str(island))])
			count+=1
		
		return array