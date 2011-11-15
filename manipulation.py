"""
Module containing classes related to the manipulation of objects in the target inverse kinematics package

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""
import os
import imp
import configurable
import loaders
import structures

class PackageManager:
	"""
	Deals with varying inverse kinetmatics packages and their configuration files

	Configuration files should be in the form of
	---
	OpenRAVE:
	    colors: "./openrave_config/colors.yaml"
	    sizes: "./openrave_config/sizes.yaml"
	    positions: "./openrave_config/positions.yaml"
	    manipulation:
	        location: "./openrave/manipulation.py"
	        class: "manipulation.OpenRaveManipulationStrategy"
	    construction:
	        location: "./openrave/construction.py"
	        class: "construction.OpenRaveConstructionStrategy"
	...

	@note: Changes forward slashes to the seperator of the current platform
	"""

	COLOR_DESCRIPTOR = "colors"
	SIZE_DESCRIPTOR = "sizes"
	POSITIONS_DESCRIPTOR = "positions"
	MANIPULATION_DESCRIPTOR = "manipulation"
	CONSTRUCTION_DESCRIPTOR = "construction"
	LOCATION_DESCRIPTOR = "location"
	CLASS_DESCRIPTOR = "class"

	def __init__(self, configuration_file=None, configuration=None):
		"""
		Constructor for a PackageManager

		@keyword configuration_file: The location of the configuration file to read inverse kinematic package data from
		@type configuration_file: String
		@keyword configuration: YAML encoded string containing configuration information
		@type configuration: String
		@note: Exactly one of the keywords must be specified
		"""

		# Check we are not over specified
		if configuration_file and configuration:
			raise ValueError("Only the configuration file or the configuration string should be specified")

		# Get a reader
		reader = loaders.YamlReaderFactory.get_instance().get_reader()

		# Get a path fixer
		fixer = PathFixer.get_instance()

		# Read data
		if configuration_file:
			self.__data = reader.load(fixer.fix(configuration_file))
		elif configuration:
			self.__data = reader.loads(configuration)
		else:
			raise ValueError("Must specify either a configuration file to load or provide a YAML encoded string")
	
	def get_colors_config_file(self, package_name):
		"""
		Determines the location of the YAML file for the colors attached to the given package

		@param package_name: The name of the package to look up the color configuration file for
		@type package_name: String
		@return: The location of the colors configuration file for the provided package name
		@rtype: String
		"""
		
		entry = self.__get_package_info(package_name)

		if not PackageManager.COLOR_DESCRIPTOR in entry:
			raise ValueError("This package does not provide color information")
		
		return entry[PackageManager.COLOR_DESCRIPTOR]

	def get_sizes_config_file(self, package_name):
		"""
		Determines the location of the YAML file for the named sizes attached to the given package

		@param package_name: The name of the package to look up the sizes configuration file for
		@type package_name: String
		@return: The location of the sizes configuration file for the provided package name
		@rtype: String
		"""
		
		entry = self.__get_package_info(package_name)

		if not PackageManager.SIZE_DESCRIPTOR in entry:
			raise ValueError("This package does not provide color information")
		
		return entry[PackageManager.SIZE_DESCRIPTOR]

	def get_positions_config_file(self, package_name):
		"""
		Determines the location of the YAML file for the named positions attached to the given package

		@param package_name: The name of the package to look up the named positions configuration file for
		@type package_name: String
		@return: The location of the sizes configuration file for the provided package name
		@rtype: String
		"""
		
		entry = self.__get_package_info(package_name)

		if not PackageManager.POSITIONS_DESCRIPTOR in entry:
			raise ValueError("This package does not provide position information")
		
		return entry[PackageManager.POSITIONS_DESCRIPTOR]

	def get_manipulation_source_file(self, package_name):
		"""
		Determines the location of the source file for the manipulation strategy attached to the given package

		@param package_name: The name of the package to look up this source file for
		@type package_name: String
		@return: The location of the the manipulation strategy source
		@rtype: String
		"""
		
		entry = self.__get_package_info(package_name)

		if not PackageManager.MANIPULATION_DESCRIPTOR in entry:
			raise ValueError("This package does not provide manipulation information")
		
		return entry[PackageManager.MANIPULATION_DESCRIPTOR][PackageManager.LOCATION_DESCRIPTOR]
	
	def get_manipulation_class_name(self, package_name):
		"""
		Determines the name of the class to load as a manipulation strategy for this package

		@param package_name: The name of the package to look for a manipulation strategy class name to go with
		@type package_name: String
		@return: The module and class name for this manipulation strategy
		@rtype: String
		"""

		entry = self.__get_package_info(package_name)

		if not PackageManager.MANIPULATION_DESCRIPTOR in entry:
			raise ValueError("This package does not provide construction information")
		
		if not PackageManager.CLASS_DESCRIPTOR in entry[PackageManager.MANIPULATION_DESCRIPTOR]:
			raise ValueError("This package does not provide a class name to load")

		return entry[PackageManager.MANIPULATION_DESCRIPTOR][PackageManager.CLASS_DESCRIPTOR]
	
	def get_construction_source_file(self, package_name):
		"""
		Determines the location of the source file for the object construction strategy attached to the given package

		@param package_name: The name of the package to look up this source file for
		@type package_name: String
		@return: The location of the the construction strategy source
		@rtype: String
		"""
		
		entry = self.__get_package_info(package_name)

		if not PackageManager.CONSTRUCTION_DESCRIPTOR in entry:
			raise ValueError("This package does not provide construction information")

		return entry[PackageManager.CONSTRUCTION_DESCRIPTOR][PackageManager.LOCATION_DESCRIPTOR]
	
	def get_construction_class_name(self, package_name):
		"""
		Determines the name of the class to load as a manipulation strategy for this package

		@param package_name: The name of the package to look for a manipulation strategy class name to go with
		@type package_name: String
		@return: The module and class name for this construction strategy
		@rtype: String
		"""

		entry = self.__get_package_info(package_name)

		if not PackageManager.CONSTRUCTION_DESCRIPTOR in entry:
			raise ValueError("This package does not provide construction information")
		
		if not PackageManager.CLASS_DESCRIPTOR in entry[PackageManager.CONSTRUCTION_DESCRIPTOR]:
			raise ValueError("This package does not provide a class name to load")
		
		return entry[PackageManager.CONSTRUCTION_DESCRIPTOR][PackageManager.CLASS_DESCRIPTOR]
	
	def __get_package_info(self, package_name):

		if not package_name in self.__data:
			raise ValueError("The package name provided has not been given a specification")

		return self.__data[package_name]

class ObjectManipulationFactory:
	"""
	Factory singleton to configure and create an ObjectManipuationFacade along with its supporting parts
	"""

	__instance = None

	def __init__(self, configuration_file):
		"""
		Constructor for an ObjectManipulationFactory

		@param configuration_file: File describing the available inverse kinematics packages
		@type configuration_file: String file location
		"""
		self.__package_manager = PackageManager(configuration_file)
	
	def get_available_manipulation_facade_types(self):
		"""
		Provies a list of packages currently supported by this manipulation factory

		@return: List of inverse kinematics packages currently supported
		@rtype: List of Strings
		"""
		return self.__object_construction_strategies.keys()
	
	def create_facade(self, package, color_yaml_location=None, sizes_yaml_location=None, default_positions_yaml_file=None):
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

		# Load locations as needed
		if color_yaml_location == None:
			color_yaml_location = self.__package_manager.get_colors_config_file(package)
		if sizes_yaml_location == None:
			sizes_yaml_location = self.__package_manager.get_sizes_config_file(package)
		if default_positions_yaml_file == None:
			default_positions_yaml_file = self.__package_manager.get_positions_config_file(package)

		# Load construction and manipulation objects
		construction_module =  self.__package_manager.get_construction_class_name(package)
		construction_path =  self.__package_manager.get_construction_source_file(package)
		construction_strategy = imp.load_source(construction_module, construction_path)

		manipulation_module =  self.__package_manager.get_manipulation_class_name(package)
		manipulation_path =  self.__package_manager.get_manipulation_source_file(package)
		manipulation_strategy = imp.load_source(manipulation_module, manipulation_path)

		# Read from configuration files
		colors = self.__read_from_yaml_file(color_yaml_location)
		sizes = self.__read_from_yaml_file(sizes_yaml_location)
		positions = self.__read_from_yaml_file(default_positions_yaml_file)

		# Create strategies
		color_strategy = configurable.MappedColorResolutionFactory.get_instance().create_strategy(colors)
		size_strategy = configurable.MappedNamedSizeResolverFactory.get_instance().create_resolver(sizes)
		position_strategy = configurable.ObjectPositionFactoryConstructor.get_instance().create_factory(positions)
		
		# Create builder
		builder = virtualobject.VirtualObjectBuilder(construction_strategy, size_strategy_color_strategy)

		return ObjectManipulationFacade(builder, manipulation_strategy, color_strategy, size_strategy, position_strategy)

	def __read_from_yaml_file(self, target):
		"""
		Helper function to read and convert the contents of a YAML file

		@param target: Path to the file to read
		@type target: String
		"""
		reader = loaders.YamlReaderFactory.get_instance().get_reader()
		fixer = loaders.PathFixer.get_instance()
		return reader.load(fixer.fix(target))

class VirtualObjectManipulationStrategy:
	pass

	def update(self, target):
		pass
	
	def grab(self, target):
		pass
	
	def face(self, target):
		pass
	
	def  

class ObjectManipulationFacade:
	"""
	Driver for management and manipulation of virutal objects

	Facade that drives the creation of new and manipulation of existing objects in an inverse kinematics package
	
	@note: Should not be created directly. Use an ObjectManipulationFactory to construct.
	"""

	def __init__(self, object_builder, manipulation_strategy, color_resolution_strategy, named_size_resolver, object_position_factory):
		"""
		Constructor for ObjectManipulationFacade

		@param object_builder: The strategy to use to create new package-specific objects
		@type object_builder: VirtualObjectBuilder
		@param manipulation_strategy: The strategy to use to actually move objects within the package
		@type manipulation_strategy: VirtualObjectManipulationStrategy
		@param color_resolution_strategy: The strategy to resolve colors for names
		@type color_resolution_strategy: ColorResolutionStrategy
		@param named_size_resolver: The strategy to use to resolve names of sizes to actual sizes
		@type named_size_resolver: NamedSizeResolver
		@param object_position_factory: Factory to create positions
		@type object_position_factory: ObjectPositionFactory
		"""

		self.__object_builder = object_builder
		self.__manipulation_strategy = manipulation_strategy
		self.__color_resolution_strategy = color_resolution_strategy
		self.__named_size_resolver = named_size_resolver
		self.__object_position_factory = object_position_factory
		self.__descriptor_set = False
		self.__virtual_objects = structures.DictionarySet()
	
	def set_new_descriptor(self, descriptor):
		"""
		Sets the descriptor of the next object and following objects to be created

		@param new_descriptor: The descriptor to give to the next object and following objects to be created
		@type new_descriptor: String
		"""

		self.__object_builder.set_descriptor(descriptor)
		self.__descriptor_set = True
	
	def set_new_color(self, color):
		"""
		Sets the color of the next object and following objects to be created

		@param new_color: The color to give to the next object and following objects to be created
		@type new_color: String
		"""

		self.__object_builder.set_color(color)
	
	def set_new_size(self, size):
		"""
		Sets the size of the next object and following objects to be created

		@param new_size: The size to give to the next object and following objects to be created
		@type new_size: VirtualObjectSize
		"""

		self.__object_builder.set_size(size)
	
	def set_new_size_by_name(self, name):
		"""
		Sets the size of the next object and following objects to be created

		Sets the size of the next object and following objects to be created based off of the name of the object to be created and its descriptor

		@param name: The name of the size to resolve
		@type name: String
		@raise ValueError: If descriptor has not been set, will raise exception
		"""
		if not self.__descriptor_set:
			raise ValueError("Please set a descriptor before providing a named size")
		
		size = self.__named_size_resolver.get_size(name)

		self.set_new_size(size)
	
	def create(self, name, position):
		"""
		Creates a new VirtualObject from the parameters previously specified in this builder

		@param name: The name to give to this new object
		@type name: String
		@param position: The place to put this new object and its orientaiton
		@type position: String (named prefabricated position) or ObjectPosition
		"""
		
		new_object = self.__object_builder.create(name, position)
		self.__virtual_objects[name] = new_object
	
	def get_objects(self, update=False):
		"""
		Returns a list of all of the object Haikw is aware of in the target simulation 

		@keyword update: If True, all the object's positions will be updated before returned. Otherwise will return position from last check. Defaults to False.
		@type update: bool
		"""
		if update:
			ret_val = []
			for name in self.__virtual_objects.keys():
				orig = self.__virtual_objects[name]
				updated = self.update(orig)
				self.__virtual_objects[name] = updated
				ret_val.append(updated)
		else:
			ret_val = self.__virtual_objects.vals()
		
		return ret_val
	
	def update(self, target):
		"""
		Finds the updated state of a given VirtualObject

		@param target: The object to find the updated state for
		@target target: VirtualObject
		"""
		name = target.get_name()
		new = self.__manipulation_strategy.update(target)
		del self.__virtual_objects[name]
		self.__virtual_objects[name] = new
		return new
	
	def grab(self, target, affector = None):
		"""
		Grabs the given object from within the inverse kinematics simulation

		@param target: The object to grasp
		@type target: VirtualObject
		@keyword affector: Affector to use to carry out the given action. If not specified, the underlying library will decide.
		@type affector: RobotPart
		"""
		self.__manipulation_strategy.grab(target, affector)
	
	def grab_by_name(self, name, affector = None):
		"""
		Grab an object by name from within the inverse kinematics simulation

		@param name: The name of the object to grasp
		@type name: String
		@keyword affector: Affector to use to carry out the given action. If not specified, the underlying library will decide.
		@type affector: RobotPart
		"""
		self.grab(self.__virtual_objects[name], affector)
	
	def face(self, target, part = None):
		"""
		Have the robot in the simulation "face" the target virtual object

		@param target: The object to face
		@type target: VirtualObject
		@keyword part: The part of the robot that will face the target object. If not specified, the underlying library will decide.
		@type part: RobotPart
		"""
		self.__manipulation_strategy.face(target, part)
	
	def face_by_name(self, name, part = None):
		"""
		Have the robot in the simulation "face" the virtual object with the given name

		@param name: The name of the object to face
		@type name: String
		@keyword part: The part of the robot that will face the target object. If not specified, the underlying library will decide.
		@type part: RobotPart 
		"""
		self.face(self.__virtual_objects[name])