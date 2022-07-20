import random
import numpy as np
import os

from fruitdemon import FruitFactory
from pirate import Pirate, Legende

import json
from collections import namedtuple

import hashlib

class Static:
	def __new__(cls):
		raise TypeError('Static classes cannot be instantiated')


class Utils(Static):




	@staticmethod
	def shuffle(pirates):
		places=np.arange(0,len(pirates))
		random.shuffle(places)
		shuffledList=[]
		for place in places:
			shuffledList.append(pirates[place])
		return shuffledList


	@staticmethod
	def clear():
		os.system('cls')


	@staticmethod
	def removeElement(array, index):
		temp=[]
		count=0
		for elem in array:
			if count!=index:
				temp.append(elem)
			count+=1
		return temp


	@staticmethod
	def hashPassword(password):
		# https://docs.python.org/fr/3/library/hashlib.html
		password=hashlib.blake2b(password.encode('utf-8')).hexdigest()
		try:
			password=password[0:240]
		except:
			pass
		return password
		

	
	@staticmethod
	def sanitization(user_input):
		forbiddenCharacters=["'", "\"", "\\", "&", "~", "{", "(", "[", "-", "|", "`", "_", "ç", "^", "à", "@", ")", "]", "=", "}", "+", "$", "£", "¤", "*", "µ", "ù", "%", "!", "§", ":", "/", ";", ".", ",", "?", "<", ">", "²"]
		if len(user_input)==0 or user_input=="": # empty input
			return False

		for elem in user_input:
			if len(elem)>=40: # max 15 characters
				return False
				
			for char in forbiddenCharacters: # no special characters
				if char in elem:
					return False
		return True


	#_________________________________LOADING DYNAMICALLY____________________________

	@staticmethod
	def decode(dict):
		tuple=namedtuple('Metamorph', dict.keys())(*dict.values())
		if tuple.type=="Legende":
			obj= Legende(tuple.name, tuple.level, tuple.fruit, tuple.qualite)
		elif tuple.type=="Pirate":
			obj= Pirate(tuple.level)
			obj.name=tuple.name
			obj.qualite=tuple.qualite
			obj.fruit=tuple.fruit
		elif tuple.type=="FruitDemon":
			obj= FruitFactory.giveThatFruit(tuple.name)
		else:
			obj=None
		return obj


	@staticmethod
	def load(obj):
		return json.loads(obj, object_hook=Utils.decode)






