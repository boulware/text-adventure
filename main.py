import group as m_group
import event as m_event
import person as m_person
import item as m_item
import action as m_action

import ipdb

events = []
world_time = 0

people = m_group.Group('person')
people.append(m_person.Person('tyler'))
player = people[-1]
people.append(m_person.Person('john'))
people.append(m_person.Person('mary'))

items = m_group.Group('item')
items.append(m_item.Item('torch'))

jump = m_action.Action('jump')
hug = m_action.Action('hug TARGET')
give = m_action.Action('give ITEM to TARGET')
walk = m_action.Action('walk to LOCATION')
crazy = m_action.Action('crazy A to B while C and D')
doubleref = m_action.Action('doubleref A to B C and D')
doublekw = m_action.Action('doublekw A to B and or C for D')
emptycmd = m_action.Action('')

text_input = ''
while text_input != 'q':
	text_input = input('> ')
	text_input = text_input.strip() # (SELF) This is an important line. Without it, our regex will break. Think carefully before removing it.
	text_input = text_input.lower()

	command, _, arguments = text_input.partition(' ')

	#print("command=\'{}\'; arguments=\'{}\'".format(command, arguments))

	# Syntax:
	#	jump
	if command == 'jump':
		event = jump.do(player, text_input, world_time)
		if event:
			events.append(event)

	# Syntax:
	#	hug TARGET
	if command == 'hug':
		event = hug.do(player, text_input, world_time)
		if event:
			events.append(event)

	# Syntax:
	#	give ITEM to TARGET
	if command == 'give':
		event = give.do(player, text_input, world_time)
		if event:
			events.append(event)

	if command == 'walk':
		event = walk.do(player, text_input, world_time)

	if command == 'crazy':
		event = crazy.do(player, 'crazy A to B while C and D or E', world_time)
		if event:
			events.append(event)

	if command == 'doubleref':
		event = doubleref.do(player, 'doubleref A to B C and D', world_time)
		if event:
			events.append(event)

	if command == 'doublekw':
		event = doublekw.do(player, 'doublekw A to B and or C for D', world_time)
		if event:
			events.append(event)

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

#	for i, event in enumerate(events):
#		print("event {}: {}".format(i, event.action))

	world_time += 1
