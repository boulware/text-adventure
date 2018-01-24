import re

import group as m_group

class Verb:
	def __init__(self, lemma, inflection, syntax):
		self.name = self.lemma = lemma
		self.inflection = inflection
		self.syntax = syntax
		self.regex = find_regex(syntax)


def do(verb, action_string, time):
	bad_syntax = False

	match = verb.regex.fullmatch(action_string)
	if not match:
		print("Invalid syntax. Try: \'{}\'".format(verb.syntax))
		print("Regex pattern: \'{}\'".format(verb.regex.pattern))
		print("action string: \'{}\'".format(action_string))
		bad_syntax = True

	if not bad_syntax:
		event_string = ''
		first = True
		for word in verb.syntax.split():
			if word == "*":
				event_string += ' {}'.format(verb.inflection)
			elif word.isupper():
				event_string += ' {}'.format(match.group(word))
			elif word.islower():
				event_string += ' {}'.format(word)

			if first:
				first = False
				event_string = event_string[1:]

		#print("{} {}{} at {} o'clock.".format(agent.name, verb.past, argument_string, time))
		print("{} at {} o'clock.".format(event_string, time))
		#return Event(time, agent, self)

	return None

def find_regex(syntax):
	pattern = ''
	first = True
	for word in syntax.split():
		if word == "*":
			pattern += '\s+(?P<VERB>.*)' # (TODO) Change the syntax to allow direct writing of the verb form in intead of '*' so it reads more naturally.
		elif word.isupper():
			pattern += '\s+(?P<{}>.*)'.format(word)
		elif word.islower():
			pattern += '\s+' + word

		if first:
			first = False
			pattern = pattern[len('\s+'):] # (TEMP) Get rid of \s+ if it's the first element.
			print(pattern)

	pattern = pattern.strip()

	if not pattern:
		print("Empty syntax encountered.") # (TODO) This should probably be dealt with in a better way.

	print("syntax=\'{}\'; pattern=\'{}\'".format(syntax, pattern))
	return re.compile(pattern)