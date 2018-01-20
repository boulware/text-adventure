import event as m_event
import person as m_person

class Parameter:
	def __init__(self, user_query):
		self.user_query = user_query

class Action:
	def __init__(self, syntax):
		self.syntax = syntax
		self.command, self.parameters = find_parameters(syntax)

	def _check_preconditions(self, agent, patient):
		if not agent:
			return False

		return True

	def _set_postconditions(self, agent, patient):
		pass

	def do(self, agent, parameter_string, time):
		bad_syntax = False

		if parameter_string:
			bad_syntax = True
			print("Incorrect syntax. Try: {}".format(self.syntax))

		if not bad_syntax:
			if self._check_preconditions(agent, None):
				self._set_postconditions(agent, None)
				return m_event.Event(time, agent, self)

		return None

def find_parameters(syntax):
	command = ''
	parameters = []
	for index, word in enumerate(syntax.split()):
		if index == 0:
			command = word

		if word.isupper():
			parameters.append(word)

	return command, parameters