from enum import Enum, unique
import pdb

events = []
world_time = 0

def find_member_by_name(group, name):
	target = [member for member in group if member.name == name]
	return target

class item:
	def __init__(self, name, description):
		self.name = name
		self.description = description
class container:
	def __init__(self, name, capacity):
		self.name = name
		self.capacity = capacity
		self.contents = []

#inventory = container("inventory", 10)
#inventory.contents.append(item("torch", "a piece of wood with an oil-soaked rag attached to one end"))

@unique
class e_action(Enum):
	kill = 0,
	tell = 1,

class event:
	def __init__(self, agent, patient, action, time):
		self.agent = agent
		self.patient = patient
		self.action = action
		self.time = time

@unique
class e_status(Enum):
	dead = 0
	alive = 1

class person:
	def __init__(self, name):
		self.name = name.lower()
		self.status = e_status.alive
#		self.memories = [] # Maybe once we get more advanced
	def kill(self, target):
		if target.status == e_status.alive:
			target.status = e_status.dead
			events.append(event(self, target, e_action.kill, world_time))
			print("{} killed {} at {} o'clock.".format(self.name, target.name, world_time))
		else:
			print("{} is already dead.".format(target.name))
	def tell(self, target, utterance):
		events.append(event(self, target, e_action.tell, world_time))
		print("{} told {} \"{}\" at {} o'clock.".format(self.name, target.name, utterance, world_time))

people = []

people.append(person("tyler"))
player = people[-1]

people.append(person("john"))
people.append(person("mary"))

def check_target(action, target, *args):
	# (SELF) The name of this function is a bit ambiguous and/or not really describing what it does completely.	
	target_count = len(target)

	if target_count == 0:
		print("That person ({}) doesn't exist.".format(target_name))
	elif target_count > 1:
		print("That name ({}) is ambiguous.".format(target_name))
	if target_count == 1:
		# Target with the given name exists and it's unique.
		#player.kill(*target)	
		action(*target, *args)

text_input = ""
while text_input != "q":
	text_input = input('> ')

	text_input.strip()
	text_input.lower()
	command = text_input.split(' ', 1)
	action = command[0]
	parameters = []
	if len(command) == 2:
		parameters = command[1]

	# Syntax:
	#	kill TARGET
	if command[0] == "kill":
		if parameters:
			target_name = parameters
		if not parameters:
			print("Who would you like to kill?")
			target_name = input('> (kill) ')

		target = find_member_by_name(people, target_name)
		check_target(player.kill, target)

	# Syntax:
	#	tell TARGET "UTTERANCE"
	if command[0] == "tell":
		bad_syntax = False

		if parameters:
			if parameters.count('\"') == 2:
				# We've got one and only one valid quote-enclosed utterance.
				# Now let's take a slice of everything before that and use that as the target name
				opening_quote = parameters.find('\"')
				closing_quote = parameters.rfind('\"')
				target_name = parameters[:opening_quote].rstrip()
				# (SELF) Why is it +1 for opening_quote but nothing for closing_quote? It works, but I don't know why
				utterance = parameters[opening_quote+1 : closing_quote]
			else:
				bad_syntax = True
				print("Incorrect syntax. Try: tell TARGET \"UTTERANCE\"")
		else:
			print("Who would you like to tell?")
			target_name = input('> (tell) ')
			print("What would you like to say?")
			utterance = input('> (tell {}) '.format(target_name))

		if not bad_syntax:
			target = find_member_by_name(people, target_name)
			check_target(player.tell, target, utterance)

	# Syntax:
	#	

	world_time += 1
		
'''
	if(command == "i"):
		print("your inventory contains:")
		for item in inventory.contents:
			print("\t" + item.name)
'''