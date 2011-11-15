"""
Module for loading configuration settings

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

import os
import yaml

class PathFixer:
	"""
	Simple singleton that changes the forward slash to the os seperator appropriate to the current platform
	"""

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of PathFixer, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: PathFixer
		"""
		if not PathFixer.__instance:
			PathFixer.__instance = PathFixer()
		
		return PathFixer.__instance
	
	def fix(self, path):
		"""
		Changes a unix style path to a path compatable with the current operating system

		@param path: The path to change
		@type path: String
		@return: New os specific path
		@rtype: String
		"""
		return path.replace("/", os.sep)

class YamlReaderFactory:
	"""
	Factory singleton that provides an implementation of YamlReader
	"""

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of YamlReaderFactory, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: YamlReaderFactory
		"""
		if not YamlReaderFactory.__instance:
			YamlReaderFactory.__instance = YamlReaderFactory()
		
		return YamlReaderFactory.__instance
	
	def __init__(self):
		pass
	
	def get_reader(self):
		"""
		Returns an implementation of YamlReader

		@return: Instance of a subclass of YamlReader
		@rtype: YamlReader subclass instance
		"""
		return PyYamlAdapter.get_instance()

class YamlReader:
	"""
	A simple interface for reading YAML strings

	@note: This is fully abstract. Client code should use a subclass. 
	"""

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of this YamlReader

		@return: Shared instance of YamlReader
		@rtype: YamlReader
		"""
		raise NotImplementedError("Must use a subclass / implementor of this interface")

	def __init__(self):
		raise NotImplementedError("Must use a subclass / implementor of this interface")
	
	def load(self, src):
		"""
		Converts the provided YAML encoded file to Python native objects

		@param src: Path to the file to read from
		@type src: String
		@return: Converted Python values
		@rtype: Python objects
		"""
		raise NotImplementedError("Must use a subclass / implementor of this interface")
		
	def loads(self, str):
		""" 
		Converts the provided YAML encoded string to Python native objects

		@param str: The string to convert
		@type str: String
		@return: Converted Python values
		@rtype: Python objects
		"""
		raise NotImplementedError("Must use a subclass / implementor of this interface")
	
class PyYamlAdapter(YamlReader):
	"""
	Adapts PyYAML library to be an implementation of YamlReader
	"""

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of this PyYamlAdapter

		@return: Shared instance of PyYamlAdapter
		@rtype: PyYamlReader
		"""
		if not PyYamlAdapter.__instance:
			PyYamlAdapter.__instance = PyYamlAdapter()
		
		return PyYamlAdapter.__instance

	def __init__(self):
		YamlReader.__init__(self)
	
	def loads(self, string):
		""" 
		Converts the provided YAML encoded string to Python native objects

		@param string: The string to convert
		@type string: String
		@return: Converted Python values
		@rtype: Python objects
		"""
		yaml.load(string)
	
	def load(self, src):
		"""
		Converts the provided YAML encoded file to Python native objects

		@param src: Path to the file to read from
		@type src: String
		@return: Converted Python values
		@rtype: Python objects
		"""
		target = open(src, "rb")
		orig_contents = target.read()
		converted_contents = yaml.load(orig_contents)
		target.close()
		return converted_contents