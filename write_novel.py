import json
import math
import random
import os
from pathlib import Path
from jinja2 import FileSystemLoader, Environment

def chooseRandom(arr) :
	return arr[random.randint(0,len(arr)-1)]

# Constants
people = ["Miss Scarlett", "Professor Plum", "Colonel Mustard", "Mr Green", "Mrs Peacock", "Mrs White"]
weapons = ["candlestick", "knife", "lead pipe", "revolver", "rope", "wrench"]
places = ["kitchen", "ballroom", "conservatory", "billiard room", "library", "study", "hall", "lounge", "dining room"]

# Establish secrets
whoDunnit = chooseRandom(people)
whatDunnit = chooseRandom(weapons)
whereDunnit = chooseRandom(places)

# Generate novel text
newLine = "It was " + whoDunnit + " in the " + whereDunnit + " with the " + whatDunnit + "!"

print(newLine)
