imported=False
try:
	import mariadb
	imported=True
except:
	pass

from statsPirate import StatsPirate
from sql import SQL
import random


class PoolOfRequests(object):

	config = {
	    'host': 'mariadb-anog-service',
	    'port': 3306,
	    'user': 'root',
	    'password': 'pwd',
	    'database': 'data'
	}

	def __init__(self):
		self._conn=mariadb.connect(**PoolOfRequests.config)
		self._cur=self._conn.cursor()
		self._commands=[]

	def __add__(self, command):
		return Request(command.sql, command.commit, self._conn, self._cur).execute()

	
	def __del__(self):
		self._cur.close()
		self._conn.close()


class Request(object):

	def __init__(self, sql, needCommit, conn, cur):
		self._sql=sql
		self._conn=conn
		self._cur=cur
		self._commit=needCommit

	def execute(self):
		if self._commit:
			Request.connectAndExecuteRequest(self._sql, self._commit, self._conn, self._cur)
		else:
			description = Request.connectAndExecuteRequest(self._sql, self._commit, self._conn, self._cur)
			return Resultat(description)
		
	@staticmethod
	def connectAndExecuteRequest(request, needCommit, conn, cur):
		if needCommit:
			try:
				cur.execute(request)
				conn.commit()
			except:
				conn.rollback()
		else:
			cur.execute(request)
		return cur

class Resultat(object):

	def __init__(self, description):
		self._items=[] # c'est une liste de listes
		for item in description:
			self._items.append(list(item))
		self._currentIndex=0

	@property
	def items(self):
		return self._items

	@property
	def singleItems(self):
		items=[]
		for item in self._items:
			items.append(item[0])
		return items

	@property
	def first(self):
		return self._items[0][0]

	@property
	def pirates(self, classe, gameid):
		pi=[]
		for elem in self.items:
			pi.append(InteractBDD.pirateTXT(elem, classe, gameid))
		return pi


	def exists(self):
		if isinstance(self.first, int) or isinstance(self.first, str):
			return True
		return False

	def asText(self):
		txt=""
		for item in self._items:
			for elem in item:
				txt= txt+"| " + str(elem)
			txt=txt+"<br>"
		txt=txt+"<br>"
		return txt


class Command(object):

	def __init__(self, sql, needCommit):
		self._sql=sql
		self._commit=needCommit

	@property
	def sql(self):
		return self._sql

	@property
	def commit(self):
		return self._commit





