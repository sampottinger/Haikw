"""
Unit tests for constructing facades

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""
import unittest
import manipulation
	
class FacadeConstructionTests(unittest.TestCase):
	""" Test suite for facade construction """

	def setUp(self):
		""" Provide common objects for testing construction """
		self.manager = manipulation.ObjectManipulationFactory("yaml", "./test/config/config.yaml")

		self.test_facade = self.manager.create_facade("test", "yaml")

		builder = self.test_facade.get_object_builder()
		builder.set_new_descriptor("cube")
		builder.set_new_color("blue")
		builder.set_new_size_by_name("small")
		self.small_blue_cube = builder.create("small_blue_cube", "origin")

		builder.set_new_descriptor("sphere")
		builder.set_new_color("red")
		builder.set_new_size_by_name("large")
		self.large_red_sphere = builder.create("large_red_sphere", "offset")

	def check_package_inclusion(self):
		""" Check packages loaded by facade factory """
		available_packages = self.manager.get_available_facade_types()
		self.assertIn("test", available_packages)
		self.assertIn("test_empty", available_packages)
	
	def check_builder_color(self):
		""" Check builder produced through factory by checking colors of its products """
		blue = self.small_blue_cube.get_color()
		self.assertEqual(blue.get_red(), 0)
		self.assertEqual(blue.get_green(), 11)
		self.assertEqual(blue.get_blue(), 255)

		red = self.large_red_sphere.get_color()
		self.assertEqual(red.get_red(), 255)
		self.assertEqual(red.get_green(), 17)
		self.assertEqual(red.get_blue(), 0)

	def check_builder_size(self):
		""" Check builder produced through factory by checking sizes of its products """

		small = self.small_blue_cube.get_size()
		self.assertEqual(small[0], 1.1)
		self.assertEqual(small[1], 1.2)
		self.assertEqual(small[2], 1.3)

		large = self.large_red_sphere.get_size()
		self.assertEqual(large[0], 3.1)
		self.assertEqual(large[1], 3.2)
		self.assertEqual(large[2], 3.3)
	
	def check_builder_descriptor(self):
		""" Check builder produced through factory by checking descriptors of its products """

		cube = self.small_blue_cube.get_descriptor()
		sphere = self.large_red_sphere.get_descriptor()

		self.assertEqual(cube, "cube")
		self.assertEqual(sphere, "sphere")
	
	def check_manipulation(self):
		""" Check that manipulation works """
		self.test_facade.face("offset")
		facing_position = self.test_facade.get_manipulation_strategy().facing
		self.assertEqual(facing_position.get_x(), 1)
		self.assertEqual(facing_position.get_y(), 2)
		self.assertEqual(facing_position.get_z(), 3)
		self.assertEqual(facing_position.get_roll(), 0.1)
		self.assertEqual(facing_position.get_pitch(), 0.2)
		self.assertEqual(facing_position.get_yaw(), 0.3)
