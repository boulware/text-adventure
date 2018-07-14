from group import Group
import group as m_group
from person import Person
from item import Item
from action import Action
from verb import Verb
import verb as m_verb
from state import State
from event import Event

from world import World
import world as m_world

events = []
world_time = 0

world = World()

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
		for verb in world.verbs:
			print(verb.lemma + ' [' + verb.syntax + ']')
	if command == ',q':
		break
	if command == ',s':
		m_world.print_states(world)
	if command == ',e':
		m_world.print_events(world)
	if command == ',t':
		world_time += 1

	text_input = 'tyler ' + text_input

	for verb in world.verbs:
		if command == verb.lemma:
			world_time += 1

			result = m_verb.do(verb, text_input, world_time, world.verbs)
			if type(result) is Event:
				world.events.append(result)
				m_world.print_events(world)
			# (CONC) Is it really necessary to check for stative verbs in a function called "do()"?
			if type(result) is State:
				world.states.append(result)
				m_world.print_states(world)