class InteractBDD(object):

	def __init__(self):
		self._pool=PoolOfRequests()

	#___________________________GAMES_____________________________
	def createGame(self, username):
		gameid=self.maxGameID()+1
		self._pool +Command(SQL.insertGames.format(str(gameid),username), True)
		self.setFruitsForGame(gameid)
		return gameid

	def addUser(self, username, gameid):
		result=True
		if self.gameExists(gameid):
			count=0
			res=self._pool +Command(SQL.selectGID.format(str(gameid)), False) 
			for elem in res.items:
				count+=1
				if int(elem[0])==0:
					# si la partie est finie on peut pas la join
					result=False
				if str(elem[1])==username:
					# si le joueur est déjà dans la partie il peut pas la rerejoindre
					result=False
			if count<8 and result:
			# on le rajoute aux joueurs
				InteractBDD.addToGame(gameid, username)
				fruitsname=self.giveAFruit(gameid)
				tuple={ "name": username, "level": str(1), "fruit": {"name": fruitsname}, "qualit": str(0) }
				InteractBDD.setMyCrew(username, self.villeDeDepart(), tuple, str(1), str(gameid) )
			else: # plus de place pour jouer avec ses potes
				result=False
		else: # partie existe pas
			result=False
		return result
		
	def joinThatGameID(self, username, gameid):
		result=True
		if self.gameExists(gameid):
			count=0
			res=self._pool +Command(SQL.selectEnCours.format(str(gameid)), False) 
			for elem in res.items:
				count+=1
				if int(elem[0])==0: # si la partie est finie on peut pas la join
					result=False
				if str(elem[1])==username: # si le joueur est déjà dans la partie il peut pas la rerejoindre
					result=False
			if count>=8: # trop de joueurs
				result=False
		else: # partie existe pas
			result=False
		return result

	def joinGame(self, username, gameid):
		result=self.joinThatGameID(username, gameid)
		if result==False:
			gameid=gameid+1
		self.addToGame(gameid, username)
		self.setFruitsForGame(gameid)
		fruitsname=self.giveAFruit(gameid)
		self.addNewPirate(username, username, 1, fruitsname, 0, gameid)
		self.allocateFruit(fruitsname, gameid)
		self.setMyLocation(username, self.villeDeDepart(), gameid)
		return gameid

	def addToGame(self, gameid, username):
		self._pool +Command(SQL.insertGames.format(str(gameid), username), True) 

	def numberOfGames(self, username):
		res=self._pool +Command(SQL.selectGID.format(username), False) 
		return len(res.items)

	def villeDeDepart(self):
		res=self._pool +Command(SQL.selectNomIle, False) 
		iles=res.singleItems
		ile=iles[random.randint(0, len(iles)-1)]
		return ile

	def gamesInProgress(self, username):
		res=self._pool +Command(SQL.selectGID.format(username), False) 
		return res.singleItems	

	def gameExists(self, gameid):
		res=self._pool +Command(SQL.selectGID2.format(gameid), False) 
		return res.exists()

	def maxGameID(self):
		gameid=0
		res=self._pool +Command(SQL.selectMaxGID, False) 
		if res.exists():
			gameid=res.first
		return gameid

	#___________________________CREDENTIALS_______________________
	def existInDB(self, username):
		res=self._pool +Command(SQL.selectUsername.format(username), False) 
		return res.exists()

	def createUser(self, username, password):
		self._pool +Command(SQL.insertJoueur.format(username, password), True)

	def checkPassword(self, username, password):
		res=self._pool +Command(SQL.selectPassword.format(username), False) 
		if res.first==password:
				return True
		return False

	#_________________________GET___________________________
	def getID(self, username):
		res=self._pool +Command(SQL.selectIDjoueur.format(username), False) 
		return res.first

	def getUsername(self, id):
		res=self._pool +Command(SQL.selectUsername2.format(str(id)), False) 
		return res.first

	def getMyCrew(self, username, gameid):
		res=self._pool +Command(SQL.selectPirate.format(username, str(gameid)), False) 
		pirates=[]
		for elem in res.items:
			txt=self.pirateTXT(elem, 'Pirate', gameid)
			pirates.append(txt) 
		return pirates

	def getMyPirate(self, id, gameid):
		res=self._pool +Command(SQL.selectPirate2.format(str(id)), False)
		return self.pirateTXT(res.first, 'Pirate', gameid)

	def getMyCrewsID(self, username, gameid):
		res=self._pool +Command(SQL.selectIDpirate.format(username, str(gameid)), False)
		return res.items

	def getMyCrewMinLevel(self, username, gameid):
		res=self._pool +Command(SQL.selectMinLevel.format(username, str(gameid)), False)
		return res.first

	def getMyLocation(self, username, gameid):
		res=self._pool +Command(SQL.selectPosition.format(username, str(gameid)), False)
		return res.first

	def getMyCurrentStep(self, username, gameid):
		res=self._pool +Command(SQL.selectCurrentStep.format(username, str(gameid)), False)
		return res.first
	
	def checkPlayer(self, islandName, gameid):
		res=self._pool +Command(SQL.checkIsland.format(islandName, str(gameid)), False)
		return res.first

	def averagePirateLevel(self, username, gameid):
		res=self._pool +Command(SQL.selectLevel.format(username, str(gameid)), False)
		levels=res.items
		return sum(levels)/len(levels)

	def getBoss(self, currentIslandName):
		res=self._pool +Command(SQL.selectPNJ.format(currentIslandName), False)
		return res.first

	def checkBoss(self, currentIslandName, gameid):
		res=self._pool +Command(SQL.selectPNJ.format(currentIslandName), False)
		return res.pirates('Legende', gameid)[0] #list of string[0]

	def phraseDeCombat(self, pnjName):
		res=self._pool +Command(SQL.selectPhrase.format(pnjName), False)
		if res.exists():
			return res.first
		return " attaque "

	def getDrop(self, currentIslandName, username, gameid):
		res=self._pool +Command(SQL.selectDrop.format(currentIslandName), False)
		drop = res.first
		if drop==0:
			return None
		boss=self.getBoss(currentIslandName)
		if self.hasThatBoss(boss[0], username, gameid):
			return None
		txt=self.pirateTXT(boss, 'Legende', gameid)
		return [txt, drop]
		
	def hasThatBoss(self, bossName, username, gameid):
		res=self._pool +Command(SQL.selectName.format(username, bossName, str(gameid)), False)
		return res.exists()

	#_____________________STORE_______________________________
	def setMyCrew(self, username, positionsName, pirates, currentstep, gameid):
		for pirate in pirates:
			self._pool +Command(SQL.insertPirate.format(username, pirate.name, str(pirate.level), pirate.fruit.name, str(pirate.qualite), str(gameid)), True)
		self._pool +Command(SQL.updateIsland.format(positionsName, username, str(gameid)), True)
		self._pool +Command(SQL.updateGames.format(str(currentstep), username, str(gameid)), True)
	
	def setMyLocation(self, username, positionsName, gameid):
		self._pool +Command(SQL.deleteIsland.format(username, str(gameid)), True)
		self._pool +Command(SQL.insertIsland.format(username, positionsName, str(gameid)), True)

	def setMyCurrentStep(self, username, currentStep, gameid):
		self._pool +Command(SQL.updateGames.format(str(currentStep), username, str(gameid)), True)

	def addNewPirate(self, username, name, level, fruitsname, qualite, gameid): 
		self._pool +Command(SQL.insertPirate.format(username, name, str(level), fruitsname, str(qualite), str(gameid)), True)
		
	def increasePirateLevel(self, username, gameid):
		self._pool +Command(SQL.updatePirate1.format(username, str(gameid)), True)
		self._pool +Command(SQL.updatePirate3.format(username, str(gameid)), True)

	#_________________________FRUITS_________________________________
	def setFruitsForGame(self, gameid):
		for sql in SQL.fruits:
			self._pool +Command(sql.format(str(gameid)), True)

	def giveAFruit(self, gameid):
		availableFruits=self.countAvailableFruits(gameid)
		if availableFruits==0:
			return "GumGum"
		fruitsNumber=random.randint(0,availableFruits-1)
		fruitsName=self.notAllocatedFruits(gameid)[fruitsNumber]
		self.allocateFruit(fruitsName, gameid)
		return fruitsName

	def countAvailableFruits(self, gameid):
		self.checkAllocatedFruits(gameid)
		res=self._pool +Command(SQL.selectCount.format(str(gameid)), False)
		return res.first

	def checkAllocatedFruits(self, gameid):
		self._pool +Command(SQL.updateFruit2.format(str(0), str(gameid)), True)
		res=self._pool +Command(SQL.selectFruit.format(str(gameid)), False)
		for elem in res.items:
			self.allocateFruit(elem[0], gameid)

	def notAllocatedFruits(self, gameid):
		res=self._pool +Command(SQL.selectFruitsname.format(str(gameid)), False)
		return res.items

	def fruitsPower(self, fruitsName):
		if fruitsName=='None':
			return [0,0,0,0]
		res=self._pool +Command(SQL.selectFruitsname.format(fruitsName), False)
		strpower=res.first
		power=list(map(int, strpower.split(",") )) # [1,2,3,4]
		return power

	def allocateFruit(self, fruitsName, gameid):
		self._pool +Command(SQL.updateFruit.format(str(1), str(fruitsName), str(gameid)), True)

	#_________________________WORLD_________________________________
	def availableIslandsInCurrentArchipel(self, currentIslandName):
		currentArchipelName=self.getArchipelFromIle(currentIslandName)
		islandNames=[] # and we must also get all the islands inside the current archipel
		res=self._pool +Command(SQL.selectFruitsname.format(currentArchipelName), False)
		if res.first!=currentIslandName:
			islandNames.append(res.first) 
		return islandNames

	def availableIslandsInAvailableArchipels(self, currentIslandName):
		connectedArchipels=self.availableArchipels(currentIslandName)
		islandNames=[]
		for archipel in connectedArchipels:
			islandNames.append(self.ilePrincipale(archipel)) 
		return islandNames

	def getArchipelFromIle(self, currentIslandName):
		res=self._pool +Command(SQL.selectArchipel.format(currentIslandName), False)
		return res.first

	def getConnectedArchipels(self, currentArchipelName):
		connectedArchipels=[]
		res=self._pool +Command(SQL.selectLiaison.format(currentArchipelName, currentArchipelName), False)
		for elem in res.items:
			if str(elem[0])!=currentArchipelName:
				connectedArchipels.append(str(elem[0])) 
			if str(elem[1])!=currentArchipelName:
				connectedArchipels.append(str(elem[1])) 
		return connectedArchipels

	def availableArchipels(self, currentIslandName):
		currentArchipelName=self.getArchipelFromIle(currentIslandName)
		connectedArchipels=self.getConnectedArchipels(currentArchipelName)
		return connectedArchipels	
		
	def ilePrincipale(self, archipel):
		res=self._pool +Command(SQL.selectIlePrincipale.format(archipel), False)
		return res.first

	#_________________________DELETE_________________________________
	def deleteUserProgress(self, username, gameid):
		self._pool +Command(SQL.deleteIsland.format(username, str(gameid)), True)
		self.deletePirates(username, gameid)

	def deletePirates(self, username, gameid):
		res=self._pool +Command(SQL.selectFruit2.format(username, str(gameid)), False) 
		for elem in res.items:
			fruitsName=elem[0]
			self._pool +Command(SQL.updateFruit.format(str(0), fruitsName, str(gameid)), True)
		self._pool +Command(SQL.deletePirate2.format(username, str(gameid)), True)

	def deallocateFruitsFromCrew(self, obj, gameid):
		if obj.isinstance()=="Joueur":
			crew=obj.equipage
		else: #equipage
			crew=obj
		for pirate in crew.team:
			if pirate.fruit.name!="None":
				self._pool +Command(SQL.updateFruit.format(str(0), str(pirate.fruit.name), str(gameid)), True)

	def removeFighter(self, username, pirate, gameid):
		fruitsName=pirate.fruit.name
		if fruitsName!="None":
			self._pool +Command(SQL.updateFruit.format(str(0), fruitsName, str(gameid)), True)
		self._pool +Command(SQL.deletePirate.format(username, pirate.name, pirate.fruit.name, str(pirate.qualite), str(gameid)), True)

	#____________________________________________________________
	def pirateTXT(self, elem, cls, gameid):
		piratesName=elem[0]
		level=elem[1]
		fruitsName=elem[2]
		qualite=elem[3]

		boss= cls=="Legende"

		power=self.fruitsPower(fruitsName)
		fruitsTXT='{"type": "FruitDemon", "name": "%s", "power": %s, "boss": "%s"}' % (fruitsName, str(power), str(boss)) 
		txt='{"type": "%s", "name": "%s", "gameid": %s, "level": %s, "qualite": %s, "fruit": %s, "stats": "%s", "availableToFight": "True", "mort": "False"}' % (cls, piratesName, str(gameid), str(level), str(qualite), fruitsTXT, str(StatsPirate.generateStats(level, qualite, power)) )
		return txt

	def retrieveWholeDatabase(self):
		txt=""
		
		txt=txt+"Games: <br>"
		txt=txt+"id | gameid | username | encours | currentStep<br>"
		res=self._pool +Command(SQL.selectAllGames, False) 
		txt=txt+res.asText()

		txt=txt+"Joueur: <br>"
		txt=txt+"id | username | password  <br>"
		res=self._pool +Command(SQL.selectAllJoueurs, False) 
		for elem in res.items:
			txt= txt+"| " + str(elem[0])
			txt= txt+"| " + str(elem[1])
			txt= txt+"| " + "Not Displayable"
			txt=txt+"<br>"
		txt=txt+"<br>"

		txt=txt+"island: <br>"
		txt=txt+"username | position's name | gameid <br>"
		res=self._pool +Command(SQL.selectAllIsland, False) 
		txt=txt+res.asText()

		txt=txt+"Pirate: <br>"
		txt=txt+" id | owner | name | level | fruit's name | qualite | gameid <br>"
		res=self._pool +Command(SQL.selectAllPirate, False) 
		txt=txt+res.asText()

		txt=txt+"Fruit: <br>"
		txt=txt+" name | power | allocated  | gameid<br>"
		res=self._pool +Command(SQL.selectAllFruit, False) 
		txt=txt+res.asText()

		txt=txt+"World: <br>"
		txt=txt+" id | archipel1 | archipel2 <br>"
		res=self._pool +Command(SQL.selectAllWorld, False) 
		txt=txt+res.asText()

		txt=txt+"PNJ: <br>"
		txt=txt+" nom | ile | level | fruit | qualite | phrase | droprate <br>"
		res=self._pool +Command(SQL.selectAllPNJ, False) 
		txt=txt+res.asText()

		txt=txt+"Ile: <br>"
		txt=txt+" nom | archipel | pvp <br>"
		res=self._pool +Command(SQL.selectAllIle, False) 
		txt=txt+res.asText()

		txt=txt+"Archipel: <br>"
		txt=txt+" nom | ilePrincipale <br>"
		res=self._pool +Command(SQL.selectAllArchipel, False) 
		txt=txt+res.asText()

		return txt
		# TODO maybe add an input to execute requests?
		# TODO add a security before that route and... the other one...