"""
Module containing objects managing simulated objects

This module provides management for objects simulated in the target inverse kinematics package

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

import re
import state

class VirtualObject:
	"""
	Simple temporary immutable state of a simulated object
	"""

	def __init__(self, name, position, descriptor, color, size):
		"""
		Constructor for a VirtualObject

		@param name: Unique name for this virtual object
		@type name: String
		@param position: The current position for this VirtualObject
		@type position: VirtualObjectPosition
		@param descriptor: The descriptor used to create this VirtualObject
		@type descriptor: String
		@param color: The color of this VirtualObject as it was created
		@type color: VirtualObjectColor
		@param size: The size of this VirtualObject as it was created
		@type size: VirtualObjectSize
		"""
		# Enforce types . . . it's kinda important here
		if not isinstance(name, str):
			raise TypeError("Expected string for VirtualObject name")
		if not isinstance(position, state.VirtualObjectPosition):
			raise TypeError("Expected VirtualObjectPosition for VirtualObject position")
		if not isinstance(descriptor, str):
			raise TypeError("Expected string for VirtualObject descriptor")
		if not isinstance(color, VirtualObjectColor):
			raise TypeError("Expected VirtualObjectColor for VirtualObject color")
		if not isinstance(size, VirtualObjectSize):
			raise TypeError("Expected VirtualObjectSize for VirtualObject size")

		# Save instance vars
		self.__name = name
		self.__position = position
		self.__descriptor = descriptor
		self.__color = color
		self.__size = size
	
	def get_name(self):
		"""
		Determine the unqiue name for this object

		@return: The name of this object
		@rtype: String
		"""
		return self.__name
	
	def get_position(self):
		"""
		Determine the position of this object at checking with the simulation when creating this state

		@return: Position as of this state's creation
		@rtype: VirtualObjectPosition
		@note: This is not kept up to date. To find the latest position, use an ObjectManipulationFacade
		"""
		return self.__position
	
	def get_descriptor(self):
		"""
		Determine the descriptor used to create this virtual object

		@return: Original descriptor used to create this object
		@rtype: String
		"""
		return self.__descriptor
	
	def get_color(self):
		"""
		Determine the color used to create this virtual object

		@return: Original color used to create this object
		@rtype: VirtualObjectColor
		"""
		return self.__color
	
	def get_size(self):
		"""
		Determine the size used to create this virtual object

		@return: Original size used to create this object
		@rtype: VirtualObjectSize
		"""
		return self.__size

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
		if r >= 0 and r <= 255:
			self.__r = r
		else:
			raise ValueError("Invalid value for the provided red value (must be between 0 and 255)")

		if g >= 0 and g <= 255:
			self.__g = g
		else:
			raise ValueError("Invalid value for the provided green value (must be between 0 and 255)")

		if b >= 0 and b <= 255:
			self.__b = b
		else:
			raise ValueError("Invalid value for the provided blue value (must be between 0 and 255)")
	
	def get_red(self):
		""" Get the red coponent of this color

		@return: The red component of this color
		@rtype: Byte / integer (range from 0 to 255)
		"""

		return self.__r

	def get_green(self):
		""" Get the green coponent of this color

		@return: The green component of this color
		@rtype: Byte / integer (range from 0 to 255)
		"""

		return self.__g
		
	def get_blue(self):
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

	def __init__(self):
		pass

	def create_object(self, virtual_object):
		"""
		Creates a new object with the given properties

		@param virtual_object: The new virtual_object to add to the inverse kinematics sim
		@type virtual_object: VirtualObject
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

