"""
Unit tests for configuration reading mechanisms

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

import unittest
import loaders
    
class LoaderTests(unittest.TestCase):
    """ Tests configuration file loading code """

    TEST_FILE_PATH = "./test/resources/test.yaml"
    TEST_SOURCE = """%YAML 1.2
---
test_3:
    property_5_str: value5
    property_6_int: 6
test_4:
    property_7_float: 1.618
    property_8_list:
        - list_2
        - 7
        - 1.23
..."""

    def test_yaml_file(self):
        """ Test reading from a sample yaml file """
        # Get dict
        reader_factory = loaders.ConfigReaderFactory.get_instance()
        yaml_reader = reader_factory.get_reader("yaml")
        test_dict = yaml_reader.load(LoaderTests.TEST_FILE_PATH)

        # Check property existance
        self.assertIn("test_1", test_dict)
        self.assertIn("test_2", test_dict)

        # Pull subtests
        test_1 = test_dict["test_1"]
        test_2 = test_dict["test_2"]

        # Check subtest property existance
        self.assertIn("property_1_str", test_1)
        self.assertIn("property_2_int", test_1)
        self.assertIn("property_3_float", test_2)
        self.assertIn("property_4_list", test_2)

        # Check subtest 1 property correctness
        self.assertEqual("value1", test_1["property_1_str"])
        self.assertEqual(2, test_1["property_2_int"])

        # Check subtest 2 simple property correctness
        self.assertEqual(3.14, test_2["property_3_float"])

        # Check subtest 2 list property correctness
        list_property = test_2["property_4_list"]
        self.assertEqual("list_1", list_property[0])
        self.assertEqual(2, list_property[1])
        self.assertEqual(2.718, list_property[2])
    
    def test_yaml_string(self):
        """ Test reading from a sample yaml formatted string """
        # Get dict
        reader_factory = loaders.ConfigReaderFactory.get_instance()
        yaml_reader = reader_factory.get_reader("yaml")
        test_dict = yaml_reader.loads(LoaderTests.TEST_SOURCE)

        # Check property existance
        self.assertIn("test_3", test_dict)
        self.assertIn("test_4", test_dict)

        # Pull subtests
        test_3 = test_dict["test_3"]
        test_4 = test_dict["test_4"]

        # Check subtest property existance
        self.assertIn("property_5_str", test_3)
        self.assertIn("property_6_int", test_3)
        self.assertIn("property_7_float", test_4)
        self.assertIn("property_8_list", test_4)

        # Check subtest 1 property correctness
        self.assertEqual("value5", test_3["property_5_str"])
        self.assertEqual(6, test_3["property_6_int"])

        # Check subtest 2 simple property correctness
        self.assertEqual(1.618, test_4["property_7_float"])

        # Check subtest 2 list property correctness
        list_property = test_4["property_8_list"]
        self.assertEqual("list_2", list_property[0])
        self.assertEqual(7, list_property[1])
        self.assertEqual(1.23, list_property[2])
