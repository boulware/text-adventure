from enum import Enum, unique
import event as m_event

@unique
class e_status(Enum):
	dead = 0
	alive = 1

class Person:
	def __init__(self, name):
		self.name = name.lower()
		self.status = e_status.alive
#		self.memories = [] # Maybe once we get more advanced
	def kill(self, target, time):
		if target.status == e_status.alive:
			event = m_event.Event(time, self, m_event.e_action.kill, target)

			target.status = e_status.dead
			print("{} killed {} at {} o'clock.".format(self.name, target.name, time))
		else:
			event = m_event.null_event

			print("{} is already dead.".format(target.name))

		return event

	def tell(self, target, utterance, time):
		event = m_event.Event(time, self, m_event.e_action.tell, target)
		print("{} told {} \"{}\" at {} o'clock.".format(self.name, target.name, utterance, time))
		return event

	def give(self, item, target, time):
		event = m_event.Event(time, self, m_event.e_action.give, item, target)
		print("{} gave {} to {} at {} o'clock.".format(self.name, item.name, target.name, time))
		return event

	def take(self, item, target, time):
		event = m_event.Event(time, self, m_event.e_action.take, item, target)
		print("{} took {} from {} at {} o'clock.".format(self.name, item.name, target.name, time))
		return event

	def laugh(self, time):
		event = m_event.Event(time, self, m_event.e_action.laugh)
		print("{} laughed at {} o'clock.".format(self.name, time))
		return event