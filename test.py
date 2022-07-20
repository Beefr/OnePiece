from joueur import Joueur
from pirate import Pirate
from equipage import Equipage
import json
from collections import namedtuple




def decode(dict):
    tuple=namedtuple('Metamorph', dict.keys())(*dict.values())
    if tuple.type=="Joueur":
        obj= Joueur(tuple.username, tuple.equipage, tuple.position, tuple.availableToFight)
    elif tuple.type=="Pirate":
        obj= Pirate(tuple.level)
        obj.name=tuple.name
        obj.qualite=tuple.qualite
        obj.fruit=tuple.fruit
    print(type(obj))
    return obj



def load(obj):
    return json.loads(obj, object_hook=decode)












fruit = '{"type": "FruitDemon", "name": "%s", "power": %s}' % ("GumGum", "[50,50,0,0]") 
pirate='{"type": "Pirate", "level": 150, "name": "Beefr", "qualite": 1, "fruit": "%s"}' % (fruit)
joueurTXT= '{ "type": "Joueur", "username": "Beefr", "equipage": [%s], "position": "Amazon Lily", "availableToFight": true }' % (pirate)
joueur = load(joueurTXT)


ennemies=Equipage([Pirate(150)])

#print(joueur.fight(ennemies))
