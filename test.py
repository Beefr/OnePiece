import os
print("\n" * 100)
os.system('cls')

import random
from joueur import Joueur
from pirate import Pirate
from equipage import Equipage
from fruitdemon import FruitFactory
from menu import Menu

import json
from collections import namedtuple




def decode(dict):
    tuple=namedtuple('Metamorph', dict.keys())(*dict.values())
    if tuple.type=="Joueur":
        obj= Joueur(tuple.username,1)
    elif tuple.type=="Pirate":
        obj= Pirate(tuple.gameid, tuple.level)
        obj.name=tuple.name
        obj.qualite=tuple.qualite
        obj.fruit=tuple.fruit
    elif tuple.type=="FruitDemon":
        obj= FruitFactory.giveThatFruit(tuple.name, tuple.boss)
    #print(type(obj))
    return obj



def load(obj):
    return json.loads(obj, object_hook=decode)






joueurTXT='{"type": "Joueur", "username": "Beefr", "gameid": 1}'

#print(joueurTXT)
#joueur = load(joueurTXT)

'''
ennemies=[]
numberEnnemies=5
name="pirateTest"
for i in range(numberEnnemies):
    pirate=Pirate(100, True, name+str(i))
    #print(str(pirate))
    ennemies.append(pirate)'''
    
#equipageEnnemy=Equipage(ennemies)

#joueur.fight(equipageEnnemy)


#menu=Menu()
#menu.joueur=joueur

#output=menu.showMenu(1)
#output['content'].print()
#output=menu.showMenu("y")
#output['content'].print()

'''
test=["mort",1,2,3,"mort",5]
for count in range(len(test)-1,-1,-1):
    print(count)
    print(test[count])
    if test[count]=="mort":
        test.pop(count)

print(test)'''

'''i=0
iles=["boudin","boudin2","boudin3","boudin4","boudin5"]
while i<100:
    ile=iles[random.randint(0, len(iles)-1)]
    i+=1
    print(ile)'''















