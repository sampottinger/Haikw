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
	
	def list_to_dict(self, target):
		"""
		Turns a list of Setups into a dictionary

		@param target: The Setups to turn into a dictionary
		@type target: Collection of Setups
		@return: Cooresponding dictionary filled with keys of Setup names and values of Setups
		@rtype: Dictionary
		"""

		return_dict = {}

		for setup in target:
			return_dict[setup.get_name()] : self.to_dict(setup)
		
		return return_dict

	def to_dict(self, target):
		"""
		Turns a setup into a dictionary describing the setup

		@param target: The setup to turn into dictionaries
		@type target: Setup
		@return: Dictionary with entries corresponding to the input setup
		@rtype: Dictionary
		"""

		virtual_object_serializer = VirtualObjectSerializer.get_instance()

		# Get each of the objects serialized
		virtual_objects = []
		for obj in setup.get_objects():
			serialized = virtual_object_serializer.to_dict(obj)
			virtual_objects.append(serialized)
		
		ret_dict = {}
		ret_dict["name"] = target.get_name()
		ret_dict["robot_state"] = target.get_robot_state()
		ret_dict["robot_descriptor"] = target.get_robot_descriptor()
		ret_dict["virtual_objects"] = virtual_objects

		return ret_dict
	
	def list_from_dict(self, target):
		"""
		Turns a dictionary filled with keys of Setup names into Setups

		@param target: Dictionary that contains information necessary to construct Setups
		@type target: Dictionary
		@return: List of Setups extracted from the provided dictionary
		@rtype: List of Setups
		"""

		ret_list = []

		for name in target.keys():
			ret_list.append(self.from_dict(target[name]))
		
		return ret_list

	def from_dict(self, target):
		"""
		Turns a dictionary containing information regarding a setup into an actual setup

		@param target: Dictionary containing information about the setup
		@type target: Dictionary
		@return: Cooresponding setup
		@rtype: Setup
		"""

		virtual_object_serializer = VirtualObjectSerializer.get_instance()

		# Get each of the objects serialized
		virtual_objects = []
		for obj in target["virtual_objects"]:
			deserialized = virtual_object_serializer.from_dict(obj)
			virtual_objects.append(deserialized)

		name = target["name"]
		robot_state = target["robot_state"]
		robot_descriptor = target["robot_descriptor"]

		return experiment.Setup(name, virtual_objects, robot_state, robot_descriptor)

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
