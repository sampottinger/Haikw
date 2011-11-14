"""
Module containing objects managing simulated objects

This module provides management for objects simulated in the target inverse kinematics package

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

class VirtualObjectColor:
	"""
	Simple structure for RBG colors
	"""

	def __init__(self, r, g, b):
		""" Construtor for VirtualObjectColor

		@param r: The red component of this color
		@type r: Byte / integer (0-255)
		@param g: The green component of this color
		@type g: Byte / integer (0-255)
		@param b: The blue component of this color
		@type b: Byte / integer (0-255)
		"""

		# Verify ranges
		if r >= 0 && r <= 255:
			self.__r = r
		else:
			raise ValueError("Invalid value for the provided red value (must be between 0 and 255)")

		if g >= 0 && g <= 255:
			self.__g = g
		else:
			raise ValueError("Invalid value for the provided green value (must be between 0 and 255)")

		if b >= 0 && b <= 255:
			self.__b = b
		else:
			raise ValueError("Invalid value for the provided blue value (must be between 0 and 255)")
	
	def get_red():
		""" Get the red coponent of this color

		@return: The red component of this color
		@rtype: Byte / integer (range from 0 to 255)
		"""

		return self.__r

	def get_green():
		""" Get the green coponent of this color

		@return: The green component of this color
		@rtype: Byte / integer (range from 0 to 255)
		"""

		return self.__g
		
	def get_blue():
		""" Get the blue coponent of this color

		@return: The blue component of this color
		@rtype: Byte / integer (range from 0 to 255)
		"""

		return self.__b

class VirtualObjectConstructionStrategy:
	"""
	Interface / fully abstract parent class for strategies for creating VirtualObjects

	@note: It's a bit un-pythonic to do this but, given long term extendability concerns, this option was taken
	"""

	def create_object(self, name, descriptor, color, size):
		"""
		Creates a new object with the given properties

		@param name: Identifying name for this new object
		@type name: String
		@param descriptor: Simple description of the object to make
		@type descriptor: String
		@param color: Color to make the next objects with
		@type color: VirtualObjectColor
		@param size: The size to assign to the next objects to make
		@type size: VirtualObjectSize
		"""

		raise NotImplementedError("Must use subclass / implementor of this interface")

class ColorResolutionStrategy:
	"""
	Interface / fully abstract parent class for strategies for turning string names into colors

	@note: It's a bit un-pythonic to do this but, given long term extendability concerns, this option was taken
	"""

	def get_color(self, name):
		"""
		Resolves this name of a color to an actual color

		@param name: The name of the color desired
		@type name: String
		@return: Color corresponding to the given name
		@rtype: VirtualObjectColor
		"""

		raise NotImplementedError("Must use subclass / implementor of this interface")

class MappedColorResolutionStrategy(ColorResolutionStrategy):
	"""
	Mapping object for simple string to color conversions
	"""

	def __init__(self):
		"""
		Constructor for MappedColorResolutionStrategy
		"""
		self.__colors = {}
	
	def get_color(self, name):
		"""
		Resolves this name of a color to an actual color

		@param name: The name of the color desired
		@type name: String
		@return: Color corresponding to the given name
		@rtype: VirtualObjectColor
		@raise ValueError: Raised if there is no mapping for the provided name
		"""
		if not name in self.__colors:
			raise ValueError("No mapping available for this color name")
		
		return self.__colors[name]
	
	def add_color(self, name, color):
		"""
		Adds a new color to this mapping

		@param name: The name of the new color to add to the mapping
		@type name: String
		@param color: The new color to add to the mapping
		@type color: VirtualObjectColor
		"""
		self.__colors[name] = color

class VirtualObjectSize:
	"""
	Structure representing an object's size that implements both the list and iterator "interfaces"
	"""

	def __init__(self, dimensions):
		"""
		Constructor for VirtualObjectSize

		@param dimensions: Object specific dimensions
		@type dimensions: list of floats
		"""

		self.__dimensions = dimensions
	
	def iter(self):
		""" Returns iterator over the dimensions of this VirtualObjectSize

		@return: Dimensions of this size
		@rtype: iterator
		"""
		return self.__dimensions.iter()
	
	def __iter__(self):
		""" Returns iterator over the dimensions of this VirtualObjectSize

		@return: Dimensions of this size
		@rtype: iterator
		"""
		return self.__dimensions.iter
	
	def __setitem__(self, key, value):
		"""
		Sets the given dimension to the provided value 

		@param key: Index in this set of dimensions
		@type key: integer
		@param value: The new value of this dimension
		@type value: float
		"""
		self.__dimensions[key] = value
	
	def __getitem__(self, key):
		"""
		Gets the given dimension to the provided value 

		@param key: Index in this set of dimensions
		@type key: integer
		@return: Value
		@rtype: float
		"""
		return self.__dimensions[key]
	
	def __delitem__(self, key):
		"""
		Removes the given dimension from this size

		@param key: Index in this set of dimensions
		@type key: integer
		"""
		del self.__dimensions[key]

class NamedSizeResolver:
	"""
	Interface / fully abstract parent class for strategies for turning names into sizes
	"""

	def get_size(self, name):
		"""
		Resolves this name of a size to an actual size

		@param name: The name of the size desired
		@type name: String
		@return: Size corresponding to the given name
		@rtype: VirtualObjectSize
		"""

		raise NotImplementedError("Must use a subclass / implementor of this interface")

class MappedNamedSizeResolver(NamedSizeResolver):
	"""
	Dictionary-based name resolver 
	"""

	def __init__(self):
		NamedSizeResolver.__init__(self)
		self.__mapping = {}
	
	def get_size(self, name):
		"""
		Resolves this name of a size to an actual size

		@param name: The name of the size desired
		@type name: String
		@return: Size corresponding to the given name
		@rtype: VirtualObjectSize
		"""

		return self.__mapping[name]
	
	def add_size(self, name, size):
		"""
		Adds a new size to this mapping

		@param name: The name of the size to add
		@type name: String
		@param size: The new size to add to the mapping
		@type size: VirtualObjectSize
		"""

		self.__mapping[name] = size

class VirtualObjectBuilder:
	""" 
	Creates virtual objects for a given inverse kinematics package

	@note: This should be created and accessed through an ObjectManipulationFacade
	"""

	NOT_SPECIFIED = None

	def __init__(self, construction_strategy, named_size_resolver, color_resolution_strategy):
		"""
		Creates a new VirtualObjectBuilder that leverages the given construction strategy
		
		@param construction_strategy: Package specific strategy for building virtual objects specific to the inverse kinematics software in use
		@type: Subclass of VirtualObjectConstructionStrategy
		@param named_size_resolver: Strategy for turning names into sizes for name - descriptor pairs
		@type named_size_resolver: Subclass of NamedSizeResolver
		@param color_resolution_strategy: A strategy for turning strings passed in for colors to VirtualObjectColor objects
		@type color_resolution_strategy: Subclass of ColorResolutionStrategy
		"""

		self.__construction_strategy = construction_strategy
		self.__named_size_resolver = named_size_resolver
		self.__color_resolution_strategy = color_resolution_strategy
		self.__descriptor = VirtualObjectBuilder.NOT_SPECIFIED
		self.__color = VirtualObjectBuilder.NOT_SPECIFIED
		self.__size = VirtualObjectBuilder.NOT_SPECIFIED
		self.__name = VirtualObjectBuilder.NOT_SPECIFIED
	
	def set_name(self, new_name):
		"""
		Sets the name of the next object and following objects to be created

		@param new_name: The name to give to the next object and following objects to be created
		@type new_name: String
		"""

		self.__name = new_name
	
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
		@type new_color: String
		"""

		self.__color = new_color
	
	def set_size(self, new_size):
		"""
		Sets the size of the next object and following objects to be created

		@param new_size: The size to give to the next object and following objects to be created
		@type new_size: VirtualObjectSize
		"""

		self.__size = new_size
	
	def create(self, position):
		"""
		Creates a new object at the given position

		@param position: The position to give this new object
		@type position: ObjectPosition
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

		if self.__name == VirtualObjectBuilder.NOT_SPECIFIED:
			raise AttributeError("Name has not been set. Please call set_name and try again.")

		# resolve color
		color = self.__color_resolution_strategy.get_color(self.__color)

		# resolve size
		size = self.__named_size_resolver.get_size(self.__size)

		# Create and return new object
		return self.__construction_strategy.create_object(self.__name, self.__descriptor, color, size)
		