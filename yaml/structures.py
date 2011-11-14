"""
Custom supporting data structures for Haikw
"""

# TODO: This is a little messy
class DictionarySet:
	"""
	An adapted dictionary-like structure without redefining keys

	A dictionary-like structure that does not allow for overwritting key values without expressly deleting them first
	"""

	def __init__(self):
		""" Constructor for DictionarySet """
		self.__internal_dict = {}
	
	def __getitem__(self, key):
		return self.__internal_dict[key]
	
	def __setitem__(self, key, value):
		if key in self.__internal_dict:
			raise AttributeError("Key already present")
		
		self.__internal_dict[key] = value
	
	def __delitem__(self, key):
		del self.__internal_dict[key]
	
	def keys(self):
		return self.__internal_dict.keys()