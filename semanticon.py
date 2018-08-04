from enum import Enum, unique
import json

@unique
class SemantType(Enum):
	Object = 0
	Action = 1
	State = 2
	Property = 3
	Quality = 4
	Relationship = 5
	Connection = 6
	Determination = 7

def LoadDataFile(filename):
	try:
		with open(filename) as file:
			data = json.load(file)
			return data
	except FileNotFoundError:
		print("Tried to open data file ({}), but it does not exist.".format(filename))

class Semanticon:
	def __init__(self, semants_filenames = {}):
		self.semants = {}
		for semant_type, filename in semants_filenames.items():
			self.semants[semant_type] = LoadDataFile(filename)

