imported=False
try:
	import mariadb
	imported=True
except:
	pass

from statsPirate import StatsPirate



class Static:
	def __new__(cls):
		raise TypeError('Static classes cannot be instantiated')


class InteractBDD(Static):

	config = {
	    'host': 'mariadb-anog-service',
	    'port': 3306,
	    'user': 'root',
	    'password': 'pwd',
	    'database': 'data'
	}

	if imported:


		#___________________________GAMES_____________________________


		@staticmethod
		def createGame(username):
			[conn, cur]=InteractBDD.beginQuery()

			gameid=InteractBDD.maxGameID()+1
			request= "INSERT INTO `games` (`gameid`, `username`, `encours`) VALUES ("+str(gameid)+", '"+username+"', 1);"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			
			InteractBDD.endQuery(conn, cur)
			return gameid

		@staticmethod
		def addUser(username, gameid):

			if InteractBDD.gameExists(gameid):
				
				[conn, cur]=InteractBDD.beginQuery()

				request= "SELECT encours, username FROM games WHERE gameid="+str(gameid)+";"
				description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
				for elem in description:
					if int(elem[0])==0:
						InteractBDD.endQuery(conn, cur) # si la partie est finie on peut pas la join
						return False
					if str(elem[1])==username:
						InteractBDD.endQuery(conn, cur) # si le joueur est déjà dans la partie il peut pas la rerejoindre
						return False

				# on le rajoute aux joueurs
				request= "INSERT INTO `games` (`gameid`, `username`, `encours`) VALUES ("+str(gameid)+", '"+username+"', 1);"
				InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
				InteractBDD.endQuery(conn, cur)
				return True
			else: # partie existe pas
				gameid=InteractBDD.createGame(username)
				return gameid
			

			

		@staticmethod
		def gamesInProgress(username):
			[conn, cur]=InteractBDD.beginQuery()

			gamesid=[]
			request= "SELECT gameid FROM games WHERE username='"+username+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				gamesid.append(int(elem[0]))


			InteractBDD.endQuery(conn, cur)
			return gamesid	


		@staticmethod
		def gameExists(gameid):
			[conn, cur]=InteractBDD.beginQuery()

			request= "SELECT gameid FROM games WHERE gameid="+str(gameid)+";"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				if gameid==int(elem[0]):
					InteractBDD.endQuery(conn, cur)
					return True
			InteractBDD.endQuery(conn, cur)
			return False

		@staticmethod
		def maxGameID():
			[conn, cur]=InteractBDD.beginQuery()

			gameid=-1
			request = "SELECT max(gameid) FROM games;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				try: 
					gameid=int(elem[0])
				except:
					pass

			InteractBDD.endQuery(conn, cur)
			return gameid



		#___________________________CREDENTIALS_______________________

		@staticmethod
		def existInDB(username):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT username FROM joueur WHERE username='"+username+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			
			for elem in description:
				if str(elem[0])==username:
					InteractBDD.endQuery(conn, cur)
					return True
			InteractBDD.endQuery(conn, cur)
			return False


		@staticmethod
		def createUser(username, password):
			[conn, cur]=InteractBDD.beginQuery()
			request = "INSERT INTO `joueur` (`username`, `password`, `currentstep`) VALUES('"+username+"','"+password+"', 1);"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			InteractBDD.endQuery(conn, cur)
			return None


		@staticmethod
		def checkPassword(username, password):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT password FROM joueur WHERE username='"+username+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)

			for elem in description:
				if str(elem[0])==password:
					InteractBDD.endQuery(conn, cur)
					return True
			InteractBDD.endQuery(conn, cur)
			return False


		#_________________________GET___________________________

		@staticmethod
		def getID(username):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT id FROM joueur WHERE username='"+str(username)+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			
			for elem in description:
				id = elem[0]
				InteractBDD.endQuery(conn, cur)
				return id
			InteractBDD.endQuery(conn, cur)
			return None

		@staticmethod
		def getUsername(id):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT username FROM joueur WHERE id='"+str(id)+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			
			for elem in description:
				username = elem[0]
				InteractBDD.endQuery(conn, cur)
				return username
			InteractBDD.endQuery(conn, cur)
			return "None"



		@staticmethod
		def getMyCrew(username):
			[conn, cur]=InteractBDD.beginQuery()
			pirates=[]
			request = "SELECT name, level, fruit, qualite FROM pirate WHERE username='"+username+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				txt=InteractBDD.pirateTXT(elem, 'Pirate')
				pirates.append(txt) #pas besoin de separation avec une ',', il n'y en a qu'un avec cet id
			InteractBDD.endQuery(conn, cur)
			return pirates

		@staticmethod
		def getMyPirate(id):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT name, level, fruit, qualite FROM pirate WHERE id='"+str(id)+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				txt=InteractBDD.pirateTXT(elem, 'Pirate')
			InteractBDD.endQuery(conn, cur)
			return txt


		@staticmethod
		def getMyCrewsID(username):
			[conn, cur]=InteractBDD.beginQuery()
			pirates=[]
			request = "SELECT id FROM pirate WHERE username='"+username+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				id=int(elem[0])
				pirates.append(id) #pas besoin de separation avec une ',', il n'y en a qu'un avec cet id
			InteractBDD.endQuery(conn, cur)
			return pirates

			

		@staticmethod
		def getMyCrewMinLevel(username):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT MIN(level) FROM pirate WHERE username='"+username+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				lvl=int(elem[0])
				InteractBDD.endQuery(conn, cur)
				return lvl
			return 1


		@staticmethod
		def getMyLocation(username):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT position FROM island WHERE username='"+username+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				value = str(elem[0])
				InteractBDD.endQuery(conn, cur)
				return value
			InteractBDD.endQuery(conn, cur)
			return ""

		@staticmethod
		def getMyCurrentStep(username):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT currentstep FROM joueur WHERE username='"+username+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				value = int(elem[0])
				InteractBDD.endQuery(conn, cur)
				return value
			InteractBDD.endQuery(conn, cur)
			return 1
			
		@staticmethod
		def retrieveWholeDatabase():
			[conn, cur]=InteractBDD.beginQuery()
			txt=""

			
			txt=txt+"Games: <br>"
			txt=txt+"id | gameid | username | encours <br>"
			request = "select * from games;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				txt= txt+"| " + str(elem[0])
				txt= txt+"| " + str(elem[1])
				txt= txt+"| " + str(elem[2])
				txt= txt+"| " + str(elem[3])
				txt=txt+"<br>"
			txt=txt+"<br>"
			
			'''
			[conn2, cur2]=InteractBDD.beginQuery()
			txt=txt+"TEEEEEEEEEEEEST: <br>"
			request = "select fruit from pnj;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				power=InteractBDD.fruitsPower(str(elem[0])) 
				txt=txt+str(power)				
				txt=txt+"<br>"
			txt=txt+"<br>"
			InteractBDD.endQuery(conn2, cur2)'''

			txt=txt+"Joueur: <br>"
			txt=txt+"id | username | password | currentStep <br>"
			request = "select * from joueur;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				txt= txt+"| " + str(elem[0])
				txt= txt+"| " + str(elem[1])
				txt= txt+"| " + "Not Displayable"
				txt= txt+"| " + str(elem[3])
				txt=txt+"<br>"
			txt=txt+"<br>"

			txt=txt+"island: <br>"
			txt=txt+"username | position's name <br>"
			request = "select * from island;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				for i in range(len(elem)):
					txt= txt+"| " + str(elem[i])
				txt=txt+"<br>"
			txt=txt+"<br>"

			txt=txt+"Pirate: <br>"
			txt=txt+" id | owner | name | level | fruit's name | qualite <br>"
			request = "select * from pirate;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				for i in range(len(elem)):
					txt= txt+" | " + str(elem[i])
				txt=txt+"<br>"
			txt=txt+"<br>"

			txt=txt+"Fruit: <br>"
			txt=txt+" name | power | allocated <br>"
			request = "select * from fruit;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				for i in range(len(elem)):
					txt= txt+" | " + str(elem[i])
				txt=txt+"<br>"
			txt=txt+"<br>"

			txt=txt+"World: <br>"
			txt=txt+" id | archipel1 | archipel2 <br>"
			request = "select * from world;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				for i in range(len(elem)):
					txt= txt+" | " + str(elem[i])
				txt=txt+"<br>"
			txt=txt+"<br>"

			txt=txt+"PNJ: <br>"
			txt=txt+" nom | ile | level | fruit | qualite | phrase<br>"
			request = "select * from pnj;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				for i in range(len(elem)):
					txt= txt+" | " + str(elem[i])
				txt=txt+"<br>"
			txt=txt+"<br>"

			txt=txt+"Ile: <br>"
			txt=txt+" nom | archipel | pvp <br>"
			request = "select * from ile;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				for i in range(len(elem)):
					txt= txt+" | " + str(elem[i])
				txt=txt+"<br>"
			txt=txt+"<br>"

			txt=txt+"Archipel: <br>"
			txt=txt+" nom | ilePrincipale <br>"
			request = "select * from archipel;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				for i in range(len(elem)):
					txt= txt+" | " + str(elem[i])
				txt=txt+"<br>"
			txt=txt+"<br>"

			InteractBDD.endQuery(conn, cur)
			return txt
			# TODO maybe add an input to execute requests?
			# TODO add a security before that route and... the other one...


		@staticmethod
		def checkPlayer(islandName):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT username FROM island WHERE position='"+islandName+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				value = str(elem[0])
				InteractBDD.endQuery(conn, cur)
				return value
			InteractBDD.endQuery(conn, cur)
			return None


		@staticmethod
		def averagePirateLevel(username):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT level FROM pirate WHERE username='"+username+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			
			levels=[]
			for elem in description:
				levels.append(int(elem[0]))

			InteractBDD.endQuery(conn, cur)
			return sum(levels)/len(levels)

		@staticmethod
		def checkBoss(currentIslandName):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT nom, level, fruit, qualite FROM pnj WHERE ile='"+currentIslandName+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			txt=""
			for elem in description:
				txt=InteractBDD.pirateTXT(elem, 'Legende')
				InteractBDD.endQuery(conn, cur)
				return txt
			return None

			
		@staticmethod
		def phraseDeCombat(pnjName):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT phrase FROM pnj WHERE nom='"+pnjName+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				texte=str(elem[0])
				InteractBDD.endQuery(conn, cur)
				return texte

			InteractBDD.endQuery(conn, cur)
			return "attaque"


			
		@staticmethod
		def getDrop(currentIslandName, username):
			[conn, cur]=InteractBDD.beginQuery()


			request = "SELECT perc FROM pnj WHERE ile='"+currentIslandName+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			drop=0
			for elem in description:
				drop = int(elem[0])
				if drop==0:
					return None

			request = "SELECT nom, level, fruit, qualite FROM pnj WHERE ile='"+currentIslandName+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			txt=""
			for elem in description:
				bossName=str(elem[0])
				has=InteractBDD.hasThatBoss(bossName, username)
				if has:
					InteractBDD.endQuery(conn, cur)
					return None

				txt=InteractBDD.pirateTXT(elem, 'Legende')
				InteractBDD.endQuery(conn, cur)
				return [txt, drop]
			return None


		@staticmethod
		def hasThatBoss(bossName, username):
			[conn, cur]=InteractBDD.beginQuery()

			request = "SELECT name FROM pirate WHERE username='"+username+"' and name='"+bossName+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				InteractBDD.endQuery(conn, cur)
				return True
			
			InteractBDD.endQuery(conn, cur)
			return False


		#_____________________STORE_______________________________

		@staticmethod
		def setMyCrew(username, positionsName, pirates, currentstep):
			[conn, cur]=InteractBDD.beginQuery()

			for pirate in pirates:
				request = "INSERT INTO `pirate` (`username`, `name`, `level`, `fruit`, `qualite`) VALUES ('"+username+"','"+pirate.name+"','"+str(pirate.level)+"','"+pirate.fruit.name+"','"+str(pirate.qualite)+"');"
				InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			# TODO not a problem to not allocate fruits? 
			request = "UPDATE island SET position='"+positionsName+"' WHERE username='"+username+"';"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			request = "UPDATE joueur SET currentstep="+str(currentstep)+" WHERE username='"+username+"';"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			InteractBDD.endQuery(conn, cur)
			return None
		
		@staticmethod
		def setMyLocation(username, positionsName):
			[conn, cur]=InteractBDD.beginQuery()
			request = "DELETE FROM island WHERE username='"+username+"';" # an update doesnt do the work since u r maybe not already in the table
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			request = "INSERT INTO island VALUES ('"+username+"', '"+positionsName+"');"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			InteractBDD.endQuery(conn, cur)
			return None

			

		@staticmethod
		def setMyCurrentStep(username, currentStep):
			[conn, cur]=InteractBDD.beginQuery()
			request = "UPDATE joueur SET currentstep='"+str(currentStep)+"' WHERE username='"+username+"';"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			InteractBDD.endQuery(conn, cur)
			return None

		@staticmethod
		def addNewFighter(username, pirate):
			[conn, cur]=InteractBDD.beginQuery() # TODO not a problem to not allocate fruits? 
			request = "INSERT INTO `pirate` (`username`, `name`, `level`, `fruit`, `qualite`) VALUES ('"+username+"','"+pirate.name+"','"+str(pirate.level)+"','"+pirate.fruit.name+"','"+str(pirate.qualite)+"');"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			InteractBDD.endQuery(conn, cur)
			return None


		@staticmethod
		def increasePirateLevel(username):
			[conn, cur]=InteractBDD.beginQuery()

			request = "UPDATE pirate SET level=level+1 WHERE username='"+username+"' and fruit='None';"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			request = "UPDATE pirate SET level=level+3 WHERE username='"+username+"' and fruit!='None';"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			InteractBDD.endQuery(conn, cur)
			return None


		#_________________________FRUITS_________________________________


		@staticmethod
		def countAvailableFruits():
			[conn, cur]=InteractBDD.beginQuery()

			InteractBDD.checkAllocatedFruits()

			request = "SELECT COUNT(*) FROM fruit WHERE allocated='0';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				value=int(elem[0])
			
			InteractBDD.endQuery(conn, cur)
			return value


		@staticmethod
		def checkAllocatedFruits():
			[conn, cur]=InteractBDD.beginQuery()

			request = "UPDATE fruit SET allocated=0;"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)


			request = "SELECT fruit FROM pirate;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			
			[conn2, cur2]=InteractBDD.beginQuery()
			for elem in description:
				fruitsName=str(elem[0])
				request = "UPDATE fruit SET allocated=1 WHERE name='"+fruitsName+"';"
				InteractBDD.connectAndExecuteRequest(request, True, conn2, cur2)

			
			
			InteractBDD.endQuery(conn2, cur2)
			InteractBDD.endQuery(conn, cur)
			return None



		@staticmethod
		def notAllocatedFruits():
			[conn, cur]=InteractBDD.beginQuery()

			fruits=[]
			request = "SELECT name FROM fruit WHERE allocated=0;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				fruits.append(str(elem[0]))
			
			InteractBDD.endQuery(conn, cur)
			return fruits


		@staticmethod
		def fruitsPower(fruitsName):
			if fruitsName=='None':
				return [0,0,0,0]

			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT power FROM fruit WHERE name='"+str(fruitsName)+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			power=""
			for elem in description:
				strpower=str(elem[0])
				power=list(map(int, strpower.split(",") )) # [1,2,3,4]
				InteractBDD.endQuery(conn, cur)
				return power
			return [0,0,0,0] # something went wrong

		@staticmethod
		def allocateFruit(fruitsName):
			[conn, cur]=InteractBDD.beginQuery()

			request = "UPDATE fruit SET allocated=1 WHERE name='"+str(fruitsName)+"';"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			
			InteractBDD.endQuery(conn, cur)
			return None



		#_________________________WORLD_________________________________

		@staticmethod
		def availableIslandsInCurrentArchipel(currentIslandName):
			[conn, cur]=InteractBDD.beginQuery()

			currentArchipelName=InteractBDD.getArchipelFromIle(currentIslandName)

			islandNames=[]
			# and we must also get all the islands inside the current archipel
			request = "SELECT nom FROM ile WHERE archipel='"+currentArchipelName+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				if str(elem[0])!=currentIslandName:
					islandNames.append(str(elem[0])) 


			InteractBDD.endQuery(conn, cur)
			return islandNames


		@staticmethod
		def availableIslandsInAvailableArchipels(currentIslandName):
			connectedArchipels=InteractBDD.availableArchipels(currentIslandName)

			islandNames=[]
			for archipel in connectedArchipels:
				islandNames.append(InteractBDD.ilePrincipale(archipel)) 

			return islandNames


		@staticmethod
		def getArchipelFromIle(currentIslandName):
			[conn, cur]=InteractBDD.beginQuery()

			request = "SELECT archipel FROM ile WHERE nom='"+currentIslandName+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				currentArchipelName = str(elem[0]) # we got the name of the current archipel
				InteractBDD.endQuery(conn, cur)
				return currentArchipelName
			InteractBDD.endQuery(conn, cur)
			return currentIslandName # something went wrong


		@staticmethod
		def getConnectedArchipels(currentArchipelName):
			[conn, cur]=InteractBDD.beginQuery()
			connectedArchipels=[]
			request = "SELECT archipel1, archipel2 FROM world WHERE archipel1='"+currentArchipelName+"' OR archipel2='"+currentArchipelName+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				if str(elem[0])!=currentArchipelName:
					connectedArchipels.append(str(elem[0])) 
				if str(elem[1])!=currentArchipelName:
					connectedArchipels.append(str(elem[1])) 

			InteractBDD.endQuery(conn, cur)
			return connectedArchipels

		@staticmethod
		def availableArchipels(currentIslandName):
			currentArchipelName=InteractBDD.getArchipelFromIle(currentIslandName)
			connectedArchipels=InteractBDD.getConnectedArchipels(currentArchipelName)
			return connectedArchipels	
			
		@staticmethod
		def ilePrincipale(archipel):
			[conn, cur]=InteractBDD.beginQuery()

			request = "SELECT ileprincipale FROM archipel WHERE nom='"+archipel+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				ileprincipale = str(elem[0]) # we got the name of the current archipel
				InteractBDD.endQuery(conn, cur)
				return ileprincipale
			InteractBDD.endQuery(conn, cur)
			return archipel # something went wrong


		#_________________________DELETE_________________________________


		@staticmethod
		def deleteUserProgress(username):

			[conn, cur]=InteractBDD.beginQuery()

			request = "DELETE FROM island WHERE username='"+username+"';"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			
			[conn2, cur2]=InteractBDD.beginQuery()
			request = "SELECT fruit FROM pirate WHERE username='"+username+"' AND name NOT IN (SELECT nom FROM pnj);"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				fruitsName=str(elem[0]) # we got the name of the current archipel
				request = "UPDATE fruit SET allocated=0 WHERE name='"+str(fruitsName)+"';"
				InteractBDD.connectAndExecuteRequest(request, True, conn2, cur2)
			InteractBDD.endQuery(conn2, cur2)

			request = "DELETE FROM pirate WHERE username='"+username+"' AND name NOT IN (SELECT nom FROM pnj);"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur) 

			request = "UPDATE pirate SET level=1 WHERE username='"+username+"';"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur) 

			InteractBDD.endQuery(conn, cur)
			return None

		@staticmethod
		def deletePirates(username):

			[conn, cur]=InteractBDD.beginQuery()
			
			[conn2, cur2]=InteractBDD.beginQuery()
			request = "SELECT fruit FROM pirate WHERE username='"+username+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				fruitsName=str(elem[0]) # we got the name of the current archipel
				request = "UPDATE fruit SET allocated=0 WHERE name='"+str(fruitsName)+"';"
				InteractBDD.connectAndExecuteRequest(request, True, conn2, cur2)
			InteractBDD.endQuery(conn2, cur2)

			request = "DELETE FROM pirate WHERE username='"+username+"';"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			InteractBDD.endQuery(conn, cur)
			return None

		@staticmethod
		def deallocateFruitsFromCrew(obj):
			if obj.isinstance()=="Joueur":
				crew=obj.equipage
			else: #equipage
				crew=obj

			[conn2, cur2]=InteractBDD.beginQuery()
			for pirate in crew.team:
				if pirate.fruit.name!="None":
					request = "UPDATE fruit SET allocated=0 WHERE name='"+str(pirate.fruit.name)+"';"
					InteractBDD.connectAndExecuteRequest(request, True, conn2, cur2)
			InteractBDD.endQuery(conn2, cur2)
			return None	


		@staticmethod
		def deleteAll():
			[conn, cur]=InteractBDD.beginQuery()
			request = "DELETE FROM island;"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			request = "DELETE FROM joueur;"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur) # TODO faudra sans doute supprimer un fichier de config avec les utilisateurs
			request = "DELETE FROM pirate;"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			request = "INSERT INTO `joueur` (`username`, `password`, `currentstep`) VALUES ('None', 'None', 1);"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			InteractBDD.endQuery(conn, cur)
			return None


		@staticmethod
		def removeFighter(username, pirate):
			[conn, cur]=InteractBDD.beginQuery()

			boss=False
			request = "SELECT nom FROM pnj WHERE nom='"+pirate.name+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				boss=True

			if boss:
				
				request = "UPDATE pirate SET level=level-10 WHERE username='"+username+"' AND name='"+pirate.name+"' AND level>10;"
				InteractBDD.connectAndExecuteRequest(request, True, conn, cur) 

				InteractBDD.endQuery(conn, cur)
				return None

			else:

				fruitsName=pirate.fruit.name
				if fruitsName!="None":
					request = "UPDATE fruit SET allocated=0 WHERE name='"+fruitsName+"';"
					InteractBDD.connectAndExecuteRequest(request, True, conn, cur)


				request = "DELETE FROM pirate WHERE username='"+username+"' and name='"+pirate.name+"' and fruit='"+pirate.fruit.name+"' and qualite='"+str(pirate.qualite)+"';"
				InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

				InteractBDD.endQuery(conn, cur)
				return None


		#____________________________________________________________
		
		@staticmethod
		def connectAndExecuteRequest(request, needCommit, conn, cur):
			#conn = mariadb.connect(**InteractBDD.config)
			#cur = conn.cursor()
			if needCommit:
				try:
					cur.execute(request)
					conn.commit()
				except:
					conn.rollback()
			else:
				cur.execute(request)

			description=cur
			#cur.close()
			#conn.close()
			return description

		@staticmethod
		def beginQuery():
			conn = mariadb.connect(**InteractBDD.config)
			cur = conn.cursor()
			return [conn, cur]

		@staticmethod
		def endQuery(conn, cur):
			cur.close()
			conn.close()
			
		@staticmethod
		def pirateTXT(elem, cls):
			piratesName=elem[0]
			level=elem[1]
			fruitsName=elem[2]
			qualite=elem[3]

			boss=False
			if cls=="Legende":
				boss=True

			power=InteractBDD.fruitsPower(fruitsName)
			#fruitsTXT='{"type": "FruitDemon", "name": \"'+fruitsName+'\", "power": \"'+str(power)+'\"}'
			#fruitsTXT="{"+"\"type\": \"FruitDemon\", \"name\": \"{}\", \"power\": \"{}\"".format(fruitsName, str(power)) + "}"
			fruitsTXT='{"type": "FruitDemon", "name": "%s", "power": %s, "boss": "%s"}' % (fruitsName, str(power), str(boss)) 
			#txt='{"type": "'+type+'", "name": \"'+piratesName+'\", "level": \"'+str(level)+ '\", "qualite": \"'+str(qualite)+'\", "fruit": \"'+ fruitsTXT+'\", "stats": \"'+str(StatsPirate.generateStats(level, qualite, power))+'\", "availableToFight": "True", "mort": "False"}'
			#txt="{"+ '\"type": "{}", "name": "{}", "level": "{}", "qualite": "{}", "fruit": "{}", "stats": "{}", "availableToFight": "True", "mort": "False\"'.format(type, piratesName, str(level), str(qualite), fruitsTXT, str(StatsPirate.generateStats(level, qualite, power)) ) +"}"
			txt='{"type": "%s", "name": "%s", "level": %s, "qualite": %s, "fruit": %s, "stats": "%s", "availableToFight": "True", "mort": "False"}' % (cls, piratesName, str(level), str(qualite), fruitsTXT, str(StatsPirate.generateStats(level, qualite, power)) )
			return txt





	else:

		currentStep=1

		crewLevel=100
		crewQuality=1
		crewFruit="GumGum"
		crewNumber=1

		username="Beefr"
		location="Amazon Lily"

		@staticmethod
		def countAvailableFruits():
			return 0

		@staticmethod
		def allocateFruit(cool):
			return None

		@staticmethod
		def fruitsPower(fruit):
			if fruit=="None":
				fruitPower=[0,0,0,0]
			else:
				fruitPower=[50,50,0,0]
			return fruitPower

		@staticmethod
		def getMyCrew(cool):
			level=InteractBDD.crewLevel
			qualite=InteractBDD.crewQuality
			fruit=InteractBDD.crewFruit
			if fruit=="None":
				fruitPower=[0,0,0,0]
			else:
				fruitPower=[50,50,0,0]

			pirates=[]
			for i in range(InteractBDD.crewNumber):
				fruitTXT = '{"type": "FruitDemon", "name": "%s", "power": %s, "boss": "False"}' % (fruit, str(fruitPower)) 
				pirateTXT='{"type": "Pirate", "name": "%s", "level": %s, "qualite": %s, "fruit": %s, "stats": "%s", "availableToFight": "True", "mort": "False"}' % (InteractBDD.username+str(i), str(level), str(qualite), fruitTXT, str(StatsPirate.generateStats(level, qualite, fruitPower)))
				pirates.append(pirateTXT)
				#print(pirateTXT)
			return pirates


		@staticmethod
		def getMyLocation(cool):
			return InteractBDD.location


		@staticmethod
		def phraseDeCombat(cool):
			return "attaque"

		@staticmethod
		def increasePirateLevel(cool):
			return None


		@staticmethod
		def getMyCurrentStep(cool):
			return InteractBDD.currentStep


		@staticmethod
		def availableIslandsInCurrentArchipel(cool):
			return ["Impel Down"]

		@staticmethod
		def availableArchipels(cool):
			return ["Impel Down"]


		@staticmethod
		def ilePrincipale(cool):
			return "Impel Down"

		@staticmethod
		def checkPlayer(cool):
			return None

		@staticmethod
		def setMyLocation(cool, cool2):
			return None

		@staticmethod
		def averagePirateLevel(cool):
			return InteractBDD.crewLevel

		@staticmethod
		def checkBoss(cool):
			return None

		@staticmethod
		def removeFighter(cool, cool2):
			return None

		@staticmethod
		def deleteUserProgress(cool):
			return None


		@staticmethod
		def setMyCrew(cool, cool2, cool3, cool4):
			return None


		@staticmethod
		def setMyCurrentStep(cool, cool2):
			return None


		@staticmethod
		def deletePirates(cool):
			return None


		@staticmethod
		def getMyCrewMinLevel(cool):
			return InteractBDD.crewLevel


		@staticmethod
		def addNewFighter(cool, cool2):
			return None


		@staticmethod
		def availableIslandsInAvailableArchipels(cool):
			return ["Impel Down"]


		@staticmethod
		def deallocateFruitsFromCrew(cool):
			return None


		@staticmethod
		def getDrop(cool, cool2):
			fruitTXT = '{"type": "FruitDemon", "name": "%s", "power": %s, "boss": "True"}' % ("Lave", str([100,0,0,0])) 
			pirateTXT='{"type": "Legende", "name": "%s", "level": %s, "qualite": %s, "fruit": %s, "stats": "%s", "availableToFight": "True", "mort": "False"}' % ("Akainu", 30, 1, fruitTXT, str(StatsPirate.generateStats(30, 1, [100,0,0,0])))
			return [pirateTXT, 50]





