from enum import Enum, unique

@unique
class e_action(Enum):
	kill = 0,
	tell = 1,
	give = 2,
	take = 3,

class Event:
	def __init__(self, time, agent, action, patient = None, recipient = None):
		self.agent = agent
		self.action = action
		self.time = time
		self.patient = patient
		self.recipient = recipient

null_event = Event(None, None, None)