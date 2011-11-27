"""
Unit tests for configuration mechanisms after file loading, creating objects for the rest of the system

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

import unittest
import configurable
	
class ConfigTests(unittest.TestCase):
	""" Test suite for initalization of configuration driven objects """

	def setUp(self):
		""" Establishes common objects for testing """

		# Test data
		self.test_color_data = {"red":{"red":255, "blue":10, "green":0}, "blue":{"red":0, "blue":250, "green":11}}
		self.test_size_data = {"small": [1, 2, 3], "large": [4, 5, 6]}
		self.test_position_data = {"small_offset": {"x": 1, "y": 2, "z": 3}, "large_offset": {"x":4, "y":5, "z":6, "roll": 0.1, "pitch":0.2, "yaw": 0.3}}

		# Create sample strategy for color resolution
		self.color_res_factory = configurable.ComplexColorResolutionFactory.get_instance()
		self.color_res_strategy = self.color_res_factory.create_strategy(self.test_color_data)

		# Create sample named size resolver
		self.size_res_factory = configurable.ComplexNamedSizeResolverFactory.get_instance()
		self.size_res_strategy = self.size_res_factory.create_resolver(self.test_size_data)

		# Create position factory
		self.position_factory_constructor = configurable.VirtualObjectPositionFactoryConstructor.get_instance()
		self.position_factory = self.position_factory_constructor.create_factory(self.test_position_data)

		# Create sample object resolver
		# TODO: MappedObjectResolverFactory

	def test_color_resolution(self):
		""" Tests the creation of color resolution strategies """

		red = self.color_res_strategy.get_color("red")
		self.assertEqual(red.get_red(), self.test_color_data["red"]["red"])
		self.assertEqual(red.get_green(), self.test_color_data["red"]["green"])
		self.assertEqual(red.get_blue(), self.test_color_data["red"]["blue"])

		blue = self.color_res_strategy.get_color("blue")
		self.assertEqual(blue.get_red(), self.test_color_data["blue"]["red"])
		self.assertEqual(blue.get_green(), self.test_color_data["blue"]["green"])
		self.assertEqual(blue.get_blue(), self.test_color_data["blue"]["blue"])
	
	def test_named_size_resolution(self):
		""" Tests the creation of name resolution strategies """

		small = self.size_res_strategy.get_size("small")
		self.assertEqual(small[0], self.test_size_data["small"][0])
		self.assertEqual(small[1], self.test_size_data["small"][1])
		self.assertEqual(small[2], self.test_size_data["small"][2])

		large = self.size_res_strategy.get_size("large")
		self.assertEqual(large[0], self.test_size_data["large"][0])
		self.assertEqual(large[1], self.test_size_data["large"][1])
		self.assertEqual(large[2], self.test_size_data["large"][2])
	
	def test_position_factory(self):
		""" Tests the creation of object position factories """

		small_offset = self.position_factory.create_prefabricated("small_offset")
		self.assertEqual(small_offset.get_x(), self.test_position_data["small_offset"]["x"])
		self.assertEqual(small_offset.get_y(), self.test_position_data["small_offset"]["y"])
		self.assertEqual(small_offset.get_z(), self.test_position_data["small_offset"]["z"])
		self.assertEqual(small_offset.get_roll(), configurable.VirtualObjectPositionFactoryConstructor.DEFAULT_ROLL)
		self.assertEqual(small_offset.get_pitch(), configurable.VirtualObjectPositionFactoryConstructor.DEFAULT_PITCH)
		self.assertEqual(small_offset.get_yaw(), configurable.VirtualObjectPositionFactoryConstructor.DEFAULT_YAW)

		large_offset = self.position_factory.create_prefabricated("large_offset")
		self.assertEqual(large_offset.get_x(), self.test_position_data["large_offset"]["x"])
		self.assertEqual(large_offset.get_y(), self.test_position_data["large_offset"]["y"])
		self.assertEqual(large_offset.get_z(), self.test_position_data["large_offset"]["z"])
		self.assertEqual(large_offset.get_roll(), self.test_position_data["large_offset"]["roll"])
		self.assertEqual(large_offset.get_pitch(), self.test_position_data["large_offset"]["pitch"])
		self.assertEqual(large_offset.get_yaw(), self.test_position_data["large_offset"]["yaw"])
	
	# NOTE: Does not test mapped object resolver factory