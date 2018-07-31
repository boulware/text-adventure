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

class Verb:
	def __init__(self, lemma, inflection, syntax, is_stative, preconditions=[]):
		self.name = self.lemma = lemma
		self.inflection = inflection
		self.syntax = syntax
		self.is_stative = is_stative

		self.regex, self.roles = parse_syntax(self, syntax)

		for precondition in preconditions:
			pass

def match_regex(verb, action_string):
	bad_syntax = False

	match = verb.regex.fullmatch(action_string)
	if not match:
		print("Invalid syntax. Try: \'{}\'".format(verb.syntax))
		print("Regex pattern: \'{}\'".format(verb.regex.pattern))
		print("Action string: \'{}\'".format(action_string))
		bad_syntax = True

	return bad_syntax, match

def do(verb, action_string, time, verbs_group):
	bad_syntax, match = match_regex(verb, action_string)

	# (NOTE) agent, patient, recipient is kind of cryptic. It might be better
	# in the long run to switch to some thing more generic, but it could also
	# be a useful classification for pre- and post-conditions

	if not bad_syntax:
		params = match.groupdict()
		roles_dict = {i:params[i] for i in params if i != 'VERB'}
		
		event_string = sub_roles(verb, roles_dict)

		if verb.is_stative:
			print("{}.".format(event_string))
			return State(verb.lemma, roles_dict, verbs_group=verbs_group) # (TODO) Hacky solution using verb.lemma to have cross-support with file loading
		else:
			print("{} at {} o'clock.".format(event_string, time))
			return m_event.Event(time, verb, roles_dict)

	return None

def sub_roles(verb, roles_dict):
	subbed_string = verb.syntax

	subbed_string = re.sub('\*', verb.inflection, subbed_string)
	for role_name, role_value in roles_dict.items():
		if role_value:
			subbed_string = re.sub(role_name.upper(), role_value, subbed_string)

	return subbed_string

def parse_syntax(verb, syntax):
	parameters = []
	roles = []

	pattern = ''
	first = True
	for word in syntax.split():
		if word == "*":
			pattern += '\s+(?P<VERB>{})'.format(verb.lemma) # (TODO) Change the syntax to allow direct writing of the verb form in instead of '*' so it reads more naturally.
			parameters.append(Parameter(ParameterType.Command, "VERB"))
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