class ComplexColorResolutionStrategy(ColorResolutionStrategy):
	"""
	Mapping object for simple string names, hex encoded strings (#rrggbb), and dicts to colors
	"""

	RED = "red"
	BLUE = "blue"
	GREEN = "green"

	def __init__(self):
		"""
		Constructor for MappedColorResolutionStrategy
		"""
		self.__colors = {}
		self.__hex_regex = None
	
	def get_color(self, description):
		"""
		Resolves this name of a color to an actual color

		@param decription: A description of the color desired
		@type description: String or dict
		@return: Color corresponding to the given name
		@rtype: VirtualObjectColor
		@raise ValueError: Raised if there is no mapping for the provided name
		"""
		if isinstance(description, str):

			# Hex description resolver
			if description[0] == "#":
				if self.__hex_regex == None:
					self.__hex_regex = re.compile("\#(?P<red>[\dA-F]{2})(?P<green>[\dA-F]{2})(?P<blue>[\dA-F]{2})")

				match = self.__hex_regex.match(description)

				if match == None:
					raise ValueError("Invalid color value, need #rrggbb, name, or individual components")
				
				red = int(match.group("red"), 16)
				blue = int(match.group("blue"), 16)
				green = int(match.group("green"), 16)
			
			# Registered name
			elif description in self.__colors:
				return self.__colors[description]
			
			# Bad string
			else:
				raise ValueError("Must be a hex description #rrggbb or name corresponding to a registered color. This string resolved to neither")
		
		# Components
		elif isinstance(description, dict):

			# Extract red
			if not ComplexColorResolutionStrategy.RED in description:
				raise ValueError("Red not specified for this color")
			red = description[ComplexColorResolutionStrategy.RED]

			if not isinstance(red, int):
				raise ValueError("The value for red was not given as a base 10 integer")

			if red > 255 or red < 0:
				raise ValueError("The value for red was between 0 and 255")

			
			# Extract blue
			if not ComplexColorResolutionStrategy.BLUE in description:
				raise ValueError("Blue not specified for this color")
			blue = description[ComplexColorResolutionStrategy.BLUE]

			if not isinstance(blue, int):
				raise ValueError("The value for blue was not given as a base 10 integer")

			if blue > 255 or blue < 0:
				raise ValueError("The value for blue was between 0 and 255")

			
			# Extract green
			if not ComplexColorResolutionStrategy.GREEN in description:
				raise ValueError("Green not specified for this color")
			green = description[ComplexColorResolutionStrategy.GREEN]

			if not isinstance(green, int):
				raise ValueError("The value for green was not given as a base 10 integer")

			if green > 255 or green < 0:
				raise ValueError("The value for green was between 0 and 255")
		
		else: # Unknown type
			raise ValueError("Description needs to be a string or dictionary")
		
		return VirtualObjectColor(red, green, blue)
	
	def add_color(self, name, color):
		"""
		Adds a new color to this mapping

		@param name: The name of the new color to add to the mapping
		@type name: String
		@param color: The new color to add to the mapping
		@type color: VirtualObjectColor, String (description or hex), or dict
		"""
		if not isinstance(color, VirtualObjectColor):
			color = self.get_color(color)
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
	Interface / fully abstract parent class for strategies for turning names or list of floats into sizes
	"""

	def __init__(self):
		pass

	def get_size(self, name):
		"""
		Resolves this name of a size to an actual size

		@param name: The name of the size desired
		@type name: String
		@return: Size corresponding to the given name
		@rtype: VirtualObjectSize
		"""

		raise NotImplementedError("Must use a subclass / implementor of this interface")

class ComplexNamedSizeResolver(NamedSizeResolver):
	"""
	Name resolver capable of resolving lists of floats and named sizes to VirtualObjectSize instances
	"""

	def __init__(self):
		NamedSizeResolver.__init__(self)
		self.__mapping = {}
	
	def get_size(self, description):
		"""
		Resolves this description of a size to an actual size

		@param description: The name of the size desired
		@type description: String or list of floats
		@return: Size corresponding to the given name or floats
		@rtype: VirtualObjectSize
		"""
		if isinstance(description, str):
			if description in self.__mapping:
				return self.__mapping[description]
			else:
				raise KeyError("No color mapping for that name has been registered")
		elif isinstance(description, list) or isinstance(description, tuple):
			return VirtualObjectSize(description)
		else:
			raise ValueError("Description must be a String name or list of floats")

	def add_size(self, name, size):
		"""
		Adds a new size to this mapping

		@param name: The name of the size to add
		@type name: String
		@param size: The new size to add to the mapping
		@type size: VirtualObjectSize
		"""

		self.__mapping[name] = size

class NamedObjectResolver:
	"""
	Interface / fully abstract class for strategies turning names into VirtualObjects
	"""

	def __init__(self):
		pass

	def get_size(self, name):
		"""
		Resolves this name of the desired object to its prototype size

		@param name: The name of the desired object
		@type name: String
		@return: Size corresponding to the given name
		@rtype: String (description) or VirtualObjectSize
		"""

		raise NotImplementedError("Must use a subclass / implementor of this interface")
	
	def get_descriptor(self, name):
		"""
		Resolves this name of the desired object to its prototype descriptor

		@param name: The name of the desired object
		@type name: String
		@return: Descriptor corresponding to the given name
		@rtype: String (description)
		"""

		raise NotImplementedError("Must use a subclass / implementor of this interface")
	
	def get_color(self, name):
		"""
		Resolves this name of the desired object to its prototype color

		@param name: The name of the desired object
		@type name: String
		@return: Color corresponding to the given name
		@rtype: String (description) or VirtualObjectColor
		"""

		raise NotImplementedError("Must use a subclass / implementor of this interface")

class ObjectResolverFlyweight:
	"""
	Simple structure containing properties for a virtual object prototype
	"""

	def __init__(self, color, size, descriptor):
		"""
		Constructor for ObjectResolverFlyweight

		@param color: The color this object takes on
		@type color: VirtualObjectColor
		@param size: The default size for this prototype
		@type size: VirtualObjectSize
		@param descriptor: Description of the shape of this object
		@type descriptor: String
		"""
		# Double check types
		if not isinstance(color, VirtualObjectColor):
			raise TypeError("Expecting VirtualObjectColor for color")
		if not isinstance(size, VirtualObjectSize):
			raise TypeError("Expecting VirtualObjectSize for size")
		if not isinstance(descriptor, str):
			raise TypeError("Expecting descriptor to be a string")

		self.color = color
		self.size = size
		self.descriptor = descriptor

class MappedObjectResolver(NamedObjectResolver):
	""" 
		Map based implementation of the NamedObjectResolver interface
	"""

	def __init__(self):
		NamedObjectResolver.__init__(self)
		self.__mapping = {}
	
	def get_registered_objects(self):
		""" 
		Get a listing of all of the objects this resolver can resolve to

		@return: The mapping in use by this resolver
		@rtype: Dict
		"""
		return self.__mapping

	def get_size(self, name):
		"""
		Resolves this name of the desired object to its prototype size

		@param name: The name of the desired object
		@type name: String
		@return: Size corresponding to the given name
		@rtype: VirtualObjectSize
		"""
		if not name in self.__mapping:
			raise KeyError("This named object has not been registered in this resolver.")

		return self.__mapping[name].size
	
	def get_descriptor(self, name):
		"""
		Resolves this name of the desired object to its prototype descriptor

		@param name: The name of the desired object
		@type name: String
		@return: Descriptor corresponding to the given name
		@rtype: String (description)
		"""
		if not name in self.__mapping:
			raise KeyError("This named object has not been registered in this resolver.")

		return self.__mapping[name].descriptor
	
	def get_color(self, name):
		"""
		Resolves this name of the desired object to its prototype color

		@param name: The name of the desired object
		@type name: String
		@return: Color corresponding to the given name
		@rtype: VirtualObjectColor
		"""
		if not name in self.__mapping:
			raise KeyError("This named object has not been registered in this resolver.")

		return self.__mapping[name].color
	
	def add_object(self, name, flyweight):
		"""
		Adds a new object to this mapping

		@param name: The name of the object to add
		@type name: String
		@param flyweight: ObjectPropertiesFlyweight with information regarding this new mapping
		@type ObjectResolverFlyweight
		"""
		self.__mapping[name] = flyweight

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
		new_obj = VirtualObject(name, position, self.__descriptor, self.__color, self.__size)

		# Add to sim
		self.__construction_strategy.create_object(new_obj)

		return new_obj
		