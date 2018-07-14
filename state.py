import re

import group as m_group
import verb as m_verb

class State:
	def __init__(self, verb_string, roles, verbs_group):
		self.verb = m_group.find_member_by_name(verbs_group, verb_string)
		self.roles = roles

	def __str__(self):
		return m_verb.sub_roles(self.verb, self.roles)