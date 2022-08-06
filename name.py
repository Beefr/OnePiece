
from abc import abstractmethod
import random
class Name(object):


	def __init__(self, name):
		self._name=name


	@abstractmethod
	def generateName(self):
		raise NotImplementedError("Hey, Don't forget to implement")


	@property
	def name(self):
		return self._name


	@staticmethod
	def generateNewName(name):
		if name==None:
			return Firstname()+Secondname()
		return name



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