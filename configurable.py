"""
Module containing factories driven by user provided configuration

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

import re
import virtualobject

class MappedColorResolutionFactory:
	"""
	Factory singleton creating MappedColorResolutionStrategies from dicts
	"""

	RED = "red"
	BLUE = "blue"
	GREEN = "green"

	__instance = None
	__hex_regex = None

	def get_instance(self):
		"""
		Returns a shared instance of this MappedColorResolutionFactory, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: MappedColorResolutionFactory
		"""

		if not MappedColorResolutionFactory.__instance:
			MappedColorResolutionFactory.__instance = MappedColorResolutionFactory()
		
		return MappedColorResolutionFactory.__instance
	
	def __init__(self):
		"""
		Constructor for MappedColorResolutionFactory

		@note: This class is a singleton and this should only be called internally
		"""
		pass
	
	def create_strategy(self, data):
		"""
		Creates a new MappedColorResolutionStrategy from the given data

		@param data: dict 
		@type data: Dictionary of the form {"colorname":{"red":decimal, "green":decimal, "blue":decimal}} or {"colorname":"#rrggbb"}
		"""

		strategy = virtualobject.MappedColorResolutionStrategy()

		for name in data.keys():

			# Create color
			new_color = self.__create_color(data[name])

			# Add it to the new strategy
			strategy.add_color(name, new_color)
		
		return strategy
	
	def __create_color(self, color):
		"""
		Creates a new color from the given description of it

		@param color: Dictionary or string describing this color
		@type color: Dictionary or String
		@return: New color corresponding to the given description
		@rtype: VirtualObjectColor
		"""

		# Extract from form #rrggbb
		if isinstance(color, str): 
			
			if self.__hex_regex == None:
				self.__hex_regex = re.compile("\#(?P=<red>\d{2})(?P=<blue>\d{2})(?P=<green>\d{2})")

			match = self.__hex_regex.match(color)

			if match == None:
				raise ValueError("Invalid color value, need #rrggbb or individual components")

			red = int(match.group("red"), 16)
			blue = int(match.group("blue"), 16)
			green = int(match.group("green"), 16)

		# Extract from dictionary listing
		else:
			
			# Extract red
			if not MappedColorResolutionFactory.RED in color:
				raise ValueError("Red not specified for this color")
			red = color[MappedColorResolutionFactory.RED]

			if not isinstance(red, int):
				raise ValueError("The value for red was not given as a base 10 integer")

			if red > 255 or red < 0:
				raise ValueError("The value for red was between 0 and 255")

			
			# Extract blue
			if not MappedColorResolutionFactory.BLUE in color:
				raise ValueError("Blue not specified for this color")
			blue = color[MappedColorResolutionFactory.BLUE]

			if not isinstance(blue, int):
				raise ValueError("The value for blue was not given as a base 10 integer")

			if blue > 255 or blue < 0:
				raise ValueError("The value for blue was between 0 and 255")

			
			# Extract green
			if not MappedColorResolutionFactory.GREEN in color:
				raise ValueError("Green not specified for this color")
			green = color[MappedColorResolutionFactory.GREEN]

			if not isinstance(green, int):
				raise ValueError("The value for green was not given as a base 10 integer")

			if green > 255 or green < 0:
				raise ValueError("The value for green was between 0 and 255")
		
		return virtualobject.VirtualObjectColor(red, green, blue)

class MappedNamedSizeResolverFactory:
	""" Factory singleton to create MappedNamedSizeResolver from Python dictionaries """

	__instance = None

	def get_instance(self):
		"""
		Returns a shared instance of this MappedNamedSizeResolverFactory, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: MappedNamedSizeResolverFactory
		"""

		if not MappedNamedSizeResolverFactory.__instance:
			MappedNamedSizeResolverFactory.__instance = MappedNamedSizeResolverFactory()
		
		return MappedNamedSizeResolverFactory.__instance
	
	def __init__(self):
		"""
		Constructor for MappedNamedSizeResolverFactory

		@note: This class is a singleton and this should only be called internally
		"""
		pass
	
	def create_resolver(self, data):
		"""
		Creates a new MappedNamedSizeResolver

		@param data: Python attributes loaded from configuration files
		@type: Dictionary containing {"name" : [float1, float2]}
		@return: New MappedNamedSizeResolver instance
		@rtype: MappedNamedSizeResolver
		"""

		new_resolver = virtualobject.MappedNamedSizeResolver()

		if not isinstance(data, dict):
			raise ValueError("Expected dictionary for data")

		for name in data.keys():
			new_size = virtualobject.VirtualObjectSize(data[name])
			new_resolver.add(name, new_size)
		
		return new_resolver

class ObjectPositionFactoryConstructor:
	"""
	Factory singleton that creates ObjectPositionFactory
	"""

	DEFAULT_ROLL = 0
	DEFAULT_PITCH = 0
	DEFAULT_YAW = 0

	def get_instance(self):
		"""
		Returns a shared instance of this ObjectPositionFactoryConstructor, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: ObjectPositionFactoryConstructor
		"""

		if not ObjectPositionFactoryConstructor.__instance:
			ObjectPositionFactoryConstructor.__instance = ObjectPositionFactoryConstructor()
		
		return ObjectPositionFactoryConstructor.__instance
	
	def __init__(self):
		"""
		Constructor for ObjectPositionFactoryConstructor

		@note: This class is a singleton and this should only be called internally
		"""
		pass
	
	def create_factory(self, data):
		"""
		Creates a new ObjectPositionFactory from the given data

		@param data: Data loaded from configuration files
		@type data: Dictionary of form {"name" : {"x":float, "y":float, "z":float, "roll":float, "pitch":float, "yaw":float}}
		@return: New ObjectPositionFactory instance with the given data as prefabricated positions
		@rtype: ObjectPositionFactory
		"""

		if not isinstance(data, dict):
			raise ValueError("Expected dictionary for data")
		
		prefabricated_positions = {}
		
		for name in data.keys():

			entry = data[name]

			# Check data present
			if not "x" in entry:
				raise ValueError("Expected value for x but none was provided for this prefabricated position")
			x = entry["x"]
			if not "y" in entry:
				raise ValueError("Expected value for y but none was provided for this prefabricated position")
			y = entry["y"]
			if not "z" in entry:
				raise ValueError("Expected value for z but none was provided for this prefabricated position")
			z = entry["z"]
			if not "roll" in entry:
				raise ValueError("Expected value for roll but none was provided for this prefabricated position")
			roll = entry["roll"]
			if not "pitch" in entry:
				raise ValueError("Expected value for pitch but none was provided for this prefabricated position")
			pitch = entry["pitch"]
			if not "yaw" in entry:
				raise ValueError("Expected value for yaw but none was provided for this prefabricated position")
			yaw = entry["yaw"]
			
			# Create new position
			prefabricated_positions[name] = virtualobject.ObjectPosition(x, y, z, roll, pitch, yaw)
		
		return virtualobject.ObjectPositionFactory(ObjectPositionFactoryConstructor.DEFAULT_ROLL, ObjectPositionFactoryConstructor.DEFAULT_PITCH, ObjectPositionFactoryConstructor.DEFAULT_YAW, prefabricated_positions)