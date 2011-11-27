import virtualobject
import experiment

class DummyConstructionStrategy(virtualobject.VirtualObjectConstructionStrategy):
	""" Virtual object construction strategy that does exactly nothing """

	def __init__(self):
		virtualobject.VirtualObjectConstructionStrategy.__init__(self)
	
	def create_object(self, virtual_object):
		pass

class DummyManipulationStrategy(virtualobject.VirtualObjectManipulationStrategy):
	""" Virtual object manipulation strategy for testing """

	def __init__(self):
		self.virtual_objects = {}
		self.default_affector = experiment.RobotPart("test_affector")
		self.grabbed = None
		self.facing = None
	
	def get_default_affector(self):
		return self.default_affector
	
	def refresh(self, target, affector):
		if not affector == self.default_affector:
			raise ValueError("Expected affector to be default affector")
		
		return self.virtual_objects[target.get_name()]
	
	def grab(self, target, affector):
		if not affector == self.default_affector:
			raise ValueError("Expected affector to be default affector")

		self.grabbed = target
	
	def face(self, position, affector):
		if not affector == self.default_affector:
			raise ValueError("Expected affector to be default affector")
		
		self.facing = position
	
	def update(self, target, position):

		self.virtual_objects[target.get_name()] = virtualobject.VirtualObject(target.get_name(), position, target.get_descriptor(), target.get_color(), target.get_size())
	
	def release(self, affector):
		if not affector == self.default_affector:
			raise ValueError("Expected affector to be default affector")
		
		self.grabbed = None
	
	def delete(self, target):
		del self.virtual_objects[target.get_name()]