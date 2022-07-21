import os
print("\n" * 100)
os.system('cls')


from joueur import Joueur
from pirate import Pirate
from equipage import Equipage
from fruitdemon import FruitFactory

import json
from collections import namedtuple




def decode(dict):
    tuple=namedtuple('Metamorph', dict.keys())(*dict.values())
    if tuple.type=="Joueur":
        obj= Joueur(tuple.username)
    elif tuple.type=="Pirate":
        obj= Pirate(tuple.level)
        obj.name=tuple.name
        obj.qualite=tuple.qualite
        obj.fruit=tuple.fruit
    elif tuple.type=="FruitDemon":
        obj= FruitFactory.giveThatFruit(tuple.name)
    #print(type(obj))
    return obj



def load(obj):
    return json.loads(obj, object_hook=decode)






joueurTXT='{"type": "Joueur", "username": "Beefr"}'

#print(joueurTXT)
joueur = load(joueurTXT)


ennemies=[]
numberEnnemies=5
name="pirateTest"
for i in range(numberEnnemies):
    pirate=Pirate(100, True, name+str(i))
    #print(str(pirate))
    ennemies.append(pirate)
    
equipageEnnemy=Equipage(ennemies)

print(joueur.fight(equipageEnnemy))



'''
test=["mort",1,2,3,"mort",5]
for count in range(len(test)-1,-1,-1):
    print(count)
    print(test[count])
    if test[count]=="mort":
        test.pop(count)

print(test)'''