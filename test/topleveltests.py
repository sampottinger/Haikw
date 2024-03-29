"""
Unit tests for testing user exposed entry points

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

import unittest
import manipulation
import configurable
import virtualobject
import state
import dummy
import builders
	
class ToplevelTests(unittest.TestCase):
	""" Test suite for non-structure objects exposed to client code """

	def setUp(self):
		""" Establishes common objects for testing """

		# Test data
		self.test_color_data = {"red":{"red":255, "blue":10, "green":0}, "blue":{"red":0, "blue":250, "green":11}}
		self.test_size_data = {"small": [1, 2, 3], "large": [4, 5, 6]}
		self.test_position_data = {"small_offset": {"x": 1, "y": 2, "z": 3}, "large_offset": {"x":4, "y":5, "z":6, "roll": 0.1, "pitch":0.2, "yaw": 0.3}}
		self.prefab_data = {"small_red_cube": {"color": "red", "size":"small", "descriptor": "cube"},
							"large_blue_sphere": {"color": "blue", "size": "large", "descriptor": "sphere"}}

		# Create sample strategy for color resolution
		self.color_res_factory = configurable.ComplexColorResolutionFactory.get_instance()
		self.color_res_strategy = self.color_res_factory.create_strategy(self.test_color_data)

		# Create sample named size resolver
		self.size_res_factory = configurable.ComplexNamedSizeResolverFactory.get_instance()
		self.size_res_strategy = self.size_res_factory.create_resolver(self.test_size_data)

		# Create position factory
		self.position_factory_constructor = configurable.VirtualObjectPositionFactoryConstructor.get_instance()
		self.position_factory = self.position_factory_constructor.create_factory(self.test_position_data)

		# Create object resolver
		self.object_resolver_factory = configurable.MappedObjectResolverFactory.get_instance()
		self.object_resolver = self.object_resolver_factory.create_resolver(self.prefab_data, self.size_res_strategy, self.color_res_strategy)

		# Create positions
		small_offset = self.position_factory.create_prefabricated("small_offset")
		large_offset = self.position_factory.create_prefabricated("large_offset")
		
		# Create internal object builder
		construction_strategy = dummy.DummyConstructionStrategy()
		self.object_builder = builders.VirtualObjectBuilder(construction_strategy)

		# Create external object builder
		self.external_object_builder = builders.ComplexObjectBuilder(self.object_builder, self.object_resolver, self.position_factory, self.color_res_strategy, self.size_res_strategy)

		# Create test objects
		self.external_object_builder.load_from_config("small_red_cube")
		self.small_red_cube = self.external_object_builder.create("small_red_cube", "small_offset")
		self.external_object_builder.load_from_config("large_blue_sphere")
		self.large_blue_sphere = self.external_object_builder.create("large_blue_sphere", "large_offset")

		# Create dummy manipulation strategy
		self.manual_manipulation_strategy = dummy.DummyManipulationStrategy()

		# Create a manipulation facade without a factory
		self.manual_facade = manipulation.ObjectManipulationFacade(self.object_builder, self.manual_manipulation_strategy, self.color_res_strategy, self.size_res_strategy, self.position_factory, None, None, self.object_resolver)
	
	def test_external_builder_prototype_position(self):
		""" Test the creation of object positions purely by prototype """

		small_offset = self.small_red_cube.get_position()
		self.assertEqual(small_offset.get_x(), self.test_position_data["small_offset"]["x"])
		self.assertEqual(small_offset.get_y(), self.test_position_data["small_offset"]["y"])
		self.assertEqual(small_offset.get_z(), self.test_position_data["small_offset"]["z"])

		large_offset = self.large_blue_sphere.get_position()
		self.assertEqual(large_offset.get_x(), self.test_position_data["large_offset"]["x"])
		self.assertEqual(large_offset.get_y(), self.test_position_data["large_offset"]["y"])
		self.assertEqual(large_offset.get_z(), self.test_position_data["large_offset"]["z"])
		self.assertEqual(large_offset.get_roll(), self.test_position_data["large_offset"]["roll"])
		self.assertEqual(large_offset.get_pitch(), self.test_position_data["large_offset"]["pitch"])
		self.assertEqual(large_offset.get_yaw(), self.test_position_data["large_offset"]["yaw"])
	
	def test_external_builder_prototype_color(self):
		""" Test the creation of object colors purely by prototype """

		cube_red = self.small_red_cube.get_color()
		self.assertEqual(cube_red.get_red(), self.test_color_data["red"]["red"])
		self.assertEqual(cube_red.get_green(), self.test_color_data["red"]["green"])
		self.assertEqual(cube_red.get_blue(), self.test_color_data["red"]["blue"])

		sphere_blue = self.large_blue_sphere.get_color()
		self.assertEqual(sphere_blue.get_red(), self.test_color_data["blue"]["red"])
		self.assertEqual(sphere_blue.get_green(), self.test_color_data["blue"]["green"])
		self.assertEqual(sphere_blue.get_blue(), self.test_color_data["blue"]["blue"])
	
	def test_external_builder_prototype_position(self):
		""" Test the creation of object positions purely by prototype """

		small_offset = self.small_red_cube.get_position()
		self.assertEqual(small_offset.get_x(), self.test_position_data["small_offset"]["x"])
		self.assertEqual(small_offset.get_y(), self.test_position_data["small_offset"]["y"])
		self.assertEqual(small_offset.get_z(), self.test_position_data["small_offset"]["z"])

		large_offset = self.large_blue_sphere.get_position()
		self.assertEqual(large_offset.get_x(), self.test_position_data["large_offset"]["x"])
		self.assertEqual(large_offset.get_y(), self.test_position_data["large_offset"]["y"])
		self.assertEqual(large_offset.get_z(), self.test_position_data["large_offset"]["z"])
		self.assertEqual(large_offset.get_roll(), self.test_position_data["large_offset"]["roll"])
		self.assertEqual(large_offset.get_pitch(), self.test_position_data["large_offset"]["pitch"])
		self.assertEqual(large_offset.get_yaw(), self.test_position_data["large_offset"]["yaw"])
	
	def test_facade_access(self):
		""" Test the use of a manipulation facade to add, delete, and get objs """
		# Add
		self.manual_facade.add_object(self.small_red_cube)
		self.manual_facade.add_object(self.large_blue_sphere)
		
		# Test simple reads
		hopefully_red_cube = self.manual_facade.get_object(self.small_red_cube.get_name())
		self.assertEqual(hopefully_red_cube.get_name(), self.small_red_cube.get_name())
		hopefully_blue_sphere = self.manual_facade.get_object(self.large_blue_sphere.get_name())
		self.assertEqual(hopefully_blue_sphere.get_name(), self.large_blue_sphere.get_name())

		# Test read all
		all_objs = self.manual_facade.get_objects()
		all_objs_names = map(lambda x: x.get_name(), all_objs)
		self.assertIn(self.small_red_cube.get_name(), all_objs_names)
		self.assertIn(self.large_blue_sphere.get_name(), all_objs_names)

		# Test delete
		self.manual_facade.delete(self.small_red_cube)
		all_objs = self.manual_facade.get_objects()
		all_objs_names = map(lambda x: x.get_name(), all_objs)
		self.assertNotIn(self.small_red_cube.get_name(), all_objs_names)
		self.assertIn(self.large_blue_sphere.get_name(), all_objs_names)

		self.manual_facade.delete("large_blue_sphere")
		all_objs = self.manual_facade.get_objects()
		all_objs_names = map(lambda x: x.get_name(), all_objs)
		self.assertNotIn("large_blue_sphere", all_objs_names)
	
	def test_facade_builder(self):
		""" Test that the builder produced by the manipulation facade is valid """

		generated_builder = self.manual_facade.get_object_builder()
		generated_builder.load_from_config("small_red_cube")
		small_red_cube = generated_builder.create("small_red_cube", "small_offset")
		self.assertEqual(small_red_cube.get_descriptor(), "cube")
	
	def test_facade_update(self):
		""" Test that the facade can update target simulations """

		self.manual_facade.add_object(self.small_red_cube)
		new_position = state.VirtualObjectPosition(10, 11, 12, 0, 0, 0)
		self.manual_facade.update(self.small_red_cube, new_position)
		test_cube = self.manual_facade.get_object(self.small_red_cube.get_name())

		test_position = test_cube.get_position()
		self.assertEqual(test_position.get_x(), new_position.get_x())
		self.assertEqual(test_position.get_y(), new_position.get_y())
		self.assertEqual(test_position.get_z(), new_position.get_z())

		self.manual_facade.delete(test_cube)
	
	def test_facade_grab(self):
		""" That that the facade can grab objects in simulations """

		self.manual_facade.add_object(self.small_red_cube)
		self.manual_facade.grab(self.small_red_cube)
		self.assertEqual(self.manual_manipulation_strategy.grabbed.get_name(), self.small_red_cube.get_name())
		self.manual_facade.release()
		self.assertEqual(self.manual_manipulation_strategy.grabbed, None)
		self.manual_facade.grab(self.small_red_cube.get_name())
		self.assertEqual(self.manual_manipulation_strategy.grabbed.get_name(), self.small_red_cube.get_name())
		self.manual_facade.delete(self.small_red_cube)
		self.assertEqual(self.manual_manipulation_strategy.grabbed, None)
	
	def test_facade_face_position(self):
		""" Test that the facade can face a position in the simulation """
		target_position = state.VirtualObjectPosition(1, 2, 3, roll=0.4, pitch=0.5, yaw=0.6)
		self.manual_facade.face(target_position)
		actual_position = self.manual_manipulation_strategy.facing
		self.assertEqual(actual_position.get_x(), target_position.get_x())
		self.assertEqual(actual_position.get_y(), target_position.get_y())
		self.assertEqual(actual_position.get_z(), target_position.get_z())
		self.assertEqual(actual_position.get_roll(), target_position.get_roll())
		self.assertEqual(actual_position.get_pitch(), target_position.get_pitch())
		self.assertEqual(actual_position.get_yaw(), target_position.get_yaw())
	
	def test_facade_face_object(self):
		""" Test that the facade can face an object in the simulation """
		self.manual_facade.face(self.large_blue_sphere)
		actual_position = self.manual_manipulation_strategy.facing
		target_position = self.large_blue_sphere.get_position()
		self.assertEqual(actual_position.get_x(), target_position.get_x())
		self.assertEqual(actual_position.get_y(), target_position.get_y())
		self.assertEqual(actual_position.get_z(), target_position.get_z())
		self.assertEqual(actual_position.get_roll(), target_position.get_roll())
		self.assertEqual(actual_position.get_pitch(), target_position.get_pitch())
		self.assertEqual(actual_position.get_yaw(), target_position.get_yaw())
	
	def test_facade_face_prefab_position(self):
		""" Test that the facade can face a named prefabricated position """
		self.manual_facade.face("small_offset")
		actual_position = self.manual_manipulation_strategy.facing
		target_position = self.position_factory.create_prefabricated("small_offset")
		self.assertEqual(actual_position.get_x(), target_position.get_x())
		self.assertEqual(actual_position.get_y(), target_position.get_y())
		self.assertEqual(actual_position.get_z(), target_position.get_z())
		self.assertEqual(actual_position.get_roll(), target_position.get_roll())
		self.assertEqual(actual_position.get_pitch(), target_position.get_pitch())
		self.assertEqual(actual_position.get_yaw(), target_position.get_yaw())

	def test_facade_face_registered_object(self):
		""" Test that the facade can face an object in the simulation """
		self.manual_facade.add_object(self.small_red_cube)
		self.manual_facade.face("small_red_cube")
		actual_position = self.manual_manipulation_strategy.facing
		target_position = self.small_red_cube.get_position()
		self.assertEqual(actual_position.get_x(), target_position.get_x())
		self.assertEqual(actual_position.get_y(), target_position.get_y())
		self.assertEqual(actual_position.get_z(), target_position.get_z())
		self.assertEqual(actual_position.get_roll(), target_position.get_roll())
		self.assertEqual(actual_position.get_pitch(), target_position.get_pitch())
		self.assertEqual(actual_position.get_yaw(), target_position.get_yaw())
		self.manual_facade.delete(self.small_red_cube)
	
	def test_facade_put(self):
		""" Test that the facade can place objects in the simulation """
		self.manual_facade.add_object(self.small_red_cube)
		self.manual_facade.put(self.small_red_cube, "large_offset")
		# WARNING: dummy does not track objects. This could be used to verify put method and should be fixed in future revision on unit testing
