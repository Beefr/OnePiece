import mariadb

from fruitdemon import FruitFactory
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
			level=elem[1]
			qualite=elem[3]
			fruit=FruitFactory.giveThatFruit(str(elem[2]))
			txt='{"type": "Pirate", "name": \"'+str(elem[0])+'\", "level": '+str(level)+ ', "qualite": '+str(qualite)+', "fruit": '+ str(fruit)+', "stats": '+str(StatsPirate.generateStats(level, qualite, fruit.power))+', "availableToFight": "True", "mort": "False"}'
			pirates.append(txt) #pas besoin de separation avec une ',', il n'y en a qu'un avec cet id
		InteractBDD.endQuery(conn, cur)
		return pirates

	@staticmethod
	def getMyPirate(id):
		[conn, cur]=InteractBDD.beginQuery()
		request = "SELECT name, level, fruit, qualite FROM pirate WHERE id='"+str(id)+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
		for elem in description:
			level=elem[1]
			qualite=elem[3]
			fruit=FruitFactory.giveThatFruit(str(elem[2]))
			txt='{"type": "Pirate", "name": \"'+str(elem[0])+'\", "level": '+str(level)+ ', "qualite": '+str(qualite)+', "fruit": '+ str(fruit)+', "stats": '+str(StatsPirate.generateStats(level, qualite, fruit.power))+', "availableToFight": "True", "mort": "False"}'
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
		txt=txt+" owner | name | level | fruit's name | qualite <br>"
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
		for elem in description:
			level=elem[1]
			qualite=elem[3]
			fruit=FruitFactory.giveThatFruit(str(elem[2]))
			txt='{"type": "Legende", "name": \"'+str(elem[0])+'\", "level": '+str(level)+ ', "qualite": '+str(qualite)+', "fruit": '+ str(fruit)+', "stats": '+str(StatsPirate.generateStats(level, qualite, fruit.power))+', "availableToFight": "True", "mort": "False"}'
		InteractBDD.endQuery(conn, cur)
		return txt

		
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
		return "se déchaîne contre"


	#_____________________STORE_______________________________

	@staticmethod
	def setMyCrew(username, positionsName, pirates):
		[conn, cur]=InteractBDD.beginQuery()

		for pirate in pirates:
			request = "INSERT INTO `pirate` (`username`, `name`, `level`, `fruit`, `qualite`) VALUES ('"+username+"','"+pirate.name+"','"+str(pirate.level)+"','"+pirate.fruit.name+"','"+str(pirate.qualite)+"');"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

		request = "UPDATE island SET position='"+positionsName+"' WHERE username='"+username+"';"
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
		[conn, cur]=InteractBDD.beginQuery()
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


	#_________________________WORLD_________________________________

	@staticmethod
	def availableIslandsInCurrentArchipel(currentIslandName):
		[conn, cur]=InteractBDD.beginQuery()

		request = "SELECT archipel FROM ile WHERE nom='"+currentIslandName+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
		for elem in description:
			currentArchipelName = str(elem[0]) # we got the name of the current archipel

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

		[conn, cur]=InteractBDD.beginQuery()

		islandNames=[]
		
		for archipel in connectedArchipels:
			request = "SELECT ileprincipale FROM archipel WHERE nom='"+archipel+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				if str(elem[0])!=currentIslandName: 
					islandNames.append(str(elem[0])) 

		InteractBDD.endQuery(conn, cur)
		return islandNames


	@staticmethod
	def availableArchipels(currentIslandName):
		[conn, cur]=InteractBDD.beginQuery()

		request = "SELECT archipel FROM ile WHERE nom='"+currentIslandName+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
		for elem in description:
			currentArchipelName = str(elem[0]) # we got the name of the current archipel

		
		# we must get all the connected archipels to get their principal island
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
	def ilePrincipale(archipel):
		[conn, cur]=InteractBDD.beginQuery()

		request = "SELECT ileprincipale FROM archipel WHERE nom='"+archipel+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
		for elem in description:
			ileprincipale = str(elem[0]) # we got the name of the current archipel

		
		InteractBDD.endQuery(conn, cur)
		return ileprincipale



	#_________________________DELETE_________________________________


	@staticmethod
	def deleteUserProgress(username):

		[conn, cur]=InteractBDD.beginQuery()

		request = "DELETE FROM island WHERE username='"+username+"';"
		InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

		request = "DELETE FROM pirate WHERE username='"+username+"';"
		InteractBDD.connectAndExecuteRequest(request, True, conn, cur) # TODO remove allocated fruits

		InteractBDD.endQuery(conn, cur)
		return None

	@staticmethod
	def deletePirates(username):

		[conn, cur]=InteractBDD.beginQuery()

		request = "DELETE FROM pirate WHERE username='"+username+"';"
		InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

		InteractBDD.endQuery(conn, cur)
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
		
