
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
    print(type(obj))
    return obj



def load(obj):
    return json.loads(obj, object_hook=decode)






joueurTXT='{"type": "Joueur", "username": "Beefr"}'

#print(joueurTXT)
joueur = load(joueurTXT)


ennemies=[]
numberEnnemies=5
for i in range(numberEnnemies):
    ennemies.append(Pirate(150))

equipageEnnemy=Equipage(ennemies)

print(joueur.fight(equipageEnnemy))
