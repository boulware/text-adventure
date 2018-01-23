from enum import Enum, unique

import event as m_event
import ipdb
from collections import namedtuple

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
		self.name, self.regex = find_regex(syntax)

	def _check_preconditions(self, agent, patient):
		if not agent:
			return False

		return True

	def _set_postconditions(self, agent, patient):
		pass

	def do(self, agent, argument_string, time):
		bad_syntax = False

		match = self.regex.fullmatch(argument_string)
		if not match:
			print("Invalid syntax. Try: \'{}\'".format(self.syntax))
			print("Regex pattern: \'{}\'".format(self.regex.pattern))
			bad_syntax = True

		if not bad_syntax:
			if self._check_preconditions(agent, None):
				self._set_postconditions(agent, None)
				return m_event.Event(time, agent, self)

		return None

def find_regex(syntax):
	command = ''
	pattern = ''
	first = True
	for word in syntax.split():
		if first == True:
			first = False
			pattern += word
			command = word
		elif word.isupper():
			pattern += '\s+(.*)'
		elif word.islower():
			pattern += '\s+' + word

	if not pattern:
		print("Empty syntax encountered.")

	#print("syntax=\'{}\'; pattern=\'{}\'".format(syntax, pattern))
	return command, re.compile(pattern)