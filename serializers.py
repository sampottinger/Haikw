"""
Module containing serializers
"""

import experiment
import virtualobject
import state

class SetupSerializer:
	"""
	Serializes setups to and from dictionaries
	"""

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of SetupSeralizer, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: SetupSerializer
		"""
		if not SetupSerializer.__instance:
			SetupSerializer.__instance = SetupSerializer()
		
		return SetupSerializer.__instance
	
	def to_dict(self, target):
		"""
		Turns a list of setups into a dictionary describing the setups

		@param target: The list of setups to turn into dictionaries
		@type target: List of Setup
		@return: Dictionary with entries corresponding to the input setups
		@rtype: Dictionary
		"""

		virtual_object_serializer = VirtualObjectSerializer.get_instance()

		ret_list = {}
		for setup in target:
			name = setup.get_name()

			# Get each of the objects serialized
			virtual_objects = []
			for obj in setup.get_objects():
				serialized = virtual_object_serializer.to_dict(obj)
				virtual_objects.append(serialized)

			ret_list[name] = virtual_objects
	
	def from_dict(self, target):
		"""
		Turns a dictionary containing information regarding setups into actual setups

		@param target: Dictionary containing information about the setups
		@type target: Dictionary
		@return: List of corresponding setups
		@rtype: List of Setups
		"""

		virtual_object_serializer = VirtualObjectSerializer.get_instance()

		ret_list = []

		for name in target.get_keys():

			# Get each of the objects de-serialized
			virtual_objects = []
			for obj in target[name]:
				unserialized = virtual_object_serializer.from_dict(obj)
				virtual_objects.append(obj)
			
			new_setup = experiment.Setup(name, virtual_objects)
			ret_list.append(new_setup)
		
		return ret_list

class VirtualObjectSerializer:
	"""
	Serializes simulated objects to and from dictionaries
	"""

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of this singleton, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: SetupSerializer
		"""
		if not VirtualObjectSerializer.__instance:
			VirtualObjectSerializer.__instance = VirtualObjectSerializer()
		
		return VirtualObjectSerializer.__instance
	
	def to_dict(self, target):
		"""
		Turns a virtual object into a dictionary

		@param target: The virtual object to serialize
		@type target: VirtualObject
		@return: Dictionary with entries corresponding to the input 
		@rtype: Dictionary
		"""

		color_serializer = ColorSerializer.get_instance()
		position_serializer = PositionSerializer.get_instance()

		return_dict = {}
		return_dict["name"] = target.get_name()
		return_dict["position"] = target.get_position()
		return_dict["descriptor"] = target.get_descriptor()
		return_dict["color"] = color_serializer.to_dict(target.get_color())
		return_dict["position"] = position_serializer.to_dict(target.get_position())
	
	def from_dict(self, target):
		"""
		Turns a dictionary into a virtual object

		@param target: Dictionary containing information about the setups
		@type target: Dictionary
		@return: Corresponding virtual object
		@rtype: VirtualObject
		"""
		color_serializer = ColorSerializer.get_instance()
		position_serializer = PositionSerializer.get_instance()

		name = target["name"]
		position = target["position"]
		descriptor = target["descriptor"]
		color = color_serializer.from_dict(target["color"])
		position = position_serializer.from_dict(target["position"])

		return VirtualObject(name, position, descriptor, color, position)

class ColorSerializer:
	"""
	Serializes colors to and from dictionaries
	"""

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of ColorSerializer, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: ColorSerializer
		"""
		if not ColorSerializer.__instance:
			ColorSerializer.__instance = ColorSerializer()
		
		return ColorSerializer.__instance
	
	def to_dict(self, target):
		"""
		Turns a color into a dictionary

		@param target: The color to serialize
		@type target: VirtualObjectColor
		@return: Dictionary with entries corresponding to the input 
		@rtype: Dictionary
		"""

		ret_val = {}

		ret_val["red"] = target.get_red()
		ret_val["green"] = target.get_green()
		ret_val["blue"] = target.get_blue()

		return ret_val

	def from_dict(self, target):
		"""
		Turns a dictionary into a color

		@param target: Dictionary containing information about the color
		@type target: Dictionary
		@return: Corresponding color
		@rtype: VirtualObjectColor
		"""

		red = target["red"]
		green = target["green"]
		blue = target["blue"]

		return virtualobject.VirtualObjectColor(red, green, blue)

class PositionSerializer:
	"""
	Serializes positions to and from dictionaries
	"""

	__instance = None

	@classmethod
	def get_instance(self):
		"""
		Returns a shared instance of PositionSerializer, creating it if necessary

		@return: Shared instance of this singleton
		@rtype: PositionSerializer
		"""
		if not PositionSerializer.__instance:
			PositionSerializer.__instance = PositionSerializer()
		
		return PositionSerializer.__instance
	
	def to_dict(self, target):
		"""
		Turns a position into a dictionary

		@param target: The position to serialize
		@type target: ObjectPosition
		@return: Dictionary with entries corresponding to the input 
		@rtype: Dictionary
		"""

		ret_val = {}

		ret_val["x"] = target.get_x()
		ret_val["y"] = target.get_y()
		ret_val["z"] = target.get_z()
		ret_val["roll"] = target.get_roll()
		ret_val["pitch"] = target.get_pitch()
		ret_val["yaw"] = target.get_yaw()

		return ret_val
	
	def from_dict(self, target):
		"""
		Turns a dictionary into a position

		@param target: Dictionary containing information about the position
		@type target: Dictionary
		@return: Corresponding position
		@rtype: ObjectPosition
		"""

		x = target["x"]
		y = target["y"]
		z = target["z"]
		roll = target["roll"]
		pitch = target["pitch"]
		yaw = target["yaw"]

		return state.ObjectPosition(x, y, z, roll, pitch, yaw)
