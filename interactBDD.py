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
	    request = "SELECT username FROM joueur WHERE username='"+username+"';"
	    description = InteractBDD.connectAndExecuteRequest(request, False)
	    
	    for elem in description:
	    	if str(elem[0])==username:
	    		return True
	    return False


	@staticmethod
	def createUser(username, password):
		request = "INSERT INTO joueur VALUES('"+username+"','"+password+"');"
		description = InteractBDD.connectAndExecuteRequest(request, True)
		return None


	@staticmethod
	def checkPassword(username, password):
		request = "SELECT password FROM joueur WHERE username='"+username+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False)

		for elem in description:
			if str(elem[0])==password:
				return True
		return False


	#_________________________GET___________________________

	@staticmethod
	def getMyCrew(username):
		piratesid=InteractBDD.getMyPiratesID(username)
		if len(piratesid)==0:
			return ""

		pirates=[]
		for pirateid in piratesid:
			request = "SELECT * FROM pirate WHERE id='"+str(pirateid)+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False)
			for elem in description:
				level=elem[2]
				qualite=elem[4]
				fruit=FruitFactory.giveThatFruit(str(elem[3]))
				txt='{"type": "Pirate", "name": \"'+str(elem[1])+'\", "level": '+str(level)+ ', "qualite": '+str(qualite)+', "fruit": '+ str(fruit)+', "stats": '+str(StatsPirate.generateStats(level, qualite, fruit.power))+', "availableToFight": "True", "mort": "False"}'
				pirates.append(txt) #pas besoin de separation avec une ',', il n'y en a qu'un avec cet id
		return pirates



	@staticmethod
	def getMyPiratesID(username):
		request = "SELECT piratesid FROM equipage WHERE username='"+username+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False)

		for elem in description:
			return str(elem[0]).split(",")

		return []



	@staticmethod
	def getMyLocation(username):
		request = "SELECT position FROM equipage WHERE username='"+username+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		for elem in description:
			return str(elem[0])


	@staticmethod
	def retrieveWholeDatabase():
		txt=""

		txt=txt+"Joueur: <br>"
		txt=txt+"username | password <br>"
		request = "select * from joueur;"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		for elem in description:
			for i in range(len(elem)):
				txt= txt+"| " + str(elem[i])
			txt=txt+"<br>"
		txt=txt+"<br>"

		txt=txt+"Equipage: <br>"
		txt=txt+"username | position's name | pirate's id <br>"
		request = "select * from equipage;"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		for elem in description:
			for i in range(len(elem)):
				txt= txt+"| " + str(elem[i])
			txt=txt+"<br>"
		txt=txt+"<br>"

		txt=txt+"Pirate: <br>"
		txt=txt+"id | name | level | fruit's name | qualite <br>"
		request = "select * from pirate;"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		for elem in description:
			for i in range(len(elem)):
				txt= txt+" | " + str(elem[i])
			txt=txt+"<br>"
		txt=txt+"<br>"

		return txt
		# TODO maybe add an input to execute requests?


	@staticmethod
	def getPirateID(pirate):
		# level='"+str(pirate.level)+"' AND
		request = "SELECT id FROM pirate WHERE name='"+pirate.name+"' AND qualite='"+str(pirate.qualite)+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		for elem in description:
			return str(elem[0])


	@staticmethod
	def checkPlayer(islandName):
		request = "SELECT username FROM equipage WHERE position='"+islandName+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		for elem in description:
			return str(elem[0])
		return None


	#_____________________STORE_______________________________

	@staticmethod
	def setMyCrew(username, positionsName, pirates):
		indexes=""
		for pirate in pirates:
			index=InteractBDD.getAvailableID()
			if not indexes:
				indexes=str(index)
			else:
				indexes=indexes+","+str(index)
			request = "INSERT INTO pirate VALUES('"+str(index)+"','"+pirate.name+"','"+str(pirate.level)+"','"+pirate.fruit.name+"','"+str(pirate.qualite)+"');"
			description = InteractBDD.connectAndExecuteRequest(request, True)


		request = "DELETE FROM equipage WHERE username='"+username+"';"
		description = InteractBDD.connectAndExecuteRequest(request, True)


		request = "INSERT INTO equipage VALUES('"+username+"','"+positionsName+"','"+indexes+"');"
		description = InteractBDD.connectAndExecuteRequest(request, True)
		return None
	
	@staticmethod
	def setMyLocation(username, positionsName):
		request = "UPDATE equipage SET position='"+positionsName+"' WHERE username='"+username+"';"
		description = InteractBDD.connectAndExecuteRequest(request, True)
		return None

	@staticmethod
	def addNewFighter(username, pirate):
		newid=InteractBDD.getAvailableID()
		request = "SELECT piratesid FROM equipage WHERE username='"+username+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		for elem in description:
			piratesid=str(elem[0])
		piratesid=piratesid+","+str(newid)
		request = "UPDATE equipage SET piratesid='"+piratesid+"' WHERE username='"+username+"';"
		description = InteractBDD.connectAndExecuteRequest(request, True)

		request = "INSERT INTO pirate VALUES('"+str(newid)+"','"+pirate.name+"','"+str(pirate.level)+"','"+pirate.fruit.name+"','"+str(pirate.qualite)+"');"
		description = InteractBDD.connectAndExecuteRequest(request, True)
		return None


	@staticmethod
	def increasePirateLevel(pirate, increase):
		pirateid=InteractBDD.getPirateID(pirate)

		request = "SELECT level FROM pirate WHERE id='"+str(pirateid)+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		for elem in description:
			level=int(elem[0])+increase

		request = "UPDATE pirate SET level='"+str(level)+"' WHERE id='"+str(pirateid)+"';"
		description = InteractBDD.connectAndExecuteRequest(request, True)
		return level


	#_________________________DELETE_________________________________


	@staticmethod
	def deleteUserProgress(username):

		request = "DELETE FROM equipage WHERE username='"+username+"';"
		description = InteractBDD.connectAndExecuteRequest(request, True)

		#request = "DELETE FROM joueur WHERE username='"+username+"';"
		#description = InteractBDD.connectAndExecuteRequest(request, True)

		piratesid=InteractBDD.getMyPiratesID(username)
		for pirateid in piratesid:
			request = "DELETE FROM pirate WHERE id='"+str(pirateid)+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False) # TODO remove allocated fruits
		return None


	@staticmethod
	def deleteAll():
		request = "DELETE FROM equipage;"
		description = InteractBDD.connectAndExecuteRequest(request, True)
		request = "DELETE FROM joueur;"
		description = InteractBDD.connectAndExecuteRequest(request, True)
		request = "DELETE FROM pirate;"
		description = InteractBDD.connectAndExecuteRequest(request, True)
		return None


	@staticmethod
	def removeFighter(username, pirate):
		pirateid=InteractBDD.getPirateID(pirate)

		request = "DELETE FROM pirate WHERE id='"+str(pirateid)+"';"
		description = InteractBDD.connectAndExecuteRequest(request, True)

		request = "SELECT piratesid FROM equipage WHERE username='"+username+"';"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		piratesid=""
		for elem in description:
			piratesid=str(elem[0])
		newid=InteractBDD.removeFromString(piratesid, pirateid)
		request = "UPDATE equipage SET piratesid='"+newid+"' WHERE username='"+username+"';"
		description = InteractBDD.connectAndExecuteRequest(request, True)
		return None

	@staticmethod
	def cleanUpDB():
		piratesid=[]
		request = "SELECT piratesid FROM equipage;"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		for elem in description:
			array=str(elem[0]).split(",")
			piratesid.append(array) #we get all the pirates id that belong to a crew

		pid=[]
		request = "SELECT id FROM pirate;"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		for elem in description:
			array=str(elem[0]).split(",")
			pid.append(array) #we get all the pirates id that exist in the db

		for pirate in pid: #for each existing pirate(id) in db
			if pirate not in piratesid: # if it is in a crew it's fine, otherwise we delete it from db
				request = "DELETE FROM pirate WHERE id='"+str(pirate)+"';"
				description = InteractBDD.connectAndExecuteRequest(request, True)
		return None
		


	#____________________________________________________________
	
	@staticmethod
	def connectAndExecuteRequest(request, needCommit):
		conn = mariadb.connect(**InteractBDD.config)
		cur = conn.cursor()
		if needCommit:
			try:
				cur.execute(request)
				conn.commit()
			except:
				conn.rollback()
		else:
			cur.execute(request)

		description=cur
		conn.close
		return description



	@staticmethod
	def getAvailableID():
		index=0
		temp=-1
		request="SELECT id FROM pirate WHERE id="+str(index)+";"
		description = InteractBDD.connectAndExecuteRequest(request, False)
		for elem in description:
			temp=elem[0]
		while temp==index:
			index+=1
			request="SELECT id FROM pirate WHERE id="+str(index)+";"
			description = InteractBDD.connectAndExecuteRequest(request, False)
			for elem in description:
				temp=elem[0]
		return index

	@staticmethod
	def removeFromString(string, elem):
		array=string.split(",")
		try:
			array.remove(elem)
		except:
			"TODO: ValueError: list.remove(x): x not in list"
		array=list(set(array))
		newString=','.join(array)
		return newString



