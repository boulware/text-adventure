from group import Group
from person import Person
from item import Item
from action import Action
from verb import Verb

import ipdb

events = []
world_time = 0

people = Group('person')
people.append(Person('tyler'))
player = people[-1]
people.append(Person('john'))
people.append(Person('mary'))

items = Group('item')
items.append(Item('torch'))

verbs = Group('verb')
verbs.append(Verb('jump', 'jumped'))
verbs.append(Verb('hug', 'hugged'))
verbs.append(Verb('give', 'gave'))
verbs.append(Verb('walk', 'walked'))
verbs.append(Verb('crazy', 'crazied'))
verbs.append(Verb('doubleref', 'doublereffed'))
verbs.append(Verb('doublekw', 'doublekwed'))
verbs.append(Verb('kill', 'killed'))
verbs.append(Verb('tell', 'told'))
verbs.append(Verb('take', 'took'))
verbs.append(Verb('laugh', 'laughed'))

actions = Group('action')
actions.append(Action('jump'))
actions.append(Action('hug TARGET'))
actions.append(Action('give ITEM to TARGET'))
actions.append(Action('walk to LOCATION'))
actions.append(Action('crazy A to B while C and D'))
actions.append(Action('doubleref A to B C and D'))
actions.append(Action('doublekw A to B and or C for D'))
#actions.append(Action('')) # (NOTE) Don't forget about these empty syntaxes. I need a way to properly deal with it.

# Old actions reimplemented with generic action implementation
actions.append(Action('kill TARGET'))
# (NOTE) This is a shortcut implementation for: tell TARGET "UTTERANCE". Shortcutted because I'm not sure how I'll handle this yet.
actions.append(Action('tell TARGET that UTTERANCE'))
actions.append(Action('take ITEM from TARGET'))
actions.append(Action('laugh'))

text_input = ''
while text_input != 'q':
	text_input = input('> ')
	text_input = text_input.strip() # (SELF) This is an important line. Without it, our regex will break. Think carefully before removing it.
	text_input = text_input.lower()

	command, delim, arguments = text_input.partition(' ')
	arguments = delim + arguments # (TEMP) messy fix for some weird stuff going on in the Action regex.

	#print("command=\'{}\'; arguments=\'{}\'".format(command, arguments))

	for action in actions:
		if command == action.name:
			event = action.do(player, arguments, world_time, verbs) # (TEMP) throwing verbs on as an arg to get back old functionality with general action template
			if event:
				events.append(event)
				for i, event in enumerate(events):
					pass#print("event {}: {}".format(i, event.action.name))


#	# Syntax:
#	#	jump
#	if command == 'jump':
#		event = jump.do(player, text_input, world_time)
#		if event:
#			events.append(event)
#
#	# Syntax:
#	#	hug TARGET
#	if command == 'hug':
#		event = hug.do(player, text_input, world_time)
#		if event:
#			events.append(event)
#
#	# Syntax:
#	#	give ITEM to TARGET
#	if command == 'give':
#		event = give.do(player, text_input, world_time)
#		if event:
#			events.append(event)
#
#	# Syntax:
#	#	walk to LOCATION
#	if command == 'walk':
#		event = walk.do(player, text_input, world_time)
#
#	if command == 'crazy':
#		event = crazy.do(player, 'crazy A to B while C and D or E', world_time)
#		if event:
#			events.append(event)
#
#	if command == 'doubleref':
#		event = doubleref.do(player, 'doubleref A to B C and D', world_time)
#		if event:
#			events.append(event)
#
#	if command == 'doublekw':
#		event = doublekw.do(player, 'doublekw A to B and or C for D', world_time)
#		if event:
#			events.append(event)

	# Syntax:
	#	kill TARGET
