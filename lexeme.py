import json

class Lexeme:
	def __init__(self, lemma, inflections):
		self.lemma = lemma
		self.inflections = inflections
		# with open(lexemes_filename) as file:
		# 	lexemes = json.load(file)['lexemes']

		# 	for lexeme in lexemes:
		# 		self.lexemes = 
