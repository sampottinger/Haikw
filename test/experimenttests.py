"""
Very simple unit tests for experiment structures, mostly here for future complexity

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

import unittest
import experiment
import state
import virtualobject
    
class ExperimentTests(unittest.TestCase):
    """ Tests configuration file loading code """

    def setUp(self):
        """ Establishes common objects for these tests """
        # Create some parts
        self.part_1 = experiment.RobotPart("test_part_1")
        self.part_2 = experiment.RobotPart("test_part_2")
        self.part_3 = experiment.RobotPart("test_part_3")

        # Create some robots
        self.robot_1 = experiment.Robot("test_robot_1", [self.part_1, self.part_2], "test_descriptor")
        self.robot_2 = experiment.Robot("test_robot_2", [self.part_3], "test_descriptor_2")

        # Create some colors
        red = virtualobject.VirtualObjectColor(255, 0, 0)
        green = virtualobject.VirtualObjectColor(0, 255, 0)

        # Create some sizes
        small = virtualobject.VirtualObjectSize([1, 1, 1])
        large = virtualobject.VirtualObjectSize([2, 2, 2])

        # Create some positions
        small_offset = state.VirtualObjectPosition(1, 1, 1, 0, 0, 0)
        large_offset = state.VirtualObjectPosition(2, 2, 2, 0, 0, 0)

        # Create some virtual objects
        self.test_obj_1 = virtualobject.VirtualObject("test_obj_1", small_offset, "cube", red, small)
        self.test_obj_2 = virtualobject.VirtualObject("test_obj_2", large_offset, "sphere", green, large)
        self.test_obj_3 = virtualobject.VirtualObject("test_obj_3", large_offset, "sphere", red, large)

        # Create some setups
        self.setup_1 = experiment.Setup("setup_1", [self.test_obj_1, self.test_obj_2])
        self.setup_2 = experiment.Setup("setup_2", [self.test_obj_3])

        # Create some setup managers
        self.setup_manager = experiment.SetupManager()
        self.setup_manager.add(self.setup_1)
        self.setup_manager.add(self.setup_2)

        # Create some robot managers
        self.robot_manager = experiment.RobotManager()
        self.robot_manager.add(self.robot_1)
        self.robot_manager.add(self.robot_2)

    def test_part(self):
        """ Test robot part """
        self.assertEqual(self.part_1.get_name(), "test_part_1")
    
    def test_robot(self):
        """ Tests non-abstract parts of a robot """

        self.assertEqual(self.robot_1.get_name(), "test_robot_1")
        parts = self.robot_1.get_parts()
        self.assertEqual(parts[0].get_name(), "test_part_1")
        self.assertEqual(parts[1].get_name(), "test_part_2")
    
    def test_setup(self):
        """ Test the creation and reading of a setup """
        self.assertEqual(self.setup_1.get_name(), "setup_1")
        objs = self.setup_1.get_objects()
        self.assertEqual(objs[0].get_name(), "test_obj_1")
        self.assertEqual(objs[1].get_name(), "test_obj_2")
    
    def test_setup_manager(self):
        """ Test the setup manager with the given set-ups """
        setup_1 = self.setup_manager.get("setup_1")
        self.assertEqual(setup_1.get_name(), "setup_1")
        setup_1_objs = setup_1.get_objects()
        self.assertEqual(setup_1_objs[0].get_name(), "test_obj_1")
        self.assertEqual(setup_1_objs[1].get_name(), "test_obj_2")
        
        setup_2 = self.setup_manager.get("setup_2")
        self.assertEqual(setup_2.get_name(), "setup_2")
        setup_2_objs = setup_2.get_objects()
        self.assertEqual(setup_2_objs[0].get_name(), "test_obj_3")
    
    def test_robot_manager(self):
        """ Test the robot manager with the given robots """
        robot_1 = self.robot_manager.get("test_robot_1")
        self.assertEqual(robot_1.get_name(), "test_robot_1")
        robot_2 = self.robot_manager.get("test_robot_2")
        self.assertEqual(robot_2.get_name(), "test_robot_2")
