from enum import Enum, unique

@unique
class e_action(Enum):
	none = 0,
	kill = 1,
	tell = 2,
	give = 3,
	take = 4,
	laugh = 5,

class Event:
	def __init__(self, time, agent, action, patient = None, recipient = None):
		self.agent = agent
		self.action = action
		self.time = time
		self.patient = patient
		self.recipient = recipient

null_event = Event(None, None, None)