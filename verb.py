import re

import group as m_group
from state import State
import event as m_event

class Verb:
	def __init__(self, lemma, inflection, syntax, is_stative):
		self.name = self.lemma = lemma
		self.inflection = inflection
		self.syntax = syntax
		self.is_stative = is_stative

		self.regex = find_regex(self, syntax)


def do(verb, action_string, time, verbs_group):
	print("action_string={}".format(action_string))

	bad_syntax = False

	match = verb.regex.fullmatch(action_string)
	if not match:
		print("Invalid syntax. Try: \'{}\'".format(verb.syntax))
		print("Regex pattern: \'{}\'".format(verb.regex.pattern))
		print("action string: \'{}\'".format(action_string))
		bad_syntax = True

	# (NOTE) agent, patient, recipient is kind of cryptic. It might be better
	# in the long run to switch to some thing more generic, but it could also
	# be a useful classification for pre- and post-conditions

	if not bad_syntax:
		params = match.groupdict()
		roles = {i:params[i] for i in params if i != 'VERB'}

		event_string = sub_roles(verb, roles)

		if verb.is_stative:
			print("{}.".format(event_string))
			return State(verb.lemma, roles, verbs_group=verbs_group) # (TODO) Hacky solution using verb.lemma to have cross-support with file loading
		else:
			print("{} at {} o'clock.".format(event_string, time))
			return m_event.Event(time, verb, **roles)

	return None

def sub_roles(verb, roles):
	subbed_string = verb.syntax

	subbed_string = re.sub('\*', verb.inflection, subbed_string)
	for role_name, role_value in roles.items():
		if role_value:
			subbed_string = re.sub(role_name.upper(), role_value, subbed_string)

	return subbed_string	

def find_regex(verb, syntax):
	pattern = ''
	first = True
	for word in syntax.split():
		if word == "*":
			pattern += '\s+(?P<VERB>{})'.format(verb.lemma) # (TODO) Change the syntax to allow direct writing of the verb form in instead of '*' so it reads more naturally.
		elif word.isupper():
			pattern += '\s+(?P<{}>.*)'.format(word)
		elif word.islower():
			pattern += '\s+' + word

		if first:
			first = False
			pattern = pattern[len('\s+'):] # (TEMP) Get rid of \s+ if it's the first element.

	pattern = pattern.strip()

	if not pattern:
		print("Empty syntax encountered.") # (TODO) This should probably be dealt with in a better way.

	return re.compile(pattern)