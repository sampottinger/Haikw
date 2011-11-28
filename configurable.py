"""
Module containing factories driven by user provided configuration

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

import re
import virtualobject
import state

class ComplexColorResolutionFactory:
	"""
	Factory singleton creating ComplexColorResolutionStrategies from dicts
	"""

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of this ComplexColorResolutionFactory, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: ComplexColorResolutionFactory
		"""

		if not ComplexColorResolutionFactory.__instance:
			ComplexColorResolutionFactory.__instance = ComplexColorResolutionFactory()
		
		return ComplexColorResolutionFactory.__instance
	
	def __init__(self):
		"""
		Constructor for ComplexColorResolutionFactory

		@note: This class is a singleton and this should only be called internally
		"""
		pass
	
	def create_strategy(self, data):
		"""
		Creates a new ComplexColorResolutionStrategy from the given data

		@param data: dict 
		@type data: Dictionary of the form {"colorname":{"red":decimal, "green":decimal, "blue":decimal}} or {"colorname":"#rrggbb"}
		"""

		strategy = virtualobject.ComplexColorResolutionStrategy()

		for name in data.keys():

			# Add it to the new strategy
			strategy.add_color(name, data[name])
		
		return strategy

class MappedObjectResolverFactory:
	""" 
	Factory singleton to create MappedObjectResolver from Python dictionaries
	"""

	DESCRIPTOR = "descriptor"
	SIZE = "size"
	COLOR = "color"

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of this MappedObjectResolverFactory, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: MappedObjectResolverFactory
		"""

		if not MappedObjectResolverFactory.__instance:
			MappedObjectResolverFactory.__instance = MappedObjectResolverFactory()
		
		return MappedObjectResolverFactory.__instance
	
	def __init__(self):
		"""
		Constructor for MappedObjectResolverFactory

		@note: This class is a singleton and this should only be called internally
		"""
		pass
	
	def create_resolver(self, prototypes, size_resolver, color_resolver):
		"""
		Creates a new MappedObjectResolver

		@param prototypes: Python attributes loaded from configuration files
		@type prototypes: Dictionary containing descriptor, size, color
		@param size_resolver: Resolver from names to sizes
		@type size_resolver: NamedSizeResolver implementor
		@param color_resolver: Resolver from names to colors
		@type color_resolver: ColorResolutionStrategy
		@return: New MappedObjectResolver instance
		@rtype: MappedObjectResolver
		"""
		# Create new resolver
		resolver = virtualobject.MappedObjectResolver()

		for name in prototypes:
			data = prototypes[name]

			# Extract descriptor
			if not MappedObjectResolverFactory.DESCRIPTOR in data:
				raise ValueError("This prototype description does not include a descriptor")
			
			descriptor = data[MappedObjectResolverFactory.DESCRIPTOR]

			# Extract size
			if not MappedObjectResolverFactory.SIZE in data:
				raise ValueError("This prototype description does not include a size")
			
			size = size_resolver.get_size(data[MappedObjectResolverFactory.SIZE])

			# Extract color
			if not MappedObjectResolverFactory.COLOR in data:
				raise ValueError("This prototype description does not include a color")
			
			color = color_resolver.get_color(data[MappedObjectResolverFactory.COLOR])	
			# Create flyweight and add
			flyweight = virtualobject.ObjectResolverFlyweight(color, size, descriptor)
			
			# Add to new resolover
			resolver.add_object(name, flyweight)
		
		return resolver

class ComplexNamedSizeResolverFactory:
	""" 
	Factory singleton to create ComplexNamedSizeResolver from Python dictionaries 
	"""

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of this ComplexNamedSizeResolverFactory, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: ComplexNamedSizeResolverFactory
		"""

		if not ComplexNamedSizeResolverFactory.__instance:
			ComplexNamedSizeResolverFactory.__instance = ComplexNamedSizeResolverFactory()
		
		return ComplexNamedSizeResolverFactory.__instance
	
	def __init__(self):
		"""
		Constructor for ComplexNamedSizeResolverFactory

		@note: This class is a singleton and this should only be called internally
		"""
		pass
	
	def create_resolver(self, data):
		"""
		Creates a new ComplexNamedSizeResolver

		@param data: Python attributes loaded from configuration files
		@type: Dictionary containing {"name" : [float1, float2]}
		@return: New ComplexNamedSizeResolver instance
		@rtype: ComplexNamedSizeResolver
		"""

		new_resolver = virtualobject.ComplexNamedSizeResolver()

		if not isinstance(data, dict):
			raise ValueError("Expected dictionary for data")

		for name in data.keys():
			new_size = virtualobject.VirtualObjectSize(data[name])
			new_resolver.add_size(name, new_size)
		
		return new_resolver

