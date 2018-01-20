import event as m_event
import person as m_person

class Parameter:
	def __init__(self, user_query):
		self.user_query = user_query


class Action:
	def __init__(self, command, ID, syntax):
		self.command = command
		self.ID = ID
		self.syntax = syntax
		self.parameters = []

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
				return m_event.Event(time, agent, self.ID)

		return None