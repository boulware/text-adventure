from enum import Enum, unique

import event as m_event
import ipdb

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
		self.parameters = find_parameters(syntax)

	def _check_preconditions(self, agent, patient):
		if not agent:
			return False

		return True

	def _set_postconditions(self, agent, patient):
		pass

	def do(self, agent, parameter_string, time):
		bad_syntax = False

		if parameter_string:
			pass
			# ex: give torch to john
			#	parameter_string = "torch to john"
			# we need to find the first occurence of the first keyword (if there is a keyword in the syntax).



# This whole thing is kind of a mess. I'm gonna try something more like a real parser with push/pop stack stuff.
	#			location = 0 # Our current location (index) in the string. We do a simple left to right parse for now.
	#			parameter_location = 0 # Current index of parameters list
	#
	#			while location >= 0:
	#				keyword = ''
	#				reference = ''
	#				for index, parameter in enumerate(self.parameters[parameter_location:]):
	#					#print("searching ({})".format(parameter))
	#					if parameter[0] == e_parameter_type.keyword:
	#						keyword = parameter[1]
	#						parameter_location = index + 1
	#						break
	#				if keyword:
	#					#ipdb.set_trace()
	#					keyword_location = parameter_string.find(keyword)
	#					if keyword_location != -1:
	#						reference = parameter_string[location : parameter_string.find(keyword) - 1]
	#						location += len(reference) + len(keyword) + 2 # two spaces
	#						if location < len(parameter_string):
	#							list_ = list(parameter_string)
	#							list_[location] = "*"
	#							str_ = "".join(list_)
	#							print("current position: {}".format(str_))
	#						print("reference: \"{}\"; keyword: \"{}\"".format(reference, keyword))
	#						if location > len(parameter_string):
	#							location = -1
	#					else:
	#						print("Invalid syntax. Try: {}".format(self.syntax))
	#				else:
	#					# We've reached the end (assuming we can't end with more than one consecutive reference with no keywords)
	#					reference = parameter_string[location:]
	#					location = -1

				#print("reference: \"{}\"; keyword: \"{}\"".format(reference, keyword))



		if not bad_syntax:
			if self._check_preconditions(agent, None):
				self._set_postconditions(agent, None)
				return m_event.Event(time, agent, self)

		return None

def find_parameters(syntax):
	parameters = []
	for index, word in enumerate(syntax.split()):
		if index == 0:
			parameters.append((e_parameter_type.command, word))
		elif word.isupper():
			parameters.append((e_parameter_type.reference, word))
		elif word.islower():
			parameters.append((e_parameter_type.keyword, word))


	return parameters