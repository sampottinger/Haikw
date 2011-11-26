"""
Unit tests for virtual object mechanisms

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

import unittest
import virtualobject
import state
	
class VirtualObjectSuite(unittest.TestCase):
	""" Test suite for initalization / setup mechanisms """

	def simple_virtual_object_test(self):
		""" Tests the simple VirtualObject structures """

		# Create name
		test_name = "test name"

		# Create position
		test_position_x = 1
		test_position_y = 2
		test_position_z = 3
		test_position_roll = 0.1
		test_position_pitch = 0.2
		test_position_yaw = 0.3
		test_position = state.VirtualObjectPosition(test_position_x, test_position_y, test_position_z, test_position_roll, test_position_pitch, test_position_yaw)

		# Create descriptor
		test_descriptor = "test descriptor"

		# Create color
		test_color_r = 1
		test_color_g = 2
		test_color_b = 3
		test_color = virtualobject.VirtualObjectColor(test_color_r, test_color_g, test_color_b)

		# Create sizes
		test_sizes = [2, 3, 4]
		test_size = virtualobject.VirtualObjectSize(test_sizes)

		# Create virtual object
		virtual_object = virtualobject.VirtualObject(test_name, test_position, test_descriptor, test_color, test_size)

		# Test validity of name
		self.assertEqual(virtual_object.get_name(), test_name)

		# Test validity of position
		position = virtual_object.get_position()
		self.assertEqual(position.get_x(), test_position_x)
		self.assertEqual(position.get_y(), test_position_y)
		self.assertEqual(position.get_z(), test_position_z)
		self.assertEqual(position.get_roll(), test_position_roll)
		self.assertEqual(position.get_pitch(), test_position_pitch)
		self.assertEqual(position.get_yaw(), test_position_yaw)

		# Test validity of color
		color = virtual_object.get_color()
		self.assertEqual(color.get_red(), test_color_r)
		self.assertEqual(color.get_green(), test_color_g)
		self.assertEqual(color.get_blue(), test_color_b)

		# Test validity of size
		size = virtual_object.get_size()
		self.assertEqual(size[0], test_sizes[0])
		self.assertEqual(size[1], test_sizes[1])
		self.assertEqual(size[2], test_sizes[2])
	
	def invalid_color_test(self):
		""" Check invalid initalization """
		with self.assertRaises(ValueError):
			virtualobject.VirtualObjectColor(-1, 0, 0)
		
		with self.assertRaises(ValueError):
			virtualobject.VirtualObjectColor(0, -1, 0)

		with self.assertRaises(ValueError):
			virtualobject.VirtualObjectColor(0, 0, -1)
		
		with self.assertRaises(ValueError):
			virtualobject.VirtualObjectColor(256, 0, 0)
		
		with self.assertRaises(ValueError):
			virtualobject.VirtualObjectColor(0, 256, 0)
		
		with self.assertRaises(ValueError):
			virtualobject.VirtualObjectColor(0, 0, 256)

	def color_test(self):
		""" Test ComplexColorResolutionStrategy """

		test_strategy = virtualobject.ComplexColorResolutionStrategy()

		# Add prefabricated colors
		test_color_r_1 = 1
		test_color_g_1 = 2
		test_color_b_1 = 3
		test_color_1 = virtualobject.VirtualObjectColor(test_color_r_1, test_color_g_1, test_color_b_1)
		test_strategy.add_color("test_color_1", test_color_1)

		test_color_r_2 = 4
		test_color_g_2 = 5
		test_color_b_2 = 6
		test_color_2 = virtualobject.VirtualObjectColor(test_color_r_2, test_color_g_2, test_color_b_2)
		test_strategy.add_color("test_color_2", test_color_2)

		# Test as dictionary
		color_dict = {"red": 10, "blue": 21, "green": 32}
		test_color_dict = test_strategy.get_color(color_dict)
		self.assertEqual(color_dict["red"], test_color_dict.get_red())
		self.assertEqual(color_dict["blue"], test_color_dict.get_blue())
		self.assertEqual(color_dict["green"], test_color_dict.get_green())

		# Test as hex
		test_color_hex = test_strategy.get_color("#0011A2")
		self.assertEqual(test_color_hex.get_red(), 0)
		self.assertEqual(test_color_hex.get_green(), 17)
		self.assertEqual(test_color_hex.get_blue(), 162)

		# Test as prefabricated
		prefab_test_color_1 = test_strategy.get_color("test_color_1")
		self.assertEqual(prefab_test_color_1.get_red(), test_color_r_1)
		self.assertEqual(prefab_test_color_1.get_green(), test_color_g_1)
		self.assertEqual(prefab_test_color_1.get_blue(), test_color_b_1)

		prefab_test_color_2 = test_strategy.get_color("test_color_2")
		self.assertEqual(prefab_test_color_2.get_red(), test_color_r_2)
		self.assertEqual(prefab_test_color_2.get_green(), test_color_g_2)
		self.assertEqual(prefab_test_color_2.get_blue(), test_color_b_2)

		# Test catching unknown
		ts = test_strategy
		self.assertRaises(ValueError, ts.get_color, (ts, 1))
		self.assertRaises(ValueError, ts.get_color, (ts, "345678"))
	
	def size_test(self):
		""" Test size resolver """

		resolver = virtualobject.ComplexNamedSizeResolver()

		# Create test sizes
		test_small = virtualobject.VirtualObjectSize([1, 2, 3])
		test_medium = virtualobject.VirtualObjectSize([4, 5, 6])
		test_large = virtualobject.VirtualObjectSize([4, 5, 6])

		# Add to resolver
		resolver.add_size("small", test_small)
		resolver.add_size("medium", test_medium)
		resolver.add_size("large", test_large)

		# Test named sizes
		extracted_small = resolver.get_size("small")
		self.assertEqual(extracted_small[0], test_small[0])
		self.assertEqual(extracted_small[1], test_small[1])
		self.assertEqual(extracted_small[2], test_small[2])

		extracted_medium = resolver.get_size("medium")
		self.assertEqual(extracted_medium[0], test_medium[0])
		self.assertEqual(extracted_medium[1], test_medium[1])
		self.assertEqual(extracted_medium[2], test_medium[2])

		extracted_large = resolver.get_size("large")
		self.assertEqual(extracted_large[0], test_large[0])
		self.assertEqual(extracted_large[1], test_large[1])
		self.assertEqual(extracted_large[2], test_large[2])

		# Test creation by float list
		test_huge = resolver.get_size([7, 8, 9])
		self.assertEqual(test_huge[0], 7)
		self.assertEqual(test_huge[1], 8)
		self.assertEqual(test_huge[2], 9)

		# Test invalid initalization
		self.assertRaises(KeyError, resolver.get_size, "345678")
		self.assertRaises(ValueError, resolver.get_size, 345678)
	
	def object_resolution_test(self):
		""" Test mapped object resolution """

		# Create resolver
		resolver = virtualobject.MappedObjectResolver()

		# Create test prototypes
		test_small = virtualobject.VirtualObjectSize([1, 2, 3])
		test_red = virtualobject.VirtualObjectColor(255, 0, 0)
		test_cube = "cube"
		proto_small_red_cube = virtualobject.ObjectResolverFlyweight(test_red, test_small, test_cube)

		test_large = virtualobject.VirtualObjectSize([4, 5, 6])
		test_green = virtualobject.VirtualObjectColor(0, 255, 0)
		test_sphere = "sphere"
		proto_large_green_sphere = virtualobject.ObjectResolverFlyweight(test_green, test_large, test_sphere)

		# Add prototypes
		resolver.add_object("small_red_cube", proto_small_red_cube)
		resolver.add_object("large_green_sphere", proto_large_green_sphere)

		# Test prototypes
		small = resolver.get_size("small_red_cube")
		self.assertEqual(small[0], test_small[0])
		self.assertEqual(small[1], test_small[1])
		self.assertEqual(small[2], test_small[2])

		red = resolver.get_color("small_red_cube")
		self.assertEqual(red.get_red(), test_red.get_red())
		self.assertEqual(red.get_green(), test_red.get_green())
		self.assertEqual(red.get_blue(), test_red.get_blue())

		cube = resolver.get_descriptor("small_red_cube")
		self.assertEqual(cube, test_cube)

		large = resolver.get_size("large_green_sphere")
		self.assertEqual(large[0], test_large[0])
		self.assertEqual(large[1], test_large[1])
		self.assertEqual(large[2], test_large[2])

		green = resolver.get_color("large_green_sphere")
		self.assertEqual(green.get_red(), test_green.get_red())
		self.assertEqual(green.get_green(), test_green.get_green())
		self.assertEqual(green.get_blue(), test_green.get_blue())

		sphere = resolver.get_descriptor("large_green_sphere")
		self.assertEqual(sphere, test_sphere)

		# Test unregistered
		r = resolver
		self.assertRaises(KeyError, r.get_size, (r, "xyz"))
		self.assertRaises(KeyError, r.get_color, (r, "xyz"))
		self.assertRaises(KeyError, r.get_descriptor, (r, "xyz"))

	# NOTE: Builder not tested here
