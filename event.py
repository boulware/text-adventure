import re

from enum import Enum, unique
import verb as m_verb

class Event:
	#def __init__(self, time, verb, agent, patient = None, recipient = None):
	def __init__(self, time, verb, **roles):
		self.time = time
		self.verb = verb
		self.roles = roles

	def __str__(self):
		event_string = m_verb.sub_roles(self.verb, self.roles)
		return '[{}:00] {}'.format(self.time, event_string)
