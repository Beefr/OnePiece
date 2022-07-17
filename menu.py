
from joueur import Joueur
from interactBDD import InteractBDD
from output import Output


class Menu(object):

	steps={ #1: "self.instanciateJoueur",
			1: "self.choseThatIsland", 
			2: "self.choseThatPirate"}
	parameters={#1: "[Menu.userInput[0],Menu.userInput[1]]",  
				1: "[self._userInput[-1]]",  
				2: "[self._userInput[-1]]"}
	


	def __init__(self):
		self._userInput=[]
		self._joueur=None
		self._currentStep=1
		self._output=Output()
		self._died=False
		self._tempData=None

	#TODO use fruit's allocation
	#TODO hook values from bdd and not code


	@property
	def joueur(self):
		return self._joueur

	@joueur.setter
	def joueur(self, joueur):
		self._currentStep=InteractBDD.getMyCurrentStep(joueur.username)
		self._joueur=joueur


	def showMenu(self, user_input=None):
		self._output.reset()


		if user_input!="None" and self._died==False:
			self._userInput=user_input
			str(eval(Menu.steps[self._currentStep] + "(" + self.getParameters() + ")"))
			self.nextStep()
		else:
			self._died=False
			self._userInput=[]
			self._currentStep=1
			self.choseThatIsland()
		
			
		return self._output.toBeDisplayed()

			

	def nextStep(self):
		if self._currentStep==1:
			self._currentStep=2
		elif self._currentStep==2:
			self._currentStep=1
		InteractBDD.setMyCurrentStep(self._joueur.username, self._currentStep)


	def getParameters(self):
		array=eval(Menu.parameters[self._currentStep])
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
			self._tempData=self._joueur.askForRecruitment(self._output)
		else:
			self._joueur.resetCrew()
			self._output.content+ "Ton équipage est mort, il va falloir recommencer du début pour devenir le roi des pirates. y/n"
			self._died=True


	def choseThatPirate(self, value):
		self._joueur.recrutement(len(self._tempData), self._output, self._tempData, value)
