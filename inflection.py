from enum import Enum, unique
import re

@unique
class InflectionType(Enum):
	Infinitive = "infinitive"
	Imperative = "imperative"
	Participle = "participle"
	Indicative = "indicative"

@unique
class InflectionTense(Enum):
	Past = "past"
	Present = "present"
	Future = "future"

@unique
class InflectionNumber(Enum):
	Singular = "singular"
	Plural = "plural"

@unique
class InflectionPerson(Enum):
	First = 0
	Second = 1
	Third = 2

class InflectionModel():
	def __init__(self, name, rules):
		self.name = name
		self.rules = rules

class Inflection():
	def __init__(self, type_=None, tense=None, number=None, person=None):
		self.parameters = [type_, tense, number, person]

def inflect(model, word_text, inflection):
	sub_rule = model.rules
	for parameter in inflection.parameters:
		if not parameter:
			print("Incomplete inflection given for inflection model: {}".format(model.name))

		sub_rule = sub_rule[parameter.value]

		if isinstance(sub_rule, str):
			break

	return sub_rule.replace('*', word_text)