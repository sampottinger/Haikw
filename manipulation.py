"""
Module containing classes related to the manipulation of objects in the target inverse kinematics package

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""
import imp
import configurable
import loaders
import serializers
import structures
import virtualobject
import state
import package

class ObjectManipulationFactory:
	"""
	Factory singleton to configure and create an ObjectManipuationFacade along with its supporting parts
	"""

	__instance = None

	def __init__(self, language, configuration_file):
		"""
		Constructor for an ObjectManipulationFactory

		@param language: The language configuration files are written in
		@type language: String
		@param configuration_file: File describing the available inverse kinematics packages
		@type configuration_file: String file location
		"""
		self.__package_manager = package.PackageManager(language, configuration_file)
	
	def get_available_manipulation_facade_types(self):
		"""
		Provies a list of packages currently supported by this manipulation factory

		@return: List of inverse kinematics packages currently supported
		@rtype: List of Strings
		"""
		return self.__package_manager.get_supported_packages()
	
	def create_facade(self, package, language, colors_source = None, colors_file_location=None, sizes_source = None, sizes_file_location=None, positions_source = None, positions_file_location=None, setup_source = None, setup_file_location=None, robot_source = None, robot_file_location=None, prototypes_file_location=None, prototypes_source=None):
		"""
		Creates a new ObjectManipulationFacade given the configuration files and packages

		@param package: The name of the software package to target
		@type package: String
		@param language: The language to use to load configuration
		@type language: String
		@keyword colors_source: The configuration settings for colors
		@type colors_sources: String
		@keyword colors_file_location: Path to the file containing information about the default named colors to use in building objects
		@type colors_file_location: String
		@keyword sizes_source: The configuration settings for sizes
		@type sizes_sources: String
		@keyword sizes_file_location: Path to the file containing information about about the default named sizes to use in building objects
		@type sizes_file_location: String
		@keyword positions_source: The configuration settings for positions
		@type positions_sources: String
		@keyword positions_file_location: Path to the file containing information about the default named positions to use in placing objects
		@type positions_file_location: String
		@keyword setup_source: The configuration settings for setup
		@type setup_sources: String
		@keyword setup_file_location: Path to file describing available setups
		@type setup_file_location: String
		@keyword robot_source: The configuration settings for robots
		@type robot_sources: String
		@keyword robot_file_location: Path to file describing available robots
		@type robot_file_location: String
		@keyword prototypes_file_location: Path to file describing available named virtual object prototypes
		@type prototypes_file_location: String
		@keyword prototypes_source: The configuration settings for the named virtual object prototypes to use for this facade
		@type prototypes_source: String
		@raise ValueError: Raised if a strategy is requested for a package that has not been adapted or if that adapter has not been registered (see add_object_construction_strategy)
		"""
		
		serializer_factory = loaders.ConfigReaderFactory.get_instance()
		serializer = serializer_factory.get_reader(language)

		# Load sources as needed
		if colors_source != None:
			colors = serializer.loads(colors_source)
		elif colors_file_location:
			colors = serializer.load(colors_file_location)
		else:
			colors = self.__package_manager.get_colors_config(package)

		if sizes_source != None:
			sizes = serializer.loads(sizes_source)
		elif sizes_file_location:
			sizes = serializer.load(sizes_file_location)
		else:
			sizes = self.__package_manager.get_sizes_config(package)

		if positions_source != None:
			positions = serializer.loads(positions_source)
		elif positions_file_location:
			positions = serializer.load(positions_file_location)
		else:
			positions = self.__package_manager.get_positions_config(package)

		if setup_source != None:
			setup_source = serializer.loads(setup_source)
		elif setup_file_location:
			setup_source = serializer.load(setup_file_location)
		else:
			setup_source = self.__package_manager.get_setup_config(package)

		if robot_source_source != None:
			robot_source = serializer.loads(robot_source)
		elif robot_file_location:
			robot_source = serializer.load(robot_file_location)
		else:
			robot_source = self.__package_manager.get_robot_config(package)
		
		if prototypes_source != None:
			prototypes_source = serializer.loads(prototypes_source)
		elif prototypes_file_location:
			prototypes_source = serializer.load(prototypes_file_location)
		else:
			prototypes_source = self.__package_manager.get_prototypes_config(package)

		# Load construction and manipulation objects
		construction_module =  self.__package_manager.get_construction_class_name(package)
		construction_path =  self.__package_manager.get_construction_source_file(package)
		construction_strategy = imp.load_source(construction_module, construction_path)

		manipulation_module =  self.__package_manager.get_manipulation_class_name(package)
		manipulation_path =  self.__package_manager.get_manipulation_source_file(package)
		manipulation_strategy = imp.load_source(manipulation_module, manipulation_path)

		# Create strategies
		color_strategy = configurable.ComplexColorResolutionFactory.get_instance().create_strategy(colors)
		size_strategy = configurable.ComplexNamedSizeResolverFactory.get_instance().create_resolver(sizes)
		position_strategy = configurable.VirtualObjectPositionFactoryConstructor.get_instance().create_factory(positions)
		object_strategy = configurable.MappedObjectResolverFactory.get_instance().create_resolver(prototypes_source, size_strategy, color_strategy)

		# Create builder
		builder = virtualobject.VirtualObjectBuilder(construction_strategy)
		
		# Create setups and robots
		setups = serializers.SetupSerializer.get_instance().list_from_dict(setup_source)
		robots = serializers.RobotSerializer.get_instance().list_from_dict(robot_source)

		# Make managers of setups and robots
		setup_manager = experiment.SetupManager(setups)
		robot_manager = experiment.RobotManager(robots)

		return ObjectManipulationFacade(language, builder, manipulation_strategy, color_strategy, size_strategy, position_strategy, setup_manager, robot_manager, object_strategy)

# TODO: Docs and exceptions
class VirtualObjectManipulationStrategy:
	"""
	Fully abstract class / interface for stratgies for package specific manipulation and management tasks
	"""

	def __init__(self):
		pass

	def get_default_affector(self):
		raise NotImplementedError("Must use implementor of this interface / fully abstract class")

	def refresh(self, target):
		raise NotImplementedError("Must use implementor of this interface / fully abstract class")
	
	def grab(self, target, affector):
		raise NotImplementedError("Must use implementor of this interface / fully abstract class")
	
	def face(self, position, affector):
		raise NotImplementedError("Must use implementor of this interface / fully abstract class")
	
	def update(self, target, position):
		raise NotImplementedError("Must use implementor of this interface / fully abstract class")
	
	def release(self, affector):
		raise NotImplementedError("Must use implementor of this interface / fully abstract class")
	
	def delete(self, target):
		raise NotImplementedError("Must use implementor of this interface / fully abstract class")

class ComplexObjectBuilder:
	"""
	User facing bridge component for the creation of virtual objects that can resolve components by config files
	"""

	def __init__(self, inner_builder, object_strategy, position_strategy, named_size_resolver, color_resolution_strategy):
		"""
		Creates a new builder to wrap the internal builder

		@param inner_builder: The builder to wrap with this ObjectBuilder
		@type inner_builder: VirtualObjectBuilder
		@param object_strategy: Strategy to resolve named object prototypes
		@type object_strategy: NamedObjectResolver implementor
		@param position_strategy: The strategy used to change names of positions to actual positions
		@type position_strategy: VirtualObjectPositionFactory
		@param named_size_resolver: Strategy for turning names into sizes for name - descriptor pairs
		@type named_size_resolver: Subclass of NamedSizeResolver
		@param color_resolution_strategy: A strategy for turning strings passed in for colors to VirtualObjectColor objects
		@type color_resolution_strategy: Subclass of ColorResolutionStrategy
		"""
		self.__descriptor_set = False
		self.__object_builder = inner_builder
		self.__object_strategy = object_strategy
		self.__position_strategy = position_strategy

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
		# resolve color
		if not isinstance(color, virtualobject.VirtualObjectColor):
			color = self.__color_resolution_strategy.get_color(self.__color)

		self.__object_builder.set_color(color)
	
	def set_new_size(self, size):
		"""
		Sets the size of the next object and following objects to be created

		@param new_size: The size to give to the next object and following objects to be created
		@type new_size: VirtualObjectSize
		"""
		# resolve size
		if not isinstance(size, virtualobject.VirtualObjectSize):
			size = self.__named_size_resolver.get_size(self.__size)

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
		@type position: String (named prefabricated position) or VirtualObjectPosition
		@return: The new object for simulation
		@rtype: VirtualObject
		"""

		# Resolve position
		if isinstance(position, str):
			position = self.__position_strategy.create_prefabricated(position)
		elif not isinstance(position, VirtualObjectPosition):
			raise ValueError("Expected position to be a name of a prefabricated position or an instance of VirtualObjectPosition")
		
		# TODO: This makes me a bit uneasy
		new_object = self.__object_builder.create(name, position)
		return new_object
	
	def load_from_config(self, name):
		"""
		Loads an object prototype from configuration files

		@param name: The name of the prototype to load
		@type name: String
		"""
		descriptor = self.__object_strategy.get_descriptor(name)
		size = self.__object_strategy.get_size(name)
		color = self.__object_strategy.get_color(name)
		
		self.set_new_descriptor(descriptor)
		self.set_new_size(size)
		self.set_new_color(color)

