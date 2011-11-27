"""
Unit tests for the Haikw library

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

import unittest
import manipulation
    
class InitalizationSuite(unittest.TestCase):
    """ Test suite for initalization / setup mechanisms """

    TEST_EMPTY = "test_empty"
    TEST_FILE = "./test/config/config.yaml"
    TEST_PACKAGE = "test"
    TEST_SOURCE = '''%YAML 1.2
---
test:
    colors:
        red: "#ff1100"
        blue:
            red: 0
            blue: 255
            green: 11
    sizes:
        small:
            - 1.1
            - 1.2
            - 1.3
        medium:
            - 2.1
            - 2.2
            - 2.3
        large:
            - 3.1
            - 3.2
            - 3.3
    positions:
        origin:
            x: 0
            y: 0
            z: 0
            roll: 0
            pitch: 0
            yaw: 0
        offset:
            x: 1
            y: 2
            z: 3
            roll: 0.1
            pitch: 0.2
            yaw: 0.3
    prototypes:
        test_cube:
            descriptor: cube
            size: small
            color: red
        test_sphere:
            descriptor: sphere
            size: 
                - 0.5
                - 1.5
                - 2.5
            color:
                red: 0
                blue: 100
                green: 255
    manipulation:
        location: "./test/manipulation.py"
        class: "manipulation.TestManipulationStrategy"
    construction:
        location: "./test/construction.py"
        class: "construction.TestConstructionStrategy"
...'''
    
    def setUp(self):
        self.source_manager = manipulation.PackageManager("yaml", configuration=InitalizationSuite.TEST_SOURCE)
        self.file_manager = manipulation.PackageManager("yaml", configuration_file=InitalizationSuite.TEST_FILE)

    def invalid_package_manager_init(self):
        """ Tests handeling of an invalid initalization of a package manager """
        with self.assertRaises(ValueError):
            manipulation.PackageManager("yaml") # Need config file or config source

    def color_source(self):
        """ Test package manager color initalization by sources """

        # Test colors - Inclusion
        color_configs = self.source_manager.get_colors_config(InitalizationSuite.TEST_PACKAGE)
        self.assertIn("red", color_configs)
        self.assertIn("blue", color_configs)

        # Test colors - Red
        red_config = color_configs["red"]
        self.assertEqual(red_config, "#ff1100")

        # Test colors - Blue
        blue_config = color_configs["blue"]
        self.assertEqual(blue_config["red"], 0)
        self.assertEqual(blue_config["green"], 11)
        self.assertEqual(blue_config["blue"], 255)
    
    def size_source(self):
        """ Test package manager size initalization by sources """

        # Test inclusion
        size_configs = self.source_manager.get_sizes_config(InitalizationSuite.TEST_PACKAGE)
        self.assertIn("small", size_configs)
        self.assertIn("medium", size_configs)
        self.assertIn("large", size_configs)

        # Test sizes - small
        small = size_configs["small"]
        self.assertEqual(small[0], 1.1)
        self.assertEqual(small[1], 1.2)
        self.assertEqual(small[2], 1.3)

        # Test sizes - medium
        medium = size_configs["medium"]
        self.assertEqual(medium[0], 2.1)
        self.assertEqual(medium[1], 2.2)
        self.assertEqual(medium[2], 2.3)

        # Test sizes - large
        large = size_configs["large"]
        self.assertEqual(large[0], 3.1)
        self.assertEqual(large[1], 3.2)
        self.assertEqual(large[2], 3.3)
    
    def position_source(self):
        """ Test package manager position initalization by sources """

        # Test inclusion
        position_configs = self.source_manager.get_positions_config(InitalizationSuite.TEST_PACKAGE)
        self.assertIn("origin", position_configs)
        self.assertIn("offset", position_configs)

        # Test positions - origin
        origin = position_configs["origin"]
        self.assertEqual(origin["x"], 0)
        self.assertEqual(origin["y"], 0)
        self.assertEqual(origin["z"], 0)
        self.assertEqual(origin["roll"], 0)
        self.assertEqual(origin["pitch"], 0)
        self.assertEqual(origin["yaw"], 0)

        # Test positions - offset
        offset = position_configs["offset"]
        self.assertEqual(offset["x"], 1)
        self.assertEqual(offset["y"], 2)
        self.assertEqual(offset["z"], 3)
        self.assertEqual(offset["roll"], 0.1)
        self.assertEqual(offset["pitch"], 0.2)
        self.assertEqual(offset["yaw"], 0.3)
    
    def prototypes_source(self):
        """ Test package manager prototype initalization by sources """

        # Test inclusion
        prototypes_config = self.source_manager.get_prototypes_config(InitalizationSuite.TEST_PACKAGE)
        self.assertIn("test_cube", prototypes_config)
        self.assertIn("test_sphere", prototypes_config)

        # Test prototypes - test_cube
        test_cube = prototypes_config["test_cube"]
        self.assertEqual(test_cube["descriptor"], "cube")
        self.assertEqual(test_cube["size"], "small")
        self.assertEqual(test_cube["color"], "red")

        # Test prototypes - test_sphere
        test_sphere = prototypes_config["test_sphere"]
        self.assertEqual(test_sphere["descriptor"], "sphere")
        self.assertEqual(test_sphere["size"][0], 0.5)
        self.assertEqual(test_sphere["size"][1], 1.5)
        self.assertEqual(test_sphere["size"][2], 2.5)
        self.assertEqual(test_sphere["color"]["red"], 0)
        self.assertEqual(test_sphere["color"]["blue"], 100)
        self.assertEqual(test_sphere["color"]["green"], 255)
    
    def manipulation_source(self):
        """ Test package manipulation properties by sources """
        manipulation_source = self.source_manager.get_manipulation_source_file(InitalizationSuite.TEST_PACKAGE)
        self.assertEqual(manipulation_source, "./test/manipulation.py")

        manipulation_class = self.source_manager.get_manipulation_class_name(InitalizationSuite.TEST_PACKAGE)
        self.assertEqual(manipulation_class, "manipulation.TestManipulationStrategy")
    
    def construction_source(self):
        """ Test package construction properties by sources """
        manipulation_source = self.source_manager.get_construction_source_file(InitalizationSuite.TEST_PACKAGE)
        self.assertEqual(manipulation_source, "./test/construction.py")

        manipulation_class = self.source_manager.get_construction_class_name(InitalizationSuite.TEST_PACKAGE)
        self.assertEqual(manipulation_class, "construction.TestConstructionStrategy") 
    
        def color_file(self):
            """ Test package manager color initalization by files """

            # Test colors - Inclusion
            color_configs = self.file_manager.get_colors_config(InitalizationSuite.TEST_PACKAGE)
            self.assertIn("red", color_configs)
            self.assertIn("blue", color_configs)

            # Test colors - Red
            red_config = color_configs["red"]
            self.assertEqual(red_config["red"], 255)
            self.assertEqual(red_config["green"], 16)
            self.assertEqual(red_config["blue"], 0)

            # Test colors - Blue
            blue_config = color_configs["blue"]
            self.assertEqual(blue_config["red"], 0)
            self.assertEqual(blue_config["green"], 255)
            self.assertEqual(blue_config["blue"], 11)
    
    def size_file(self):
        """ Test package manager size initalization by sources """

        # Test inclusion
        size_configs = self.file_manager.get_sizes_config(InitalizationSuite.TEST_PACKAGE)
        self.assertIn("small", size_configs)
        self.assertIn("medium", size_configs)
        self.assertIn("large", size_configs)

        # Test sizes - small
        small = size_configs["small"]
        self.assertEqual(small[0], 1.1)
        self.assertEqual(small[1], 1.2)
        self.assertEqual(small[2], 1.3)

        # Test sizes - medium
        medium = size_configs["medium"]
        self.assertEqual(medium[0], 2.1)
        self.assertEqual(medium[1], 2.2)
        self.assertEqual(medium[2], 2.3)

        # Test sizes - large
        large = size_configs["large"]
        self.assertEqual(large[0], 3.1)
        self.assertEqual(large[1], 3.2)
        self.assertEqual(large[2], 3.3)
    
    def position_file(self):
        """ Test package manager position initalization by sources """

        # Test inclusion
        position_configs = self.file_manager.get_positions_config(InitalizationSuite.TEST_PACKAGE)
        self.assertIn("origin", position_configs)
        self.assertIn("offset", position_configs)

        # Test positions - origin
        origin = position_configs["origin"]
        self.assertEqual(origin["x"], 0)
        self.assertEqual(origin["y"], 0)
        self.assertEqual(origin["z"], 0)
        self.assertEqual(origin["roll"], 0)
        self.assertEqual(origin["pitch"], 0)
        self.assertEqual(origin["yaw"], 0)

        # Test positions - offset
        offset = position_configs["offset"]
        self.assertEqual(offset["x"], 1)
        self.assertEqual(offset["y"], 2)
        self.assertEqual(offset["z"], 3)
        self.assertEqual(offset["roll"], 0.1)
        self.assertEqual(offset["pitch"], 0.2)
        self.assertEqual(offset["yaw"], 0.3)
    
    def prototypes_file(self):
        """ Test package manager prototype initalization by sources """

        # Test inclusion
        prototypes_config = self.file_manager.get_prototypes_config(InitalizationSuite.TEST_PACKAGE)
        self.assertIn("test_cube", prototypes_config)
        self.assertIn("test_sphere", prototypes_config)

        # Test prototypes - test_cube
        test_cube = prototypes_config["test_cube"]
        self.assertEqual(test_cube["descriptor"], "cube")
        self.assertEqual(test_cube["size"], "small")
        self.assertEqual(test_cube["color"], "red")

        # Test prototypes - test_sphere
        test_sphere = prototypes_config["test_sphere"]
        self.assertEqual(test_sphere["descriptor"], "sphere")
        self.assertEqual(test_sphere["size"][0], 0.5)
        self.assertEqual(test_sphere["size"][1], 1.5)
        self.assertEqual(test_sphere["size"][2], 2.5)
        self.assertEqual(test_sphere["color"]["red"], 0)
        self.assertEqual(test_sphere["color"]["blue"], 100)
        self.assertEqual(test_sphere["color"]["green"], 255)
    
    def manipulation_file(self):
        """ Test package manipulation properties by sources """
        manipulation_source = self.file_manager.get_manipulation_source_file(InitalizationSuite.TEST_PACKAGE)
        self.assertEqual(manipulation_source, "./test/manipulation.py")

        manipulation_class = self.file_manager.get_manipulation_class_name(InitalizationSuite.TEST_PACKAGE)
        self.assertEqual(manipulation_class, "manipulation.TestManipulationStrategy")
    
    def construction_file(self):
        """ Test package construction properties by sources """
        manipulation_source = self.file_manager.get_construction_source_file(InitalizationSuite.TEST_PACKAGE)
        self.assertEqual(manipulation_source, "./test/construction.py")

        manipulation_class = self.file_manager.get_construction_class_name(InitalizationSuite.TEST_PACKAGE)
        self.assertEqual(manipulation_class, "construction.TestConstructionStrategy") 
    
    def test_empty(self):
        """ Test that the package manager will report missing information """
        name = InitalizationSuite.TEST_EMPTY

        # Color information is provided
        self.file_manager.get_colors_config(name)

        # The rest is not
        fm = self.file_manager
        self.assertRaises(ValueError, fm.get_sizes_config, (fm, name))
        self.assertRaises(ValueError, fm.get_positions_config, (fm, name))
        self.assertRaises(ValueError, fm.get_prototypes_config, (fm, name))
        self.assertRaises(ValueError, fm.get_manipulation_class_name, (fm, name))
        self.assertRaises(ValueError, fm.get_manipulation_source_file, (fm, name))
        self.assertRaises(ValueError, fm.get_construction_class_name, (fm, name))
        self.assertRaises(ValueError, fm.get_construction_source_file, (fm, name))