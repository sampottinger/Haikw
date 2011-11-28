"""
Module containing classes related to package / library specific strategies

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

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