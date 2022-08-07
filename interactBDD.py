imported=False
try:
	import mariadb
	imported=True
except:
	pass

from statsPirate import StatsPirate
import random

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


	fruits=["INSERT INTO fruit VALUES('GumGum','30,40,30,0', 0, {});",
			"INSERT INTO fruit VALUES('Feu','25,50,0,25', 0, {});",
			"INSERT INTO fruit VALUES('Ice','25,0,50,25', 0, {});",
			"INSERT INTO fruit VALUES('Homme','25,25,25,25', 0, {});",
			"INSERT INTO fruit VALUES('Conversion','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Allosaure','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Vieillissement','0,0,100,0', 0, {});",
			"INSERT INTO fruit VALUES('Chateau','25,25,25,25', 0, {});",
			"INSERT INTO fruit VALUES('Lumiere','0,50,50,0', 0, {});",
			"INSERT INTO fruit VALUES('Passion','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Poison','30,40,30,0', 0, {});",
			"INSERT INTO fruit VALUES('Hormones','100,0,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Lave','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Gaz','0,0,100,0', 0, {});",
			"INSERT INTO fruit VALUES('Gravite','25,25,25,25', 0, {});",
			"INSERT INTO fruit VALUES('Barriere','0,0,100,0', 0, {});",
			"INSERT INTO fruit VALUES('Mammouth','10,0,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Mochi','0,50,50,0', 0, {});",
			"INSERT INTO fruit VALUES('Fumee','0,50,50,0', 0, {});",
			"INSERT INTO fruit VALUES('Meteo','25,25,25,25', 0, {});",
			"INSERT INTO fruit VALUES('Sable','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Balistique','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Bouddha','30,40,30,0', 0, {});",
			"INSERT INTO fruit VALUES('Tremblement','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Phoenix','100,0,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Electricite','0,50,50,0', 0, {});",
			"INSERT INTO fruit VALUES('Glace','30,40,30,0', 0, {});",
			"INSERT INTO fruit VALUES('Guepard','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Ombre','100,0,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Bistouri','50,50,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Vaudou','25,25,25,25', 0, {});",
			"INSERT INTO fruit VALUES('Musique','25,25,25,25', 0, {});",
			"INSERT INTO fruit VALUES('Soul','100,0,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Dragon','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Yami','100,0,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Ressort','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Ferraille','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Coussinet','0,0,100,0', 0, {});",
			"INSERT INTO fruit VALUES('Eclosion','0,100,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Resurrection','100,0,0,0', 0, {});",
			"INSERT INTO fruit VALUES('Fragmentation','0,50,50,0', 0, {});"]

	if imported:


		#___________________________GAMES_____________________________


		@staticmethod
		def createGame(username):
			[conn, cur]=InteractBDD.beginQuery()

			gameid=InteractBDD.maxGameID()+1
			request= "INSERT INTO `games` (`gameid`, `username`, `encours`, `currentstep`) VALUES ("+str(gameid)+", '"+username+"', 1, 1);"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			
			for request in InteractBDD.fruits:
				request=request.format(str(gameid))
				InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			InteractBDD.endQuery(conn, cur)
			return gameid

		@staticmethod
		def addUser(username, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			result=True
			if InteractBDD.gameExists(gameid):
				count=0
				request= "SELECT encours, username FROM games WHERE gameid="+str(gameid)+";"
				description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
				for elem in description:
					count+=1
					if int(elem[0])==0:
						# si la partie est finie on peut pas la join
						result=False
					if str(elem[1])==username:
						# si le joueur est déjà dans la partie il peut pas la rerejoindre
						result=False

				if count<8 and result:
				# on le rajoute aux joueurs
					request= "INSERT INTO `games` (`gameid`, `username`, `encours`, `currentstep`) VALUES ("+str(gameid)+", '"+username+"', 1, 1);"
					InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

					InteractBDD.setMyLocation(username, InteractBDD.villeDeDepart(), gameid)
					
					fruitsname=InteractBDD.giveAFruit(gameid)
					request = "INSERT INTO `pirate` (`username`, `name`, `level`, `fruit`, `qualite`, `gameid`) VALUES ('"+username+"','"+username+"','"+str(1)+"','"+fruitsname+"','"+str(0)+"', "+str(gameid)+");"
					InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

					request = "UPDATE fruit SET allocated=1 WHERE gameid="+str(gameid)+" and name='"+fruitsname+"';"
					InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
				else: # plus de place pour jouer avec ses potes
					result=False

			else: # partie existe pas
				result=False
			InteractBDD.endQuery(conn, cur)
			return result
			
		@staticmethod
		def joinThatGameID(username, gameid):
			result=True
			[conn, cur]=InteractBDD.beginQuery()
			if InteractBDD.gameExists(gameid):
				

				count=0
				request= "SELECT encours, username FROM games WHERE gameid="+str(gameid)+";"
				description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
				for elem in description:
					count+=1
					if int(elem[0])==0:
						# si la partie est finie on peut pas la join
						result=False
					if str(elem[1])==username:
						# si le joueur est déjà dans la partie il peut pas la rerejoindre
						result=False

				if count>=8:
				# trop de joueurs
					result=False
				

			else: # partie existe pas
				result=False

			InteractBDD.endQuery(conn, cur)
			return result

		@staticmethod
		def joinGame(username, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			result=InteractBDD.joinThatGameID(username, gameid)
			if result==False:
				gameid=gameid+1
			
			request= "INSERT INTO `games` (`gameid`, `username`, `encours`, `currentstep`) VALUES ("+str(gameid)+", '"+username+"', 1, 1);"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			InteractBDD.setMyLocation(username, InteractBDD.villeDeDepart(), gameid)
			
			fruitsname=InteractBDD.giveAFruit(gameid)
			request = "INSERT INTO `pirate` (`username`, `name`, `level`, `fruit`, `qualite`, `gameid`) VALUES ('"+username+"','"+username+"','"+str(1)+"','"+fruitsname+"','"+str(0)+"', "+str(gameid)+");"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			for request in InteractBDD.fruits:
				request=request.format(str(gameid))
				InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			request = "UPDATE fruit SET allocated=1 WHERE gameid="+str(gameid)+" and name='"+fruitsname+"';"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			InteractBDD.endQuery(conn, cur)
			return gameid
			

		@staticmethod
		def numberOfGames(username):
			[conn, cur]=InteractBDD.beginQuery()
			count=0
			request= "SELECT encours FROM games WHERE username='"+username+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for _ in description:
				count+=1
			
			InteractBDD.endQuery(conn, cur)
			return count


		@staticmethod
		def villeDeDepart():
			[conn, cur]=InteractBDD.beginQuery()

			request = "SELECT nom from ile;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			iles=[]
			for elem in description:
				iles.append(elem[0])

			ile=iles[random.randint(0, len(iles)-1)]
				

			InteractBDD.endQuery(conn, cur)
			return ile


		@staticmethod
		def giveAFruit(gameid):
			availableFruits=InteractBDD.countAvailableFruits(gameid)
			if availableFruits==0:
				return "GumGum"
			fruitsNumber=random.randint(0,availableFruits-1)
			fruitsName=InteractBDD.notAllocatedFruits(gameid)[fruitsNumber]
			InteractBDD.allocateFruit(fruitsName, gameid)
			return fruitsName


		@staticmethod
		def gamesInProgress(username):
			[conn, cur]=InteractBDD.beginQuery()

			gamesid=[]
			request= "SELECT gameid FROM games WHERE username='"+username+"' and encours=1;"
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
			for _ in description:
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
			request = "INSERT INTO `joueur` (`username`, `password`) VALUES('"+username+"','"+password+"');"
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
		def getMyCrew(username, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			pirates=[]
			request = "SELECT name, level, fruit, qualite, gameid FROM pirate WHERE username='"+username+"' and gameid="+str(gameid)+";"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				txt=InteractBDD.pirateTXT(elem, 'Pirate', gameid)
				pirates.append(txt) #pas besoin de separation avec une ',', il n'y en a qu'un avec cet id
			InteractBDD.endQuery(conn, cur)
			return pirates

		@staticmethod
		def getMyPirate(id, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT name, level, fruit, qualite, gameid FROM pirate WHERE id='"+str(id)+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				txt=InteractBDD.pirateTXT(elem, 'Pirate', gameid)
			InteractBDD.endQuery(conn, cur)
			return txt


		@staticmethod #y a pas moyen de degager getmypirateid au profit de cette methode là?
		def getMyCrewsID(username, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			pirates=[]
			request = "SELECT id FROM pirate WHERE username='"+username+"' and gameid="+str(gameid)+";"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				id=int(elem[0])
				pirates.append(id) #pas besoin de separation avec une ',', il n'y en a qu'un avec cet id
			InteractBDD.endQuery(conn, cur)
			return pirates

			

		@staticmethod
		def getMyCrewMinLevel(username, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT MIN(level) FROM pirate WHERE username='"+username+"' and gameid="+str(gameid)+";"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				lvl=int(elem[0])
				InteractBDD.endQuery(conn, cur)
				return lvl
			return 1


		@staticmethod
		def getMyLocation(username, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT position FROM island WHERE username='"+username+"' and gameid="+str(gameid)+";"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				value = str(elem[0])
				InteractBDD.endQuery(conn, cur)
				return value
			InteractBDD.endQuery(conn, cur)
			return ""

		@staticmethod
		def getMyCurrentStep(username, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT currentstep FROM games WHERE username='"+username+"' and gameid="+str(gameid)+";"
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
			txt=txt+"id | gameid | username | encours | currentStep<br>"
			request = "select * from games;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				txt= txt+"| " + str(elem[0])
				txt= txt+"| " + str(elem[1])
				txt= txt+"| " + str(elem[2])
				txt= txt+"| " + str(elem[3])
				txt= txt+"| " + str(elem[4])
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
			txt=txt+"id | username | password  <br>"
			request = "select * from joueur;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				txt= txt+"| " + str(elem[0])
				txt= txt+"| " + str(elem[1])
				txt= txt+"| " + "Not Displayable"
				txt=txt+"<br>"
			txt=txt+"<br>"

			txt=txt+"island: <br>"
			txt=txt+"username | position's name | gameid <br>"
			request = "select * from island;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				for i in range(len(elem)):
					txt= txt+"| " + str(elem[i])
				txt=txt+"<br>"
			txt=txt+"<br>"

			txt=txt+"Pirate: <br>"
			txt=txt+" id | owner | name | level | fruit's name | qualite | gameid <br>"
			request = "select * from pirate;"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				for i in range(len(elem)):
					txt= txt+" | " + str(elem[i])
				txt=txt+"<br>"
			txt=txt+"<br>"

			txt=txt+"Fruit: <br>"
			txt=txt+" name | power | allocated  | gameid<br>"
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
			txt=txt+" nom | ile | level | fruit | qualite | phrase | droprate <br>"
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
		def checkPlayer(islandName, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT username FROM island WHERE position='"+islandName+"' and gameid="+str(gameid)+";"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				value = str(elem[0])
				InteractBDD.endQuery(conn, cur)
				return value
			InteractBDD.endQuery(conn, cur)
			return None


		@staticmethod
		def averagePirateLevel(username, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT level FROM pirate WHERE username='"+username+"' and gameid='"+str(gameid)+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			
			levels=[]
			for elem in description:
				levels.append(int(elem[0]))

			InteractBDD.endQuery(conn, cur)
			return sum(levels)/len(levels)

		@staticmethod
		def checkBoss(currentIslandName, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			request = "SELECT nom, level, fruit, qualite FROM pnj WHERE ile='"+currentIslandName+"';"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			txt=""
			for elem in description:
				txt=InteractBDD.pirateTXT(elem, 'Legende', gameid)
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
			return " attaque "


			
		@staticmethod
		def getDrop(currentIslandName, username, gameid):
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
				has=InteractBDD.hasThatBoss(bossName, username, gameid)
				if has:
					InteractBDD.endQuery(conn, cur)
					return None

				txt=InteractBDD.pirateTXT(elem, 'Legende', gameid)
				InteractBDD.endQuery(conn, cur)
				return [txt, drop]
			return None


		@staticmethod
		def hasThatBoss(bossName, username, gameid):
			[conn, cur]=InteractBDD.beginQuery()

			request = "SELECT name FROM pirate WHERE username='"+username+"' and name='"+bossName+"' and gameid="+str(gameid)+";"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for _ in description:
				InteractBDD.endQuery(conn, cur)
				return True
			
			InteractBDD.endQuery(conn, cur)
			return False


		#_____________________STORE_______________________________

		@staticmethod
		def setMyCrew(username, positionsName, pirates, currentstep, gameid):
			[conn, cur]=InteractBDD.beginQuery()

			for pirate in pirates:
				request = "INSERT INTO `pirate` (`username`, `name`, `level`, `fruit`, `qualite`, `gameid`) VALUES ('"+username+"','"+pirate.name+"','"+str(pirate.level)+"','"+pirate.fruit.name+"','"+str(pirate.qualite)+"', "+str(gameid)+");"
				InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			# TODO not a problem to not allocate fruits? 
			request = "UPDATE island SET position='"+positionsName+"' WHERE username='"+username+"' and gameid="+str(gameid)+";"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			request = "UPDATE games SET currentstep="+str(currentstep)+" WHERE username='"+username+"' and gameid="+str(gameid)+";"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			InteractBDD.endQuery(conn, cur)
			return None
		
		@staticmethod
		def setMyLocation(username, positionsName, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			request = "DELETE FROM island WHERE username='"+username+"' and gameid="+str(gameid)+";" # an update doesnt do the work since u r maybe not already in the table
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			request = "INSERT INTO island VALUES ('"+username+"', '"+positionsName+"', "+str(gameid)+");"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			InteractBDD.endQuery(conn, cur)
			return None

			

		@staticmethod
		def setMyCurrentStep(username, currentStep, gameid):
			[conn, cur]=InteractBDD.beginQuery()
			request = "UPDATE games SET currentstep='"+str(currentStep)+"' WHERE username='"+username+"' and gameid="+str(gameid)+";"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			InteractBDD.endQuery(conn, cur)
			return None

		@staticmethod
		def addNewFighter(username, pirate, gameid):
			[conn, cur]=InteractBDD.beginQuery() # TODO not a problem to not allocate fruits? 
			request = "INSERT INTO `pirate` (`username`, `name`, `level`, `fruit`, `qualite`, `gameid`) VALUES ('"+username+"','"+pirate.name+"','"+str(pirate.level)+"','"+pirate.fruit.name+"','"+str(pirate.qualite)+"', "+str(gameid)+");"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			InteractBDD.endQuery(conn, cur)
			return None


		@staticmethod
		def increasePirateLevel(username, gameid):
			[conn, cur]=InteractBDD.beginQuery()

			request = "UPDATE pirate SET level=level+1 WHERE username='"+username+"' and fruit='None' and gameid="+str(gameid)+";"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			request = "UPDATE pirate SET level=level+3 WHERE username='"+username+"' and fruit!='None' and gameid="+str(gameid)+";"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)
			InteractBDD.endQuery(conn, cur)
			return None


		#_________________________FRUITS_________________________________


		@staticmethod
		def countAvailableFruits(gameid):
			[conn, cur]=InteractBDD.beginQuery()

			InteractBDD.checkAllocatedFruits(gameid)

			request = "SELECT COUNT(*) FROM fruit WHERE allocated='0' and gameid="+str(gameid)+";"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				value=int(elem[0])
			
			InteractBDD.endQuery(conn, cur)
			return value


		@staticmethod
		def checkAllocatedFruits(gameid):
			[conn, cur]=InteractBDD.beginQuery()

			request = "UPDATE fruit SET allocated=0 WHERE gameid="+str(gameid)+";"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)


			request = "SELECT fruit FROM pirate WHERE gameid="+str(gameid)+";"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			
			[conn2, cur2]=InteractBDD.beginQuery()
			for elem in description:
				fruitsName=str(elem[0])
				request = "UPDATE fruit SET allocated=1 WHERE name='"+fruitsName+"' and gameid="+str(gameid)+";"
				InteractBDD.connectAndExecuteRequest(request, True, conn2, cur2)

			
			
			InteractBDD.endQuery(conn2, cur2)
			InteractBDD.endQuery(conn, cur)
			return None



		@staticmethod
		def notAllocatedFruits(gameid):
			[conn, cur]=InteractBDD.beginQuery()

			fruits=[]
			request = "SELECT name FROM fruit WHERE allocated=0 and gameid="+str(gameid)+";"
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
		def allocateFruit(fruitsName, gameid):
			[conn, cur]=InteractBDD.beginQuery()

			request = "UPDATE fruit SET allocated=1 WHERE name='"+str(fruitsName)+"' and gameid="+str(gameid)+";"
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
		def deleteUserProgress(username, gameid):

			[conn, cur]=InteractBDD.beginQuery()

			request = "DELETE FROM island WHERE username='"+username+"' and gameid="+str(gameid)+";"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			
			[conn2, cur2]=InteractBDD.beginQuery()
			#request = "SELECT fruit FROM pirate WHERE username='"+username+"' AND name NOT IN (SELECT nom FROM pnj);" 
			request = "SELECT fruit FROM pirate WHERE username='"+username+"' and gameid="+str(gameid)+";" 
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				fruitsName=str(elem[0]) # we got the name of the current archipel
				request = "UPDATE fruit SET allocated=0 WHERE name='"+str(fruitsName)+"' and gameid="+str(gameid)+";"
				InteractBDD.connectAndExecuteRequest(request, True, conn2, cur2)
			InteractBDD.endQuery(conn2, cur2)

			#request = "DELETE FROM pirate WHERE username='"+username+"' AND name NOT IN (SELECT nom FROM pnj);"
			request = "DELETE FROM pirate WHERE username='"+username+"' and gameid="+str(gameid)+";"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur) 

			#request = "UPDATE pirate SET level=1 WHERE username='"+username+"';"
			#InteractBDD.connectAndExecuteRequest(request, True, conn, cur) 

			InteractBDD.endQuery(conn, cur)
			return None

		@staticmethod
		def deletePirates(username, gameid):

			[conn, cur]=InteractBDD.beginQuery()
			
			[conn2, cur2]=InteractBDD.beginQuery()
			request = "SELECT fruit FROM pirate WHERE username='"+username+"' and gameid="+str(gameid)+";"
			description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			for elem in description:
				fruitsName=str(elem[0]) # we got the name of the current archipel
				request = "UPDATE fruit SET allocated=0 WHERE name='"+str(fruitsName)+"' and gameid="+str(gameid)+";"
				InteractBDD.connectAndExecuteRequest(request, True, conn2, cur2)
			InteractBDD.endQuery(conn2, cur2)

			request = "DELETE FROM pirate WHERE username='"+username+"' and gameid="+str(gameid)+";"
			InteractBDD.connectAndExecuteRequest(request, True, conn, cur)

			InteractBDD.endQuery(conn, cur)
			return None

		@staticmethod
		def deallocateFruitsFromCrew(obj, gameid):
			if obj.isinstance()=="Joueur":
				crew=obj.equipage
			else: #equipage
				crew=obj

			[conn2, cur2]=InteractBDD.beginQuery()
			for pirate in crew.team:
				if pirate.fruit.name!="None":
					request = "UPDATE fruit SET allocated=0 WHERE name='"+str(pirate.fruit.name)+"' and gameid="+str(gameid)+";"
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
		def removeFighter(username, pirate, gameid):
			[conn, cur]=InteractBDD.beginQuery()

			#boss=False
			#request = "SELECT nom FROM pnj WHERE nom='"+pirate.name+"';"
			#description = InteractBDD.connectAndExecuteRequest(request, False, conn, cur)
			#for elem in description:
			#	boss=True

			#if boss:
				
			#request = "UPDATE pirate SET level=level-10 WHERE username='"+username+"' AND name='"+pirate.name+"' AND level>10;"
			#InteractBDD.connectAndExecuteRequest(request, True, conn, cur) 

			#InteractBDD.endQuery(conn, cur)
			#return None

			#else:

			fruitsName=pirate.fruit.name
			if fruitsName!="None":
				request = "UPDATE fruit SET allocated=0 WHERE name='"+fruitsName+"' and gameid="+str(gameid)+";"
				InteractBDD.connectAndExecuteRequest(request, True, conn, cur)


			request = "DELETE FROM pirate WHERE username='"+username+"' and name='"+pirate.name+"' and fruit='"+pirate.fruit.name+"' and qualite='"+str(pirate.qualite)+"' and gameid="+str(gameid)+";"
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
		def pirateTXT(elem, cls, gameid):
			piratesName=elem[0]
			level=elem[1]
			fruitsName=elem[2]
			qualite=elem[3]

			boss= cls=="Legende"

			power=InteractBDD.fruitsPower(fruitsName)
			fruitsTXT='{"type": "FruitDemon", "name": "%s", "power": %s, "boss": "%s"}' % (fruitsName, str(power), str(boss)) 
			txt='{"type": "%s", "name": "%s", "gameid": %s, "level": %s, "qualite": %s, "fruit": %s, "stats": "%s", "availableToFight": "True", "mort": "False"}' % (cls, piratesName, str(gameid), str(level), str(qualite), fruitsTXT, str(StatsPirate.generateStats(level, qualite, power)) )
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
			return " attaque "

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





