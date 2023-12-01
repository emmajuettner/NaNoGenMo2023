import json
import math
import random
import os
from pathlib import Path
from jinja2 import FileSystemLoader, Environment
import tracery
from tracery.modifiers import base_english

# This code is a mess, sorry!

# Utility functions

def generateFromGrammar(grammarFile, origin):
	grammarStr = Path("grammars/"+grammarFile+".json").read_text()
	grammarJson = json.loads(grammarStr)
	grammar = tracery.Grammar(grammarJson)
	grammar.add_modifiers(base_english)
	return grammar.flatten("#" + origin + "#")

def chooseRandom(arr) :
	return random.choice(arr)

def arrayWithout(superSet, subSetToExclude):
	return list(set(superSet).difference(set(subSetToExclude)))

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

# Establish initially held clues
peopleClues = arrayWithout(people, [whoDunnit])
weaponClues = arrayWithout(weapons, [whatDunnit])
placesClues = arrayWithout(places, [whereDunnit])
allClues = peopleClues + weaponClues + placesClues
detectiveIndex = 0
while len(allClues) > 0:
	randomClue = chooseRandom(allClues)
	if randomClue in people:
		detectiveHasAcquiredClues[people[detectiveIndex]]["people"].append(randomClue)
	elif randomClue in weapons:
		detectiveHasAcquiredClues[people[detectiveIndex]]["weapons"].append(randomClue)
	else:
		detectiveHasAcquiredClues[people[detectiveIndex]]["places"].append(randomClue)
	allClues.remove(randomClue)
	detectiveIndex += 1
	if detectiveIndex >= len(people):
		detectiveIndex = 0

# Generate novel text
solution = "It was " + whoDunnit + " in the " + whereDunnit + " with the " + whatDunnit + "!"
novel = ""

def addToNovel(newParagraph):
	global novel
	novel += "<p>" + newParagraph + "</p>"

def addDividerToNovel():
	global novel
	novel += "<hr>\n"

# Introduction
addToNovel(generateFromGrammar("weather", "origin"))
addToNovel("Six visitors had come to Boddy Manor by express invitation of its owner, Mr Boddy.")
for detective in people:
	addToNovel(detective + " was " + generateFromGrammar("people", "individual") + ".")
addToNovel(generateFromGrammar("people", "group"))
addDividerToNovel()

def moveDetective(detective):
	#unexploredPlaces = list(set(places).difference(set(detectiveHasAcquiredClues[detective]["places"])))
	#if len(unexploredPlaces) == 0:
	#	newLocation = chooseRandom(places)
	#else:
	#	newLocation = chooseRandom(unexploredPlaces)
	newLocation = chooseRandom(arrayWithout(places, [detectiveLocations[detective]]))
	detectiveLocations[detective] = newLocation
	addToNovel(generateFromGrammar("adverbs", "enteringRoom") + ", " +
		 detective + " stepped into the " + newLocation + ".")

def callDetective(callingDetective, location):
	calledDetective = chooseRandom(arrayWithout(people, [callingDetective]))
	addToNovel(callingDetective + " called " + calledDetective + " into the " + location + ".")
	detectiveLocations[calledDetective] = location

def possibleClues(detective):
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

def possibleSuggestees(detective):
	currentLocation = detectiveLocations[detective]
	peopleToSuggestTo = []
	for person in people:
		if person is not detective and detectiveLocations[person] is currentLocation:
			peopleToSuggestTo.append(person)
	return peopleToSuggestTo

def generateSuggestion(detective):
	peopleToSuggest = arrayWithout(people, detectiveHasAcquiredClues[detective]["people"])
	weaponsToSuggest = arrayWithout(weapons, detectiveHasAcquiredClues[detective]["weapons"])
	placeToSuggest = detectiveLocations[detective]
	return chooseRandom(people), chooseRandom(weapons), placeToSuggest

def refuteSuggestion(person, weapon, place, suggestee):
	canRefute = {}
	if person in detectiveHasAcquiredClues[suggestee]["people"]:
		canRefute[person]=" it wasn't " + person + ". " + person + " " + generateFromGrammar("refutations", "person")
	if weapon in detectiveHasAcquiredClues[suggestee]["weapons"]:
		canRefute[weapon]=" the murder weapon isn't the " + weapon + ". " + generateFromGrammar("refutations", weapon)
	if place in detectiveHasAcquiredClues[suggestee]["places"]:
		canRefute[place]=" the murder couldn't have taken place in the " + place + ". " + generateFromGrammar("refutations", "location")
	if len(canRefute) == 0:
		return "", ""
	else:
		refutedClue = chooseRandom(list(canRefute.items()))
		return generateFromGrammar("refutations", "canRefute") + refutedClue[1], refutedClue[0]

