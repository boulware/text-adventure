from group import Group
import group as m_group
from person import Person
from item import Item
from action import Action
from verb import Verb
import verb as m_verb
from state import State

import ipdb

events = []
world_time = 0

people = Group('person', Person, 'data/people.dat')
items = Group('item', Item, 'data/items.dat')
verbs = Group('verb', Verb, 'data/verbs.dat')
actions = Group('action', Action, 'data/actions.dat')
states = Group('state', State, 'data/states.dat')

player = m_group.find_member_by_name(people, 'tyler')

# (TEST) test for unfound verbs in unit tests
# (TODO) Don't forget about these empty syntaxes. I need a way to properly deal with it.
# (NOTE) This is a shortcut implementation for: tell TARGET "UTTERANCE". Shortcutted because I'm not sure how I'll handle this yet.

text_input = ''
while text_input != 'q':
	text_input = input('> ')
	text_input = text_input.strip() # (SELF) This is an important line. Without it, our regex will break. Think carefully before removing it.
	text_input = text_input.lower()
	#text_input = 'tyler ' + text_input

	command, delim, arguments = text_input.partition(' ')
	text_input = 'tyler ' + text_input
	arguments = delim + arguments # (TEMP) messy fix for some weird stuff going on in the Action regex.

	#print("command=\'{}\'; arguments=\'{}\'".format(command, arguments))

	for verb in verbs:
		if command == verb.lemma:
			event = m_verb.do(verb, text_input, world_time) # (TEMP) throwing verbs on as an arg to get back old functionality with general action template
			if event:
				events.append(event)
				for i, event in enumerate(events):
					pass#print("event {}: {}".format(i, event.action.name))

	world_time += 1
