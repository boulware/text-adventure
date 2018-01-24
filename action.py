from enum import Enum, unique

from event import Event
import group as m_group
import ipdb

import re

@unique
class e_parameter_type(Enum):
	command = 0 # The textual command associated with the Action. e.g., command="give" for the give Action
	reference = 1 # A parameter that is eventually replaced with a reference to an object
	keyword = 2 # A parameter that serves only to contextualize surrounding references. e.g., "to" in "give ITEM to TARGET"

class Parameter:
	def __init__(self, user_query):
		self.user_query = user_query

class Action:
	def __init__(self, syntax):
		self.syntax = syntax
		self.command, self.regex = find_regex(syntax)
		self.name = self.command # (TEMP) holdover for Group functions using "name" instead of something more generic

	def _check_preconditions(self, agent, patient):
		if not agent:
			return False

		return True

	def _set_postconditions(self, agent, patient):
		pass

	def do(self, agent, argument_string, time, verbs):
		bad_syntax = False

		match = self.regex.fullmatch(argument_string)
		if not match:
			print("Invalid syntax. Try: \'{}\'".format(self.syntax))
			print("Regex pattern: \'{}\'".format(self.regex.pattern))
			print("Argument string: \'{}\'".format(argument_string))
			bad_syntax = True

		if not bad_syntax:
			if self._check_preconditions(agent, None):
				self._set_postconditions(agent, None)
				verb = m_group.find_member_by_name(verbs, self.name)
				if verb:
					print("{} {}{} at {} o'clock.".format(agent.name, verb.past, argument_string, time))
				else:
					print("Verb not found for command \'{}\'".format(self.command))
				return Event(time, agent, self)

		return None

def find_regex(syntax):
	command = ''
	pattern = ''
	first = True
	for word in syntax.split():
		if first == True:
			first = False
			command = word
		elif word.isupper():
			pattern += '\s+(?P<{}>.*)'.format(word)
		elif word.islower():
			pattern += '\s+' + word

	pattern = pattern.strip()

	if not command:
		print("Empty syntax encountered.") # (TODO) This should probably be dealt with in a better way.

	#print("syntax=\'{}\'; pattern=\'{}\'".format(syntax, pattern))
	return command, re.compile(pattern)