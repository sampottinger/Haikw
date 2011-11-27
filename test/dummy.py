import virtualobject
import experiment
import manipulation

class DummyConstructionStrategy(virtualobject.VirtualObjectConstructionStrategy):
	""" Virtual object construction strategy that does exactly nothing """

	def __init__(self):
		virtualobject.VirtualObjectConstructionStrategy.__init__(self)
	
	def create_object(self, virtual_object):
		pass

class DummyManipulationStrategy(manipulation.VirtualObjectManipulationStrategy):
	""" Virtual object manipulation strategy for testing """

	def __init__(self):
		self.default_affector = experiment.RobotPart("test_affector")
		self.grabbed = None
		self.facing = None
	
	def get_default_affector(self):
		return self.default_affector
	
	def refresh(self, target):
		return target
	
	def grab(self, target, affector):
		if not affector == self.default_affector:
			raise ValueError("Expected affector to be default affector")

		self.grabbed = target
	
	def face(self, position, affector):
		if not affector == self.default_affector:
			raise ValueError("Expected affector to be default affector")
		
		self.facing = position
		if self.grabbed != None:
			self.update(self.grabbed, position)
	
	def update(self, target, position):
		return virtualobject.VirtualObject(target.get_name(), position, target.get_descriptor(), target.get_color(), target.get_size())
	
	def release(self, affector):
		if not affector == self.default_affector:
			raise ValueError("Expected affector to be default affector")
		
		self.grabbed = None
	
	def delete(self, target):
		if self.grabbed == target:
			self.grabbed = None
