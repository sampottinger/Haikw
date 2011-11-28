"""
Unit tests for testing "behind the scenes" mechanisms relient on other tested mechanisms

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

import unittest
import configurable
import virtualobject
import dummy
	
class MidlevelTests(unittest.TestCase):
	""" Test suite for "midlevel" management objects """

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
		
		# Create object builder
		construction_strategy = dummy.DummyConstructionStrategy()
		self.object_builder = virtualobject.VirtualObjectBuilder(construction_strategy)

		# Test small red cube
		self.object_builder.set_descriptor("cube")
		self.object_builder.set_color(self.color_res_strategy.get_color("red"))
		self.object_builder.set_size(self.size_res_strategy.get_size("small"))
		self.small_red_cube = self.object_builder.create("small_red_cube", small_offset)

		# Test large red sphere
		self.object_builder.set_descriptor("sphere")
		self.object_builder.set_size(self.size_res_strategy.get_size("large"))
		self.large_red_sphere = self.object_builder.create("large_red_sphere", large_offset)

	def test_object_resolver_color(self):
		""" Test the object resolver factory color resolution by checking the object resolver it produces """

		red = self.object_resolver.get_color("small_red_cube")
		self.assertEqual(red.get_red(), self.test_color_data["red"]["red"])
		self.assertEqual(red.get_green(), self.test_color_data["red"]["green"])
		self.assertEqual(red.get_blue(), self.test_color_data["red"]["blue"])

		blue = self.object_resolver.get_color("large_blue_sphere")
		self.assertEqual(blue.get_red(), self.test_color_data["blue"]["red"])
		self.assertEqual(blue.get_green(), self.test_color_data["blue"]["green"])
		self.assertEqual(blue.get_blue(), self.test_color_data["blue"]["blue"])

	def test_object_resolver_size(self):
		""" Test the object resolver factory size resolution by checking the object resolver it produces """

		small = self.object_resolver.get_size("small_red_cube")
		self.assertEqual(small[0], self.test_size_data["small"][0])
		self.assertEqual(small[1], self.test_size_data["small"][1])
		self.assertEqual(small[2], self.test_size_data["small"][2])

		large = self.object_resolver.get_size("large_blue_sphere")
		self.assertEqual(large[0], self.test_size_data["large"][0])
		self.assertEqual(large[1], self.test_size_data["large"][1])
		self.assertEqual(large[2], self.test_size_data["large"][2])
	
	def test_object_resolver_descriptor(self):
		""" Test the object resolver factory descriptor resolution by checking the object resolver it produces """

		cube = self.object_resolver.get_descriptor("small_red_cube")
		self.assertEqual(cube, "cube")

		sphere = self.object_resolver.get_descriptor("large_blue_sphere")
		self.assertEqual(sphere, "sphere")
	
	def test_built_color(self):
		""" Test builder built object color """
		cube_red = self.small_red_cube.get_color()
		self.assertEqual(cube_red.get_red(), self.test_color_data["red"]["red"])
		self.assertEqual(cube_red.get_green(), self.test_color_data["red"]["green"])
		self.assertEqual(cube_red.get_blue(), self.test_color_data["red"]["blue"])

		sphere_red = self.large_red_sphere.get_color()
		self.assertEqual(sphere_red.get_red(), self.test_color_data["red"]["red"])
		self.assertEqual(sphere_red.get_green(), self.test_color_data["red"]["green"])
		self.assertEqual(sphere_red.get_blue(), self.test_color_data["red"]["blue"])
	
	def test_built_position(self):
		""" Test builder built object position """
		small_offset = self.small_red_cube.get_position()
		self.assertEqual(small_offset.get_x(), self.test_position_data["small_offset"]["x"])
		self.assertEqual(small_offset.get_y(), self.test_position_data["small_offset"]["y"])
		self.assertEqual(small_offset.get_z(), self.test_position_data["small_offset"]["z"])

		large_offset = self.large_red_sphere.get_position()
		self.assertEqual(large_offset.get_x(), self.test_position_data["large_offset"]["x"])
		self.assertEqual(large_offset.get_y(), self.test_position_data["large_offset"]["y"])
		self.assertEqual(large_offset.get_z(), self.test_position_data["large_offset"]["z"])
		self.assertEqual(large_offset.get_roll(), self.test_position_data["large_offset"]["roll"])
		self.assertEqual(large_offset.get_pitch(), self.test_position_data["large_offset"]["pitch"])
		self.assertEqual(large_offset.get_yaw(), self.test_position_data["large_offset"]["yaw"])
	
	def test_built_descriptor(self):
		""" Test builder built object descriptor """
		cube = self.small_red_cube.get_descriptor()
		sphere = self.large_red_sphere.get_descriptor()

		self.assertEqual(cube, "cube")
		self.assertEqual(sphere, "sphere")
