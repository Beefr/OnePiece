
from joueur import Joueur
from interactBDD import InteractBDD
from output import Output


class Menu(object):

	userInput=[]
	steps={ #1: "self.instanciateJoueur",
			1: "self.choseThatIsland", 
			2: "self.choseThatPirate"}
	parameters={#1: "[Menu.userInput[0],Menu.userInput[1]]",  
				1: "[Menu.userInput[-1]]",  
				2: "[Menu.userInput[-1]]"}
	currentStep=1
	tempData=None


	def __init__(self):
		self._joueur=None
		Menu.userInput=[]
		Menu.currentStep=1
		self._output=Output()
		self._died=False

	#TODO use fruit's allocation
	#TODO hook values from bdd and not code


	@property
	def joueur(self):
		return self._joueur

	@joueur.setter
	def joueur(self, joueur):
		self._joueur=joueur


	def showMenu(self, user_input=None):
		self._output.reset()


		if user_input!=None and self._died==False:
			Menu.userInput=user_input
			str(eval(Menu.steps[Menu.currentStep] + "(" + Menu.getParameters() + ")"))
			self.nextStep()
		else:
			self._died=False
			Menu.userInput=[]
			Menu.currentStep=1
			self.choseThatIsland()
		
			
		return self._output.toBeDisplayed()

			

	def nextStep(self):
		if Menu.currentStep==1:
			Menu.currentStep=2
		elif Menu.currentStep==2:
			Menu.currentStep=1



	@staticmethod
	def getParameters():
		array=eval(Menu.parameters[Menu.currentStep])
		txt=""
		if array!=[]:
			for param in array:
				if txt!="":
					txt=txt+","
				try:
					txt=txt+'"'+param+'"'
				except: 
					txt= "Error: list and str concatenation"+str(param)
		return txt

	
	def choseThatIsland(self, value=None):
		if value!=None:
			self._joueur.goingToNextIsland(value, self._output)
			self.checkAliveForRecruitment()
		else:
			return self._joueur.showMenu(self._output)



	def checkAliveForRecruitment(self):
		if self._joueur.availableToFight:
			Menu.tempData=self._joueur.askForRecruitment(self._output)
		else:
			self._joueur.resetCrew()
			self._output.content+ "Ton équipage est mort, il va falloir recommencer du début pour devenir le roi des pirates. y/n"
			self._died=True


	def choseThatPirate(self, value):
		self._joueur.recrutement(len(Menu.tempData), self._output, Menu.tempData, value)