class ObjectManipulationFacade:
	"""
	Driver for management and manipulation of virutal objects

	Facade that drives the creation of new and manipulation of existing objects in an inverse kinematics package
	
	@note: Should not be created directly. Use an ObjectManipulationFactory to construct.
	"""

	def __init__(self, object_builder, manipulation_strategy, color_resolution_strategy, named_size_resolver, object_position_factory, setup_manager, robot_manager, object_strategy):
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
		@type object_position_factory: VirtualObjectPositionFactory
		@param setup_manager: Manager of setups
		@type setup_manager: SetupManager
		@param robot_manager: Manager of potential robots for this facade
		@type robot_manager: RobotManager
		@param object_strategy: Strategy for the resolution of names to virtual object prototypes
		@type object_strategy: NamedObjectResolver implementor
		"""

		self.__manipulation_strategy = manipulation_strategy
		self.__internal_object_builder = object_builder
		self.__external_facing_object_builder = None
		self.__color_resolution_strategy = color_resolution_strategy
		self.__named_size_resolver = named_size_resolver
		self.__object_position_factory = object_position_factory
		self.__virtual_objects = structures.DictionarySet()
		self.__setup_manager = setup_manager
		self.__robot_manager = robot_manager
		self.__object_strategy = object_strategy
	
	def delete(self, target):
		"""
		Deletes the given target object

		@param target: Object to remove from the simulation
		@type target: VirtualObject or String name to resolve
		"""
		if isinstance(target, str):
			target_name = target
			target = self.get_object(target_name)
		elif isinstance(target, virtualobject.VirtualObject):
			target_name = target.get_name()
		else:
			raise ValueError("Expected String name for target or VirtualObject")
		
		self.__manipulation_strategy.delete(target)
		del self.__virtual_objects[target_name]

	def get_object_builder(self):
		""" Return a common builder for this factory """
		if not self.__external_facing_object_builder:
			self.__external_facing_object_builder = ComplexObjectBuilder(self.__internal_object_builder, self.__object_strategy, self.__object_position_factory, self.__named_size_resolver, self.__color_resolution_strategy)
		
		return self.__external_facing_object_builder
	
	def add_object(self, new_object):
		"""
		Has this facade track the given VirtualObject

		@param new_object: The new object to have this facade track
		@type new_object: VirtualObject
		"""
		self.__virtual_objects[new_object.get_name()] = new_object
	
	def get_objects(self, update=True):
		"""
		Returns a list of all of the object Haikw is aware of in the target simulation 

		@keyword update: If True, all the object's positions will be updated before returned. Otherwise will return position from last check. Defaults to True.
		@type update: bool
		"""
		if update:
			ret_val = []
			for name in self.__virtual_objects.keys():
				orig = self.__virtual_objects[name]
				updated = self.refresh(orig)
				ret_val.append(updated)
		else:
			ret_val = self.__virtual_objects.vals()
		
		return ret_val
	
	def get_object(self, name, update=True):
		"""
		Returns the object with the given name

		@param name: The name of the object to read from the simulation
		@type name: String
		@return: The current state of the requested object
		@rtype: VirtualObject
		"""
		if not name in self.__virtual_objects:
			raise KeyError("No objects by that name have been registered in this simulation")
		
		ret_val = self.__virtual_objects[name]

		if update:
			ret_val = self.refresh(ret_val)
		
		return ret_val
	
	def update(self, target, position):
		"""
		Updates this object in the simulation, giving it the provided position

		@param target: The object to update in the simulation
		@type target: String (name) or VirtualObject
		@param position: The position to put this object at
		@type position: VirtualObjectPosition or String (name)
		"""
		# Resolve target
		if isinstance(target, str):
			target = self.get_object(target, False)
		elif not isinstance(target, virtualobject.VirtualObject):
			raise ValueError("Target must be the string name of a simulated object or a VirtualObject instance")
		
		# Resolve position
		if isinstance(position, str):
			position = self.__object_position_factory.create_prefabricated(position)
		elif not isinstance(position, state.VirtualObjectPosition):
			raise ValueError("Expected position to be a VirtualObjectPosition instance or String name corresponding to position from a config file")
		
		target = self.__manipulation_strategy.update(target, position)
		del self.__virtual_objects[target.get_name()]
		self.__virtual_objects[target.get_name()] = target
	
	def refresh(self, target):
		"""
		Gets the updated state of a given VirtualObject

		@param target: The object to find the updated state for
		@target target: VirtualObject
		"""
		name = target.get_name()
		new = self.__manipulation_strategy.refresh(target)
		del self.__virtual_objects[name]
		self.__virtual_objects[name] = new
		return new
	
	def put(self, target, position, affector = None):
		"""
		Moves target to position using robotic affectors

		@param target: The object to move
		@type target: VirtualObject or String name of a simulated VirtualObject
		@param position: The position to move this object to
		@type position: String name of a prefacbricated position or VirtualObjectPosition
		@keyword affector: Specify which affector to use to do the manipulation
		@type affector: RobotPart
		@return: Updated version of the object just moved
		@rtype: VirtualObject
		"""
		if affector == None:
			affector = self.__manipulation_strategy.get_default_affector()

		if isinstance(target, str):

			if not target in self.__virtual_objects:
				raise KeyError("That object has not been registered in this simulation yet")
			
			target = self.__virtual_objects[target]
		
		elif not isinstance(target, virtualobject.VirtualObject):
			raise ValueError("Expected target to be a VirtualObject or string name of a registered VirtualObject")
		
		self.grab(target, affector=affector)
		self.face(position, affector=affector)
		self.release(affector=affector)
		return self.refresh(target)
	
	def release(self, affector=None):
		"""
		Has the given end affector "release" 

		@param affector: The affector to put into a "release" state
		@type affector: RobotPart
		"""
		if affector == None:
			affector = self.__manipulation_strategy.get_default_affector()
		
		self.__manipulation_strategy.release(affector)
	
	def grab(self, target, affector = None):
		"""
		Grabs the given object from within the inverse kinematics simulation

		@param target: The object to grasp
		@type target: VirtualObject or String name
		@keyword affector: Affector to use to carry out the given action. If not specified, the underlying library will decide.
		@type affector: RobotPart
		"""
		if affector == None:
			affector = self.__manipulation_strategy.get_default_affector()
		
		if isinstance(target, str):
			target = self.get_object(target)
		elif not isinstance(target, virtualobject.VirtualObject):
			raise ValueError("Position must be the name (string) of a simulated object or a VirtualObject")

		self.__manipulation_strategy.grab(target, affector)
	
	def face(self, target, affector = None):
		"""
		Have the robot in the simulation "face" the target virtual object

		@param target: The object to face
		@type target: VirtualObject, String, or VirtualObjectPosition
		@keyword affector: The part of the robot that will face the target object. If not specified, the underlying library will decide.
		@type affector: RobotPart
		"""
		if affector == None:
			affector = self.__manipulation_strategy.get_default_affector()
		
		# Try to resolve targets to face
		if isinstance(target, state.VirtualObjectPosition):
			position = target
		elif isinstance(target, virtualobject.VirtualObject):
			position = target.get_position()
		elif isinstance(target, str):

			if target in self.__object_position_factory.get_prefabrications():
				position = self.__object_position_factory.create_prefabricated(target)
			elif target in self.__virtual_objects:
				position = self.__virtual_objects[target].get_position()
			else:
				raise ValueError("Unable to resolve string target to position")
		
		else:
			raise TypeError("Expected target to be a VirtualObject, VirtualObjectPosition, or String name of a position or object")

		self.__manipulation_strategy.face(position, affector)
	
	def get_manipulation_strategy(self):
		""" Allow direct access to the underlying manipulation strategy for the Will Robinsons of the world """
		return self.__manipulation_strategy

	# TODO: Place relative, set_new_prototype, 