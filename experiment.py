"""
Module containing classes related to the management of experimental setups and robots

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""
import structures

class RobotPart:
	"""
	Description of a part belonging to a robot
	"""

	def __init__(self, name):
		"""
		Constructor for RobotPart

		@param name: The name of this part
		@type name: String
		"""
		self.__name = name
	
	def get_name(self):
		"""
		Determine the name of this robot part

		@return: The name of this part of a robot
		@rtype: String
		"""
		return self.__name

class Robot:
	"""
	Description of a robot and its parts

	@note: This is partially abstract and a package specific subclass should be used
	"""

	def __init__(self, name, parts, descriptor):
		"""
		Constructor for Robot

		@param name: The name of this robot
		@type name: String
		@param parts: List of parts of this robot
		@type parts: List / Tuple of RobotParts
		@param descriptor: Location of this robot's package-specific descritive file location / string
		"""
		self.__name = name
		self.__parts = tuple(parts)
		self.__descriptor = descriptor
	
	def get_name(self):
		"""
		Determines the name of this robot

		@return: The name assigned to this robot at construction
		@rtype: String
		"""
		return self.__name
	
	def get_parts(self):
		"""
		Determines which parts belong to this robot

		@return: The parts assigned to this robot
		@rtype: Tuple of RobotParts
		"""
		return self.__parts
	
	def get_state(self):
		"""
		Get a serializable representation of this robot's state such that it can be saved and restored

		@return: The robot's current state
		@rtype: Serializable Python collection
		"""
		raise NotImplementedError("Need subclass of this abstract class to preform this action")

class Setup:
	"""
	Serializable immutable state containing objects and their current positions
	"""

	def __init__(self, name, objects):
		"""
		Constructor for Setup

		@param name: The unique name of this setup
		@type name: String
		@param objects: The objects in this setup
		@type objects: List / Tuple of VirtualObjects
		@note: The name is unique in any given runtime
		"""
		self.__name = name
		self.__objects = tuple(objects)
	
	def get_objects(self):
		"""
		Return the objects in this setup

		@return: List of objects in this setup
		@rtype: Tuple of VirutalObjects
		"""
		return self.__objects
	
	def get_name(self):
		"""
		Determine the name of this setup

		@return: The name assigned to this setup at its creation
		@rtype: String
		"""
		return self.__name

class SetupManager:
	"""
	Manager specific to handeling virtual experimental setups
	"""

	def __init__(self):
		"""
		Constructor for SetupManager
		"""
		self.__setups = structures.DictionarySet()
	
	def get(self, name):
		"""
		Retrieves a named state from this manager's store

		@param name: The name of the state to restore
		@type name: String
		"""
		if not name in self.__setups:
			raise ValueError("A setup by that name has not been registered")
		
		return self.__setups[name]
	
	def add(self, setup):
		"""
		Adds a new setup to the store of available setups

		@param setup: The new setup to save
		@type setup: Setup
		"""
		self.__setups[setup.get_name()] = setup

class RobotManager:
	"""
	Manager specific to handling virtual robots
	"""

	def __init__(self):
		"""
		Constructor for RobotManager
		"""
		
		self.__robots = structures.DictionarySet()
	
	def get(self, name):
		"""
		Finds a robot by name

		@param name: The name of the robot to find
		@type name: String
		@return: The robot by the given name
		@rtype: Robot
		"""
		if not name in self.__robots:
			raise ValueError("A robot by that name has not been reigstered")
		
		return self.__robots[name]
	
	def add(self, robot):
		"""
		Adds a new robot to this manager

		@param robot: The new robot to save
		@type robot: Robot
		"""
		self.__robots[robot.get_name()] = robot