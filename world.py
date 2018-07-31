from group import Group

from person import Person
from item import Item
from verb import Verb
from action import Action
from state import State
from event import Event
from lexeme import Lexeme


class World:
	def __init__(self):
		self.lexemes = Group('lexeme', Lexeme, 'data/lexemes.dat')
		self.people = Group('person', Person, 'data/people.dat')
		self.items = Group('item', Item, 'data/items.dat')
		self.verbs = Group('verb', Verb, 'data/verbs.dat')
		self.actions = Group('action', Action, 'data/actions.dat')
		self.states = Group('state', State, 'data/states.dat', **{'verbs_group': self.verbs})

		self.events = Group('event', Event)

def print_states(world):
	print("States:")
	for state in world.states:
		print('\t{}.'.format(state))

def print_events(world):
	print("Events:")
	for event in world.events:
		print('\t{}.'.format(event))