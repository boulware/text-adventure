from enum import Enum, unique

class Event:
	def __init__(self, time, agent, action, patient = None, recipient = None):
		self.agent = agent
		self.action = action
		self.time = time
		self.patient = patient
		self.recipient = recipient