class SetupManagerFactory:
	"""
	Factory singleton that creates a SetupManager
	"""

	COLOR = "color"
	POSITION = "position"
	DESCRIPTOR = "descriptor"
	SIZE = "size"

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of this SetupManagerFactory, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: SetupManagerFactory
		"""

		if not SetupManagerFactory.__instance:
			SetupManagerFactory.__instance = SetupManagerFactory()
		
		return SetupManagerFactory.__instance
	
	def create_setup_manager(self, data, obj_builder):
		"""
		Creates a new SetupManager

		@param data: Dictionary containing a setup strategy of form {"setup_1":{"test_block":{"color":"red", "position":"origin", "size":"small", descriptor:"cube"}}}
		@type data: Dict
		@param obj_builder: Builder used to make virtual objects
		@type obj_builder: ComplexObjectBuilder
		@return: A new SetupManager cooresponding to provided dictionary
		@rtype: SetupManager
		"""
		setups = {}

		# Iterate through names of setups
		for setup_name in data:

			setup_data = data[setup_name]

			# Iterate through names of objects in setups
			setup_objs = []
			for obj_name in setup_data:

				# Get data to build object
				obj_data = setup_data[obj_name]

				# Setup builder by individual properties
				if isinstance(objdata, dict):

					# Extract required data
					color_data = obj_data[SetupManagerFactory.COLOR]
					position_data = obj_data[SetupManagerFactory.POSITION]
					descriptor_data = obj_data[SetupManagerFactory.DESCRIPTOR]
					size_data = obj_data[SetupManagerFactory.SIZE]

					# Setup builder
					obj_builder.set_descriptor(descriptor_data)
					obj_builder.set_position(position_data)
					obj_builder.set_color(color_data)
				
				# Load by prototype
				elif isinstance(objdata, str):

					obj_builder.load_from_config(objdata)
				
				else:
					raise TypeError("Expected string prototype name or dictionary describing object.")

				new_obj = obj_builder.create(obj_name, position_data)

				setup_objs.append(new_obj)

			new_setup = experiment.Setup(setup_name, setup_objs)
			setups[setup_name] = new_setup

		new_manager = experiment.SetupManager(setups)
		return new_manager


class VirtualObjectPositionFactoryConstructor:
	"""
	Factory singleton that creates VirtualObjectPositionFactory
	"""

	DEFAULT_ROLL = 0
	DEFAULT_PITCH = 0
	DEFAULT_YAW = 0

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of this VirtualObjectPositionFactoryConstructor, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: VirtualObjectPositionFactoryConstructor
		"""

		if not VirtualObjectPositionFactoryConstructor.__instance:
			VirtualObjectPositionFactoryConstructor.__instance = VirtualObjectPositionFactoryConstructor()
		
		return VirtualObjectPositionFactoryConstructor.__instance
	
	def __init__(self):
		"""
		Constructor for VirtualObjectPositionFactoryConstructor

		@note: This class is a singleton and this should only be called internally
		"""
		pass
	
	def create_factory(self, data):
		"""
		Creates a new VirtualObjectPositionFactory from the given data

		@param data: Data loaded from configuration files
		@type data: Dictionary of form {"name" : {"x":float, "y":float, "z":float, "roll":float, "pitch":float, "yaw":float}}
		@return: New VirtualObjectPositionFactory instance with the given data as prefabricated positions
		@rtype: VirtualObjectPositionFactory
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
				roll = VirtualObjectPositionFactoryConstructor.DEFAULT_ROLL
			else:
				roll = entry["roll"]

			if not "pitch" in entry:
				pitch = VirtualObjectPositionFactoryConstructor.DEFAULT_PITCH
			else:
				pitch = entry["pitch"]
			
			if not "yaw" in entry:
				yaw = VirtualObjectPositionFactoryConstructor.DEFAULT_YAW
			else:
				yaw = entry["yaw"]
			
			# Create new position
			prefabricated_positions[name] = state.VirtualObjectPosition(x, y, z, roll, pitch, yaw)
		
		return state.VirtualObjectPositionFactory(VirtualObjectPositionFactoryConstructor.DEFAULT_ROLL, VirtualObjectPositionFactoryConstructor.DEFAULT_PITCH, VirtualObjectPositionFactoryConstructor.DEFAULT_YAW, prefabricated_positions)