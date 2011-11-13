"""
Module containing classes related to the manipulation of objects in the target inverse kinematics package

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""
import os

class ObjectManipulationFactory:
	"""
	Factory singleton to configure and create an ObjectManipuationFactory along with its supporting parts
	"""

	__instance = None

	CONFIG_DIRECTORY = "." + os.sep + "config" + os.sep
	DEFAULT_TYPES_FILE = CONFIG_DIRECTORY + "types.yaml"
	DEFAULT_COLORS_FILE = CONFIG_DIRECTORY + "colors.yaml"
	DEFAULT_SIZES_FILE = CONFIG_DIRECTORY + "sizes.yaml"

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of ObjectManipulationFactory, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: ObjectManipulationFactory
		"""
		if not ObjectManipulationFactory.__instance:
			ObjectManipulationFactory.__instance = ObjectManipulationFactory()
		
		return ObjectManipulationFactory.__instance

	def __init__(self):
		"""
		Constructor for an ObjectManipulationFactory
		"""
		self.__object_constructions_strategies = {}
	
	def add_object_construction_strategy(self, package, strategy):
		"""
		Creates a new package specific strategy for creating virtual objects

		@param package: The name of package the following strategy supports
		@type package: String
		@param strategy: An instance of the target strategy
		@type strategy: Instance of a subclass of VirtualObjectConstructionStrategy
		"""
		self.__object_constructions_strategies[package] = strategy
	
	def get_available_manipulation_facade_types(self):
		"""
		Provies a list of packages currently supported by this manipulation factory

		@return: List of inverse kinematics packages currently supported
		@rtype: List of Strings
		"""
		return self.__object_constructions_strategies.keys()
	
	def create_facade(self, package, types_yaml_location=ObjectManipulationFactory.DEFAULT_TYPES_FILE, color_yaml_location=ObjectManipulationFactory.DEFAULT_COLORS_FILE, sizes_yaml_location=ObjectManipulationFactory.DEFAULT_SIZES_FILE, default_position_yaml_file=ObjectManipulationFactory.DEFAULT_POSITIONS_FILE):

		pass