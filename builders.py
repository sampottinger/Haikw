"""
Module containing classes for building VirtualObjects

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""
import virtualobject

class VirtualObjectBuilder:
	""" 
	Creates virtual objects for a given inverse kinematics package

	@note: This should be created and accessed through an ObjectManipulationFacade
	""" 

	NOT_SPECIFIED = None

	def __init__(self, construction_strategy):
		"""
		Creates a new VirtualObjectBuilder that leverages the given construction strategy
		
		@param construction_strategy: Package specific strategy for building virtual objects specific to the inverse kinematics software in use
		@type: Subclass of VirtualObjectConstructionStrategy
		"""

		self.__construction_strategy = construction_strategy
		self.__descriptor = VirtualObjectBuilder.NOT_SPECIFIED
		self.__color = VirtualObjectBuilder.NOT_SPECIFIED
		self.__size = VirtualObjectBuilder.NOT_SPECIFIED
	
	def set_descriptor(self, new_descriptor):
		"""
		Sets the descriptor of the next object and following objects to be created

		@param new_descriptor: The descriptor to give to the next object and following objects to be created
		@type new_descriptor: String
		"""

		self.__descriptor = new_descriptor
	
	def set_color(self, new_color):
		"""
		Sets the color of the next object and following objects to be created

		@param new_color: The color to give to the next object and following objects to be created
		@type new_color: VirtualObjectColor
		"""

		self.__color = new_color
	
	def set_size(self, new_size):
		"""
		Sets the size of the next object and following objects to be created

		@param new_size: The size to give to the next object and following objects to be created
		@type new_size: VirtualObjectSize
		"""

		self.__size = new_size
	
	def create(self, name, position):
		"""
		Creates a new object at the given position

		@param name: The name to assign this object
		@type name: String
		@param position: The position to give this new object
		@type position: VirtualObjectPosition
		@return: A new virtual object
		@rtype: VirtualObject

		@note: This does not add this object to the simulation. Make sure not to call this directly. Use ObjectManipulationFacade instead
		"""

		if self.__descriptor == VirtualObjectBuilder.NOT_SPECIFIED:
			raise AttributeError("Descriptor has not been set. Please call set_descriptor and try again.")

		if self.__color == VirtualObjectBuilder.NOT_SPECIFIED:
			raise AttributeError("Color has not been set. Please call set_color and try again.")

		if self.__size == VirtualObjectBuilder.NOT_SPECIFIED:
			raise AttributeError("Size has not been set. Please call set_size and try again.")

		# Create virtual object
		new_obj = virtualobject.VirtualObject(name, position, self.__descriptor, self.__color, self.__size)

		# Add to sim
		self.__construction_strategy.create_object(new_obj)

		return new_obj

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