def describeSuggestees(suggestees, location):
	description = ""
	if len(suggestees) == 1:
		description += "One other"
	elif len(suggestees) == 2:
		description += "Two others"
	elif len(suggestees) == 3:
		description += "Three others"
	elif len(suggestees) == 4:
		description += "Four others"
	elif len(suggestees) == 5:
		description += "Five others"
	description += " already occupied the room. "
	for detective in suggestees:
		description += detective + " was " + generateFromGrammar("people", location) + ". "
	return description

def acquireClues(detective):
	suggestees = possibleSuggestees(detective)
	if len(suggestees) == 0:
		addToNovel("The room was empty.")
		callDetective(detective, detectiveLocations[detective])
	else:
		addToNovel(describeSuggestees(suggestees, detectiveLocations[detective]))
	suggestees = possibleSuggestees(detective)
	suggestee = chooseRandom(suggestees)
	personToSuggest, weaponToSuggest, placeToSuggest = generateSuggestion(detective)
	personToSuggestRelativeToSpeaker = personToSuggest
	if personToSuggest == detective:
		personToSuggestRelativeToSpeaker = "me"
	elif personToSuggest == suggestee:
		personToSuggestRelativeToSpeaker = "you"
	addToNovel(detective + " said, \"" + suggestee + ", " 
		+ generateFromGrammar("suggestions", "introduceSuggestion") + " it was " + personToSuggestRelativeToSpeaker 
		+ " in the " + placeToSuggest + " with the " + weaponToSuggest + "!\"")
	refutedSuggestion, refutedClue = refuteSuggestion(personToSuggest, weaponToSuggest, placeToSuggest, suggestee)
	if len(refutedSuggestion) == 0:
		addToNovel(generateFromGrammar("adverbs", "notRefutingSuggestion") + ", " + suggestee + " replied, \"" + generateFromGrammar("refutations", "cannotRefute") + "\"")
	else:
		addToNovel(generateFromGrammar("adverbs", "refutingSuggestion") + ", " 
			+ suggestee + " answered, \"" + refutedSuggestion + "\"")
		addToNovel("\"Oh,\" " + detective + " said. \"" + generateFromGrammar("refutations", "refutationResponse") + "\"")
		if personToSuggest in suggestees:
			addToNovel(personToSuggest + " shot " + detective + generateFromGrammar("suggestions", "accusedLook") + ".")
		if random.random() < 0.8:
			return
		if refutedClue in people:
			detectiveHasAcquiredClues[detective]["people"].append(refutedClue)
		elif refutedClue in places:
			detectiveHasAcquiredClues[detective]["places"].append(refutedClue)
		else:
			detectiveHasAcquiredClues[detective]["weapons"].append(refutedClue)

def generateFinalMonologue():
	monologue = "\""
	for i in range(5):
		monologue += generateFromGrammar("monologue", "origin")
	monologue = monologue[0:len(monologue)-2]
	monologue += "--\""
	return monologue

mysterySolved = False;
while mysterySolved is not True:
	for detective in people:
		moveDetective(detective)
		acquireClues(detective)
		if (detective is not whoDunnit 
			and len(detectiveHasAcquiredClues[detective]["places"]) >= 8
			and len(detectiveHasAcquiredClues[detective]["weapons"]) >= 5
			and len(detectiveHasAcquiredClues[detective]["people"]) >= 5):
			mysterySolved = True
			addDividerToNovel()
			addToNovel(detective + " called everyone to gather together and began to speak: " + generateFinalMonologue())
			interruptingDetective = chooseRandom(arrayWithout(people, [detective, whoDunnit]))
			addToNovel("\"Excuse me,\" broke in " + interruptingDetective + ". \"Are you going to tell us who actually did it?\"")
			solution.replace(detective, "me")
			addToNovel("\"Why, haven't I said already?\" asked " + detective + ". \"" + solution + "\"")
			break
		addDividerToNovel()

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

