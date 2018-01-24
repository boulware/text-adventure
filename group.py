from enum import Enum, unique
import json

class Group(list):
	def __init__(self, member_title, member_class, filepath):
		self.member_title = member_title # The general term that can be used for a member of the group (e.g., "person" for a group of people)
		self.member_class = member_class

		with open(filepath) as file:
			data = json.load(file)

			for _, members in data.items():
				for member in members:
					try:
						self.append(member_class(**member))
					except TypeError:
						print("Invalid {} encountered in {}.".format(member_title, filepath))

# (TEMP) This is a workaround to return only a single (first found) member intead of the more generic list return of find_members_by_name()
def find_member_by_name(group, name):
	for member in group:
		if member.name == name:
			return member

	print("Unable to find member {} in group {}.".format(name, group.member_title))

def find_members_by_name(group, name):
	target = [member for member in group if member.name == name]
	return target

@unique
class e_target_type(Enum):
	null = 0, 		# No target exists with the given specs
	ambiguous = 1,	# Multiple targets exist with the given specs
	unique = 2,		# Exactly one target exists with the given specs

def check_target(target, group, target_name):
	target_count = len(target)

	if target_count == 0:
		print("That {} ({}) doesn't exist.".format(group.member_title, target_name))
		return e_target_type.null
	elif target_count > 1:
		print("That {} name ({}) is ambiguous.".format(group.member_title, target_name))
		return e_target_type.ambiguous
	if target_count == 1:
		return e_target_type.unique