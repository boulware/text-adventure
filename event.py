from enum import Enum, unique

class Event:
	def __init__(self, time, agent, verb, patient = None, recipient = None):
		self.time = time
		self.agent = agent
		self.verb = verb
		self.patient = patient
		self.recipient = recipient