

class SQL(object):
    
    
    insertGames="INSERT INTO `games` (`gameid`, `username`, `encours`, `currentstep`) VALUES ({}, '{}', 1, 1);"
    insertJoueur="INSERT INTO `joueur` (`username`, `password`) VALUES('{}','{}');"
    insertPirate="INSERT INTO `pirate` (`username`, `name`, `level`, `fruit`, `qualite`, `gameid`) VALUES ('{}','{}',{},'{}',{}, {});"
    insertIsland = "INSERT INTO island VALUES ('{}', '{}', {});"

    #__________________________DELETE_________________________________
    deletePirate="DELETE FROM pirate WHERE username='{}' and name='{}' and fruit='{}' and qualite='{}' and gameid={};"
    deletePirate2="DELETE FROM pirate WHERE username='{}' and gameid={};"

    deleteIsland = "DELETE FROM island WHERE username='{}' and gameid={};" 

    #__________________________SELECT_________________________________
    #fruit
    selectAllFruit="select * from fruit;"
    selectCount="SELECT COUNT(*) FROM fruit WHERE allocated='0' and gameid={};"
    selectFruitsname="SELECT name FROM fruit WHERE allocated=0 and gameid={};"
    selectPower= "SELECT power FROM fruit WHERE name='{}';" 

    # pirate
    selectAllPirate="select * from pirate;"
    selectFruit="SELECT fruit FROM pirate WHERE gameid={};"
    selectFruit2="SELECT fruit FROM pirate WHERE username='{}' and gameid={};"
    selectPirate="SELECT name, level, fruit, qualite, gameid FROM pirate WHERE username='{}' and gameid={};"
    selectPirate2="SELECT name, level, fruit, qualite, gameid FROM pirate WHERE id={};"

    # pnj
    selectAllPNJ="select * from pnj;"
    selectPNJ="SELECT nom, level, fruit, qualite FROM pnj WHERE ile='{}';"
    
    # ile
    selectAllIle="select * from ile;"
    selectNomIle="SELECT nom FROM ile;"
    selectNomIle2="SELECT nom FROM ile WHERE archipel='{}';"
    selectArchipel="SELECT archipel FROM ile WHERE nom='{}';"

    # world
    selectAllWorld="select * from world;"
    selectLiaison= "SELECT archipel1, archipel2 FROM world WHERE archipel1='{}' OR archipel2='{}';"

    # archipel
    selectAllArchipel="select * from archipel;"
    selectIlePrincipale =  "SELECT ileprincipale FROM archipel WHERE nom='{}';"

    # games
    selectAllGames="select * from games;"
    selectCurrentStep="SELECT currentstep FROM games WHERE username='{}' and gameid={};"
    selectEnCours="SELECT encours, username FROM games WHERE gameid={};"
    selectGID= "SELECT gameid FROM games WHERE username='{}' and encours=1;"
    selectGID2= "SELECT gameid FROM games WHERE gameid={};"

    # joueur
    selectAllJoueurs= "select * from joueur;"

    # island
    selectAllIsland= "select * from island;"

    checkIsland="SELECT username FROM island WHERE position='{}' and gameid={};"
    selectDrop="SELECT perc FROM pnj WHERE ile='{}';"
    selectIDjoueur="SELECT id FROM joueur WHERE username='{}';"
    selectIDpirate="SELECT id FROM pirate WHERE username='{}' and gameid={};"
    selectLevel="SELECT level FROM pirate WHERE username='{}' and gameid={};"
    selectMaxGID="SELECT max(gameid) FROM games;"
    selectMinLevel="SELECT MIN(level) FROM pirate WHERE username='{}' and gameid={};"
    selectName="SELECT name FROM pirate WHERE username='{}' and name='{}' and gameid={};"
    selectPassword="SELECT password FROM joueur WHERE username='{}';"
    selectPhrase= "SELECT phrase FROM pnj WHERE nom='{}';"
    selectPosition="SELECT position FROM island WHERE username='{}' and gameid={};"
    selectUsername= "SELECT username FROM joueur WHERE username='{}';"
    selectUsername2="SELECT username FROM joueur WHERE id={};"

    #___________________________UPDATE__________________________________
    updateFruit="UPDATE fruit SET allocated={} WHERE name='{}' and gameid={};"
    updateFruit2="UPDATE fruit SET allocated={} WHERE gameid={};"

    updateIsland="UPDATE island SET position='{}' WHERE username='{}' and gameid={};"
    updateGames="UPDATE games SET currentstep={} WHERE username='{}' and gameid={};"
    updatePirate1="UPDATE pirate SET level=level+1 WHERE username='{}' and fruit='None' and gameid={};"
    updatePirate3="UPDATE pirate SET level=level+3 WHERE username='{}' and fruit='None' and gameid={};"

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

