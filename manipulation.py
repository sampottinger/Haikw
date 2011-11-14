"""
Module containing classes related to the manipulation of objects in the target inverse kinematics package

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""
import os
import loaders

class ObjectManipulationFactory:
	"""
	Factory singleton to configure and create an ObjectManipuationFacade along with its supporting parts
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
		self.__object_construction_strategies = {}
	
	def add_object_construction_strategy(self, package, strategy):
		"""
		Creates a new package specific strategy for creating virtual objects

		@param package: The name of package the following strategy supports
		@type package: String
		@param strategy: An instance of the target strategy
		@type strategy: Instance of a subclass of VirtualObjectConstructionStrategy
		"""
		self.__object_construction_strategies[package] = strategy
	
	def get_available_manipulation_facade_types(self):
		"""
		Provies a list of packages currently supported by this manipulation factory

		@return: List of inverse kinematics packages currently supported
		@rtype: List of Strings
		"""
		return self.__object_construction_strategies.keys()
	
	def create_facade(self, package, color_yaml_location=ObjectManipulationFactory.DEFAULT_COLORS_FILE, sizes_yaml_location=ObjectManipulationFactory.DEFAULT_SIZES_FILE, default_positions_yaml_file=ObjectManipulationFactory.DEFAULT_POSITIONS_FILE):
		"""
		Creates a new ObjectManipulationFacade given the configuration files and packages

		@param package: The name of the software package to target
		@type package: String
		@param color_yaml_location: Path to the yaml file containing information about the default named colors to use in building objects
		@type color_yaml_location: String
		@param sizes_yaml_location: Path to the yaml file containing information about about the default named sizes to use in building objects
		@type sizes_yaml_location: String
		@param default_positions_yaml_file: Path to the yaml file containing information about the default named positions to use in placing objects
		@type default_positions_yaml_file: String
		@raise ValueError: Raised if a strategy is requested for a package that has not been adapted or if that adapter has not been registered (see add_object_construction_strategy)
		"""

		# Determine construction factory
		if not package in self.__object_construction_strategies:
			raise ValueError(package + " has not been registered as an inverse kinematics package")
		creation_strategy = self.__object_construction_strategies[package]

		# Read from configuration files
		colors = self.__read_from_yaml_file(color_yaml_location)
		sizes = self.__read_from_yaml_file(sizes_yaml_location)
		positions = self.__read_from_yaml_file(default_positions_yaml_file)

		#return ObjectManipulationFacade()

	def __read_from_yaml_file(self, target):
		"""
		Helper function to read and convert the contents of a YAML file

		@param target: Path to the file to read
		@type target: String
		"""
		reader = loaders.YamlReaderFactory.get_instance()
		return reader.load(target)

class ObjectManipulationFacade:
	"""
	Driver for management and manipulation of virutal objects

	Facade that drives the creation of new and manipulation of existing objects in an inverse kinematics package
	
	@note: Should not be created directly. Use an ObjectManipulationFactory to construct.
	"""

	def __init__(self, creation_strategy, color_resolution_strategy, named_size_resolver, object_position_factory):
		"""
		Constructor for ObjectManipulationFacade

		@param creation_strategy: The strategy to use to create new package-specific objects
		@type creation_strategy: VirtualObjectBuilder
		@param named_size_resolver: The strategy to use to resolve names of sizes to actual sizes
		@type named_size_resolver: NamedSizeResolver
		@param object_position_factory: Factory to create positions
		@type object_position_factory: ObjectPositionFactory
		"""

		pass