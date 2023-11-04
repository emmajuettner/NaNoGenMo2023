import json
import math
import random
import os
from pathlib import Path
from jinja2 import FileSystemLoader, Environment


def chooseRandom(arr) :
	return random.choice(arr)

# Constants
people = ["Miss Scarlett", "Professor Plum", "Colonel Mustard", "Mr Green", "Mrs Peacock", "Mrs White"]
weapons = ["candlestick", "knife", "lead pipe", "revolver", "rope", "wrench"]
places = ["kitchen", "ballroom", "conservatory", "billiard room", "library", "study", "hall", "lounge", "dining room"]

# Detective variables
detectiveLocations = {"Miss Scarlett" : "", "Professor Plum" : "", "Colonel Mustard" : "", "Mr Green" : "", "Mrs Peacock" : "", "Mrs White" : ""}
detectiveHasAcquiredClues = {"Miss Scarlett" : {"people" : [], "places" : [], "weapons" : []}, 
							 "Professor Plum" : {"people" : [], "places" : [], "weapons" : []},
							 "Colonel Mustard" : {"people" : [], "places" : [], "weapons" : []},
							 "Mr Green" : {"people" : [], "places" : [], "weapons" : []}, 
							 "Mrs Peacock" : {"people" : [], "places" : [], "weapons" : []},
							 "Mrs White" : {"people" : [], "places" : [], "weapons" : []}}

# Establish secrets
whoDunnit = chooseRandom(people)
whatDunnit = chooseRandom(weapons)
whereDunnit = chooseRandom(places)

# Generate novel text
solution = "It was " + whoDunnit + " in the " + whereDunnit + " with the " + whatDunnit + "!"
novel = "It was a dark and stormy night...\n"

def moveDetective(detective):
	global novel
	newLocation = chooseRandom(places)
	detectiveLocations[detective] = newLocation
	novel += detective + " has moved to the " + newLocation + "\n"

def possibleClues(detective):
	global novel
	possibleClues = []
	if detectiveLocations[detective] not in detectiveHasAcquiredClues[detective]["places"] and detectiveLocations[detective] is not whereDunnit:
		possibleClues.append(detectiveLocations[detective])
	for weapon in weapons:
		if weapon not in detectiveHasAcquiredClues[detective]["weapons"] and weapon is not whatDunnit:
			possibleClues.append(weapon)
	for person in people:
		if person not in detectiveHasAcquiredClues[detective]["people"] and person is not whoDunnit:
			possibleClues.append(person)
	return possibleClues

def acquireClues(detective):
	global novel
	clues = possibleClues(detective)
	if len(clues) == 0:
		novel += (detective + " has found " + str(detectiveHasAcquiredClues[detective]["people"]) + " people clues"
				+ " and " + str(detectiveHasAcquiredClues[detective]["places"]) + " places clues"
				+ " and " + str(detectiveHasAcquiredClues[detective]["weapons"]) + " weapons clues.") + "\n"
		return
	newClue = chooseRandom(clues)
	novel += detective + " found a clue: " + newClue + "\n"
	if newClue in people:
		detectiveHasAcquiredClues[detective]["people"].append(newClue)
	elif newClue in places:
		detectiveHasAcquiredClues[detective]["places"].append(newClue)
	else:
		detectiveHasAcquiredClues[detective]["weapons"].append(newClue)

mysterySolved = False;
while mysterySolved is not True:
	for detective in people:
		moveDetective(detective)
		acquireClues(detective)
		if (detective is not whoDunnit 
			and len(detectiveHasAcquiredClues[detective]["places"]) == 8
			and len(detectiveHasAcquiredClues[detective]["people"]) == 5
			and len(detectiveHasAcquiredClues[detective]["weapons"]) == 5):
			mysterySolved = True
			novel += detective + " solved the mystery!" + "\n"
			break

print(novel)

# Build an html file populated with the novel we've generated
loader = FileSystemLoader(".")
env = Environment(
    loader=loader, extensions=["jinja2_humanize_extension.HumanizeExtension"]
)
template = env.get_template("index.jinja")
Path("index.html").write_text(
    template.render(
        {
            "novel" : novel
        }
    )
)
print("Generated index.html")