#	if command[0] == 'kill':
#		if parameters:
#			target_name = parameters
#		if not parameters:
#			print("Who would you like to kill?")
#			target_name = input('> (kill) ')
#
#		target_list = m_group.find_member_by_name(people, target_name)
#		if m_group.check_target(target_list, people, target_name) == m_group.e_target_type.unique:
#			event = player.kill(*target_list, world_time)
#			events.append(event)

	# Syntax:
	#	tell TARGET "UTTERANCE"
#	if command[0] == 'tell':
#		bad_syntax = False
#
#		if parameters:
#			if parameters.count('\"') == 2:
#				# We've got one and only one valid quote-enclosed utterance.
#				# Now let's take a slice of everything before that and use that as the target name
#				opening_quote = parameters.find('\"')
#				closing_quote = parameters.rfind('\"')
#				target_name = parameters[:opening_quote].rstrip()
#				# (SELF) Why is it +1 for opening_quote but nothing for closing_quote? It works, but I don't know why
#				utterance = parameters[opening_quote+1 : closing_quote]
#			else:
#				bad_syntax = True
#				print("Incorrect syntax. Try: tell TARGET \"UTTERANCE\"")
#		else:
#			print("Who would you like to tell?")
#			target_name = input('> (tell) ')
#			print("What would you like to say?")
#			utterance = input('> (tell {}) '.format(target_name))
#
#		if not bad_syntax:
#			target_list = m_group.find_member_by_name(people, target_name)
#			if m_group.check_target(target_list, people, target_name) == m_group.e_target_type.unique:
#				event = player.tell(*target_list, utterance, world_time)
#				events.append(event)
#
#	# Syntax:
#	#	give ITEM to TARGET
#	if command[0] == 'give':
#		bad_syntax = False
#
#		if parameters:
#			to_delimiter = ' to '
#			to_location = parameters.rfind(' to ')
#			if to_location != -1:
#				item_name = parameters[:to_location].strip().lower()
#				target_name = parameters[to_location+len(to_delimiter):].strip().lower()
#			else:
#				bad_syntax = True
#				print("Incorrect syntax. Try: give ITEM to TARGET")
#		else:
#			print("What would you like to give?")
#			item_name = input('> (give) ')
#			print("Who would you like to give to?")
#			target_name = input('> (give {} to) '.format(item_name))
#
#		if not bad_syntax:
#			item_list = m_group.find_member_by_name(items, item_name)
#			target_list = m_group.find_member_by_name(people, target_name)
#			if m_group.check_target(item_list, items, item_name) == m_group.check_target(target_list, people, target_name) == m_group.e_target_type.unique:
#				event = player.give(*item_list, *target_list, world_time)
#				events.append(event)
#
#	# Syntax:
#	#	take ITEM from TARGET
#	if command[0] == 'take':
#		bad_syntax = False
#
#		if parameters:
#			from_delimiter = ' from '
#			from_location = parameters.rfind(' from ')
#			if from_location != -1:
#				item_name = parameters[:from_location].strip().lower()
#				target_name = parameters[from_location+len(from_delimiter):].strip().lower()
#			else:
#				bad_syntax = True
#				print("Incorrect syntax. Try: take ITEM from TARGET")
#		else:
#			print("What would you like to take?")
#			item_name = input('> (take) ')
#			print("Whom would you like to take it from?")
#			target_name = input('> (take {} from) '.format(item_name))
#
#		if not bad_syntax:
#			item_list = m_group.find_member_by_name(items, item_name)
#			target_list = m_group.find_member_by_name(people, target_name)
#			if m_group.check_target(item_list, items, item_name) == m_group.check_target(target_list, people, target_name) == m_group.e_target_type.unique:
#				event = player.take(*item_list, *target_list, world_time)
#				events.append(event)
#
#	# Syntax:
#	#	laugh
#	if command[0] == 'laugh':
#		bad_syntax = False
#
#		if parameters:
#			bad_syntax = True
#			print("Incorrect syntax. Try: laugh")
#
#		if not bad_syntax:
#			event = player.laugh(world_time)
#			events.append(event)

	world_time += 1
