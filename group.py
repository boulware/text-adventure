from enum import Enum, unique

class Group(list):
	def __init__(self, member_title):
		self.member_title = member_title # The general term that can be used for a member of the group (e.g., "person" for a group of people)

def find_member_by_name(group, name):
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