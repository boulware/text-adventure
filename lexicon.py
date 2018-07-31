import json

class Lexicon:
	def __init__(self, nouns_filename, verbs_filename, adjectives_filename):
		with open(nouns_filename) as file:
			data = json.load(file)
			self.nouns = data["nouns"]
		with open(verbs_filename) as file:
			data = json.load(file)
			self.verbs = data["verbs"]
		with open(adjectives_filename) as file:
			data = json.load(file)
			self.adjectives = data["adjectives"]