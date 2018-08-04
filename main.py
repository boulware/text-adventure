from group import Group
import group as m_group
from person import Person
from item import Item
from action import Action
import action as m_action
from state import State
from event import Event
from lexicon import Lexicon
from semanticon import Semanticon, SemantType
from inflection import InflectionType, InflectionTense, InflectionNumber, InflectionPerson, InflectionModel, Inflection, inflect

from world import World
import world as m_world

import json

semanticon = Semanticon({	SemantType.Object: "data/semanticon/objects.dat",
							SemantType.Action: "data/semanticon/actions.dat",
							SemantType.State: "data/semanticon/states.dat",
							SemantType.Property: "data/semanticon/properties.dat",
							SemantType.Determination: "data/semanticon/determinations.dat"})


inflection_models = Group("inflection models", InflectionModel, "data/lexicon/inflection_models.dat")
default_model = m_group.find_member_by_name(inflection_models, 'default')
this_inflection = Inflection(type_=InflectionType.Indicative, tense=InflectionTense.Past, number=InflectionNumber.Plural, person=InflectionPerson.First)
inflected_word = inflect(default_model, "jump", this_inflection)
print("inflected word={}".format(inflected_word))

events = []
world_time = 0

world = World()
#Lexicon("data/nouns.dat", "data/verbs.dat", "data/adjectives.dat")

player = m_group.find_member_by_name(world.people, 'tyler')

# (TEST) test for unfound verbs in unit tests
# (TODO) Don't forget about these empty syntaxes. I need a way to properly deal with it.
# (NOTE) This is a shortcut implementation for: tell TARGET "UTTERANCE". Shortcutted because I'm not sure how I'll handle this yet.

text_input = ''
while text_input != 'q':
	text_input = input('> ')
	text_input = text_input.strip() # (SELF) This is an important line. Without it, our regex will break. Think carefully before removing it.
	text_input = text_input.lower()

	command, delim, arguments = text_input.partition(' ')
	if command == ',?':
		for action in world.actions:
			print(action.lemma + ' [' + action.syntax + ']')
	if command == ',q':
		break
	if command == ',s':
		m_world.print_states(world)
	if command == ',e':
		m_world.print_events(world)
	if command == ',t':
		world_time += 1

	text_input = 'tyler ' + text_input

	for action in world.actions:
		if command == action.lemma:
			world_time += 1

			result = m_action.do(action, text_input, world_time, world.actions)
			if type(result) is Event:
				world.events.append(result)
				m_world.print_events(world)
			# (CONC) Is it really necessary to check for stative actions in a function called "do()"?
			if type(result) is State:
				world.states.append(result)
				m_world.print_states(world)