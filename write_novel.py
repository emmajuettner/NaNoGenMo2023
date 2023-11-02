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
novel = "It was " + whoDunnit + " in the " + whereDunnit + " with the " + whatDunnit + "!"

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
