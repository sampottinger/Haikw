"""
Module containing objects providing management of state

This module provides state containing objects that manage state inherent to inverse kinematics simulations

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

class VirtualObjectPosition:
	"""
	Immutable generic position / orientation flyweight in an inverse kinematics simulation

	Package independent representation of a position and orientation in the target inverse kinematics software

	@note: Should be created through an VirtualObjectPositionFactory
	"""

	def __init__(x, y, z, roll, pitch, yaw):
		""" Default constructor for an VirtualObjectPosition

		@param x: The x component of this position
		@type x: float
		@param y: The y component of this position
		@type y: float
		@param z: The z component of this position
		@type z: float
		@param roll: The roll (rotation about x axis) component of this orientation
		@type roll: float
		@param pitch: The pitch (rotation about y axis) component of this orientation
		@type pitch: float
		@param yaw: The yaw (rotation about the z axis) component of this orientation
		@type yaw: float """

		self.__x = x
		self.__y = y
		self.__z = z
		self.__roll = roll
		self.__pitch = pitch
		self.__yaw = yaw
	
	def get_x():
		""" Determine's this position's x component

		@return: This position's x component
		@rtype: float """

		return self.__x
	
	def get_y():
		""" Determine's this position's y component

		@return: This position's y component
		@rtype: float """

		return self.__y
	
	def get_z():
		""" Determine's this position's z component

		@return: This position's z component
		@rtype: float """

		return self.__z
	
	def get_roll():
		""" Determine's this orientations's x component (roll)

		@return: This orientation's roll
		@rtype: float """

		return self.__roll
	
	def get_pitch():
		""" Determine's this orientations's y component (pitch)

		@return: This orientation's pitch
		@rtype: float """

		return self.__pitch
	
	def get_yaw():
		""" Determine's this orientations's z component (yaw)

		@return: This orientation's yaw
		@rtype: float """

		return self.__yaw



class VirtualObjectPositionFactory:
	"""
	Factory to create VirtualObjectPositions that leverages predefined names, defaults, and other conveniences.

	@note: Should be created through an ObjectManipulationFacade and its VirtualObjectPositionFactoryConstructor
	"""

	DEFAULT = None
	
	def __init__(self, default_roll, default_pitch, default_yaw, prefabricated_positions):
		""" Constructor for an VirtualObjectPositionFactory
		
		@param default_roll: The default roll applied to new positions
		@type default_roll: float
		@param default_pitch: The default pitch applied to new positions
		@type default_pitch: float
		@param default_yaw: The default yaw applied to new positions
		@type default_yaw: float
		@param prefabricated_positions: Named default positions
		@type prefabricated_positions: Dictionary of String to VirtualObjectPosition"""

		self.__default_roll = default_roll
		self.__default_pitch = default_pitch
		self.__default_yaw = default_yaw
		self.__prefabricated_positions = prefabricated_positions
	
	def create_position(self, x, y, z, roll=VirtualObjectPositionFactory.DEFAULT, pitch=VirtualObjectPositionFactory.DEFAULT, yaw=VirtualObjectPositionFactory.DEFAULT):

		""" Creates a new position by values

		@param x: The x component of this new position
		@type x: float
		@param y: The y component of this new position
		@type y: float
		@param z: The z component of this new position
		@type z: float
		@keyword roll: The roll component of this new orientation, defaults to the roll provided in init
		@type: roll: float
		@keyword pitch: The pitch component of this new orientation, defaults to the pitch provided in init
		@type: pitch: float
		@keyword yaw: The yaw component of this new orientation, defaults to the yaw provided in init
		@type: yaw: float 
		@return: New position that fits the provided parameters
		@type: VirtualObjectPosition"""

		# Resolve defaults
		if roll == VirtualObjectPosition.DEFAULT:
			roll = self.__default_roll

		if pitch == VirtualObjectPosition.DEFAULT:
			pitch = self.__default_pitch

		if yaw == VirtualObjectPosition.DEFAULT:
			yaw = self.__default_yaw
		
		return VirtualObjectPosition(x, y, z, roll, pitch, yaw)
	
	def create_prefabricated(name, x=VirtualObjectPositionFactory.DEFAULT, y=VirtualObjectPositionFactory.DEFAULT, z=VirtualObjectPositionFactory.DEFAULT, roll=VirtualObjectPositionFactory.DEFAULT, pitch=VirtualObjectPositionFactory.DEFAULT, yaw=VirtualObjectPositionFactory.DEFAULT):
		""" Creates a new position based off of the named prefabricated position
			
		@param name: The name of the prefabrication to base this new position off of
		@type name: String
		@keyword x: Specifies the x component of the new position, defaults to the x position specified in the desired prefabrication
		@type x: float
		@keyword y: Specifies the y component of the new position, defaults to the y position specified in the desired prefabrication
		@type y: float
		@keyword z: Specifies the z component of the new position, defaults to the z position specified in the desired prefabrication
		@type z: float
		@keyword roll: Specifies the roll of the new orientation, defaults to the roll specified in the desired prefabrication
		@type roll: float
		@keyword pitch: Specifies the pitch of the new orientation, defaults to the pitch specified in the desired prefabrication
		@type pitch: float
		@keyword yaw: Specifies the yaw of the new orientation, defaults to the yaw specified in the desired prefabrication
		@type yaw: float 
		@raise ValueError: Raised if the requested prefabricated position has not been specified previously"""
	
		# Attempt to find the prefabrication, throwing an exception if not available
		if not name in self.__prefabricated_positions:
			raise ValueError("Prefabricated position not defined")
		
		position = self.__prefabricated_positions[name]

		return self.clone(position, x, y, z, roll, pitch, yaw)
		
	def clone(position, x=VirtualObjectPositionFactory.DEFAULT, y=VirtualObjectPositionFactory.DEFAULT, z=VirtualObjectPositionFactory.DEFAULT, roll=VirtualObjectPositionFactory.DEFAULT, pitch=VirtualObjectPositionFactory.DEFAULT, yaw=VirtualObjectPositionFactory.DEFAULT):
		""" Creates a new position based off of the given position 

		@param position: The position to base the new position off of
		@type: VirtualObjectPosition
		@keyword x: Specifies the x component of the new position, defaults to the x position specified in the position provided to clone
		@type x: float
		@keyword y: Specifies the y component of the new position, defaults to the y position specified in the position provided to clone
		@type y: float
		@keyword z: Specifies the z component of the new position, defaults to the z position specified in the position provided to clone
		@type z: float
		@keyword roll: Specifies the roll of the new orientation, defaults to the roll specified in the position provided to clone
		@type roll: float
		@keyword pitch: Specifies the pitch of the new orientation, defaults to the pitch specified in the position provided to clone
		@type pitch: float
		@keyword yaw: Specifies the yaw of the new orientation, defaults to the yaw specified in the position provided to clone
		@type yaw: float """

		if x == VirtualObjectPositionFactory.DEFAULT:
			x = position.get_x()
		
		if y == VirtualObjectPositionFactory.DEFAULT:
			y = position.get_y()
		
		if z == VirtualObjectPositionFactory.DEFAULT:
			z = position.get_z()

		if roll == VirtualObjectPositionFactory.DEFAULT:
			roll = position.get_roll()
		
		if pitch == VirtualObjectPositionFactory.DEFAULT:
			pitch = position.get_pitch()
		
		if yaw == VirtualObjectPositionFactory.DEFAULT:
			yaw = position.get_yaw()
		
		return VirtualObjectPosition(x, y, z, roll, pitch, yaw)
	
	def create_position_relative(position, x, y, z, roll=VirtualObjectPositionFactory.DEFAULT, pitch=VirtualObjectPositionFactory.DEFAULT, yaw=VirtualObjectPositionFactory.DEFAULT):
		""" Creates a new position based off of the given position 

		@param position: The position to base the new position off of
		@type: VirtualObjectPosition
		@param x: Specifies the x component of the new position, computed relative to the provided existing position
		@type x: float
		@param y: Specifies the y component of the new position, computed relative to the provided existing position
		@type y: float
		@param z: Specifies the z component of the new position, computed relative to the provided existing position
		@type z: float
		@keyword roll: Specifies the roll of the new orientation, defaults to the roll specified when this factory was created
		@type roll: float
		@keyword pitch: Specifies the pitch of the new orientation, defaults to the pitch specified when this factory was created
		@type pitch: float
		@keyword yaw: Specifies the yaw of the new orientation, defaults to the yaw specified when this factory was created
		@type yaw: float """

		# Resolve defaults
		if roll == VirtualObjectPosition.DEFAULT:
			roll = self.__default_roll

		if pitch == VirtualObjectPosition.DEFAULT:
			pitch = self.__default_pitch

		if yaw == VirtualObjectPosition.DEFAULT:
			yaw = self.__default_yaw
		
		# Compute relative values
		x = x + position.get_x()
		y = y + position.get_y()
		z = z + position.get_z()
		roll = roll + position.get_roll()
		pitch = pitch + position.get_pitch()
		yaw = yaw + position.get_yaw()

		return VirtualObjectPosition(x, y, z, roll, pitch, yaw)