from enum import Enum, unique
import re
from collections import namedtuple

import group as m_group
from state import State
import event as m_event

@unique
class ParameterType(Enum):
	Command = 0 # The textual command associated with the Action. e.g., command="give" for the give Action
	Reference = 1 # A parameter that is eventually replaced with a reference to an object
	Keyword = 2 # A parameter that serves only to contextualize surrounding references. e.g., "to" in "give ITEM to TARGET"

Parameter = namedtuple('Parameter', 'type name')

class SemanticAction:
	def __init__(self, lemma, inflection, syntax, preconditions=[], postconditions=[]):
		self.name = self.lemma = lemma
		self.inflection = inflection
		self.syntax = syntax

		self.regex, self.roles = parse_syntax(self, syntax)

		for precondition in preconditions:
			pass

def match_regex(semantic_action, semantic_action_string):
	bad_syntax = False

	match = semantic_action.regex.fullmatch(semantic_action_string)
	if not match:
		print("Invalid syntax. Try: \'{}\'".format(semantic_action.syntax))
		print("Regex pattern: \'{}\'".format(semantic_action.regex.pattern))
		print("semantic_action string: \'{}\'".format(semantic_action_string))
		bad_syntax = True

	return bad_syntax, match

def do(semantic_action, semantic_action_string, time, semantic_actions_group):
	bad_syntax, match = match_regex(semantic_action, semantic_action_string)

	# (NOTE) agent, patient, recipient is kind of cryptic. It might be better
	# in the long run to switch to some thing more generic, but it could also
	# be a useful classification for pre- and post-conditions

	if not bad_syntax:
		params = match.groupdict()
		roles_dict = {i:params[i] for i in params if i != 'VERB'}
		
		event_string = sub_roles(semantic_action, roles_dict)

		if semantic_action.is_stative:
			print("{}.".format(event_string))
			return State(semantic_action.lemma, roles_dict, semantic_actions_group=semantic_actions_group) # (TODO) Hacky solution using semantic_action.lemma to have cross-support with file loading
		else:
			print("{} at {} o'clock.".format(event_string, time))
			return m_event.Event(time, semantic_action, roles_dict)

	return None

def sub_roles(semantic_action, roles_dict):
	subbed_string = semantic_action.syntax

	subbed_string = re.sub('\*', semantic_action.inflection, subbed_string)
	for role_name, role_value in roles_dict.items():
		if role_value:
			subbed_string = re.sub(role_name.upper(), role_value, subbed_string)

	return subbed_string

def parse_syntax(semantic_action, syntax):
	parameters = []
	roles = []

	pattern = ''
	first = True
	for word in syntax.split():
		if word == "*":
			pattern += '\s+(?P<VERB>{})'.format(semantic_action.lemma) # (TODO) Change the syntax to allow direct writing of the semantic_action form in instead of '*' so it reads more naturally.
			parameters.append(Parameter(ParameterType.Command, "verb"))
		elif word.isupper():
			pattern += '\s+(?P<{}>.*)'.format(word)
			parameters.append(Parameter(ParameterType.Reference, word))
			roles.append(word)
		elif word.islower():
			pattern += '\s+' + word
			parameters.append(Parameter(ParameterType.Keyword, word))

		if first:
			first = False
			pattern = pattern[len('\s+'):] # (TEMP) Get rid of \s+ if it's the first element.

	pattern = pattern.strip()

	if not pattern:
		print("Empty syntax encountered.") # (TODO) This should probably be dealt with in a better way.

	return re.compile(pattern), roles

def parse_condition(condition_string, roles):
	for word in condition_string.split():
		if word.isupper():
			pass
			# Word is a reference
		else:
			pass


# from enum import Enum, unique

# from event import Event
# import group as m_group
# import ipdb

# import re

# class Parameter:
# 	def __init__(self, user_query):
# 		self.user_query = user_query

# class Action:
# 	def __init__(self, syntax):
# 		self.syntax = syntax
# 		self.command, self.regex = find_regex(syntax)
# 		self.name = self.command # (TEMP) holdover for Group functions using "name" instead of something more generic

# 	def _check_preconditions(self, agent, patient):
# 		if not agent:
# 			return False

# 		return True

# 	def _set_postconditions(self, agent, patient):
# 		pass

# 	def do(self, agent, argument_string, time, verbs):
# 		bad_syntax = False

# 		match = self.regex.fullmatch(argument_string)
# 		if not match:
# 			print("Invalid syntax. Try: \'{}\'".format(self.syntax))
# 			print("Regex pattern: \'{}\'".format(self.regex.pattern))
# 			print("Argument string: \'{}\'".format(argument_string))
# 			bad_syntax = True

# 		if not bad_syntax:
# 			if self._check_preconditions(agent, None):
# 				self._set_postconditions(agent, None)
# 				verb = m_group.find_member_by_name(verbs, self.name)
# 				if verb:
# 					print("{} {}{} at {} o'clock.".format(agent.name, verb.past, argument_string, time))
# 				else:
# 					print("Verb not found for command \'{}\'".format(self.command))
# 				return Event(time, agent, self)

# 		return None

# def find_regex(syntax):
# 	command = ''
# 	pattern = ''
# 	first = True
# 	for word in syntax.split():
# 		if first == True:
# 			first = False
# 			command = word
# 		elif word.isupper():
# 			pattern += '\s+(?P<{}>.*)'.format(word)
# 		elif word.islower():
# 			pattern += '\s+' + word

# 	pattern = pattern.strip()

# 	if not command:
# 		print("Empty syntax encountered.") # (TODO) This should probably be dealt with in a better way.

# 	return command, re.compile(pattern)