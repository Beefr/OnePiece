

from bdd import InteractBDD
from output import Output


class Menu(object):

	steps={ #1: "self.instanciateJoueur",
			1: "self.choseThatIsland", 
			2: "self.choseThatPirate"}
	'''
	parameters={#1: "[Menu.userInput[0],Menu.userInput[1]]",  
				1: "[self._userInput[-1]]",  
				2: "[self._userInput[-1]]"}
	'''
	


	def __init__(self):
		self._userInput=[]
		self._joueur=None
		self._currentStep=1
		self._output=Output()
		self._died=False

	@property
	def joueur(self):
		return self._joueur

	@joueur.setter
	def joueur(self, joueur):
		self._currentStep=InteractBDD().getMyCurrentStep(joueur.username, joueur.gameid)
		self._joueur=joueur


	def showMenu(self, user_input="None"):
		self._output.reset()
		try:
			user_input=int(user_input)
		except:
			pass
		
		if self._died==True:
			self._output.content+ "Ton équipage est mort, la partie est finie pour toi."
		elif not isinstance(user_input, int):
			self._died=False
			self._userInput=[]
			str(eval(Menu.steps[self._currentStep] + "(" + self.getParameters() + ")"))
		else:
			self._userInput=user_input
			str(eval(Menu.steps[self._currentStep] + "(" + self.getParameters() + ")"))
			
		return self._output.toBeDisplayed()

			

	def nextStep(self):
		if self._currentStep==1:
			self._currentStep=2
		elif self._currentStep==2:
			self._currentStep=1
		InteractBDD().setMyCurrentStep(self._joueur.username, self._currentStep, self._joueur.gameid)


	def getParameters(self):
		if self._userInput==[]:
			return ""
		return str(self._userInput)
		'''
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
		return txt'''

	
	def choseThatIsland(self, value=None):
		if value!=None:
			self._joueur.goingToNextIsland(value, self._output)
			self.checkAliveForRecruitment()
		else:
			return self._joueur.showMenu(self._output)



	def checkAliveForRecruitment(self):
		if self._joueur.availableToFight:
			self._joueur.askForRecruitment(self._output) # put the pirates id that we want to recruit
			self.nextStep()
		else:
			self._joueur.resetCrew()
			self._output.content+ "Ton équipage est mort, la partie est finie pour toi."
			self._died=True
			self._currentStep=1


	def choseThatPirate(self, value=None):
		if value!=None:
			recruitablePirates=InteractBDD().getMyCrewsID("recrutement"+self._joueur.username, self._joueur.gameid)
			self._joueur.recrutement(self._output, recruitablePirates, value)
			self.nextStep()
		else:
			self.checkAliveForRecruitment()
		
