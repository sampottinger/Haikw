""" Driver for unit testing """
import unittest
from test import initalization
from test import virtualstructtest

full_suite = unittest.TestSuite()

init_suite = unittest.TestSuite()
init_suite.addTest(initalization.InitalizationSuite("invalid_package_manager_init"))
init_suite.addTest(initalization.InitalizationSuite("color_source"))
init_suite.addTest(initalization.InitalizationSuite("size_source"))
init_suite.addTest(initalization.InitalizationSuite("position_source"))
init_suite.addTest(initalization.InitalizationSuite("prototypes_source"))
init_suite.addTest(initalization.InitalizationSuite("manipulation_source"))
init_suite.addTest(initalization.InitalizationSuite("construction_source"))
init_suite.addTest(initalization.InitalizationSuite("size_file"))
init_suite.addTest(initalization.InitalizationSuite("position_file"))
init_suite.addTest(initalization.InitalizationSuite("prototypes_file"))
init_suite.addTest(initalization.InitalizationSuite("manipulation_file"))
init_suite.addTest(initalization.InitalizationSuite("construction_file"))
init_suite.addTest(initalization.InitalizationSuite("test_empty"))
full_suite.addTest(init_suite)

virtual_object_suite = unittest.TestSuite()
virtual_object_suite.addTest(virtualstructtest.VirtualObjectSuite("simple_virtual_object_test"))
virtual_object_suite.addTest(virtualstructtest.VirtualObjectSuite("invalid_color_test"))
virtual_object_suite.addTest(virtualstructtest.VirtualObjectSuite("color_test"))
virtual_object_suite.addTest(virtualstructtest.VirtualObjectSuite("size_test"))
virtual_object_suite.addTest(virtualstructtest.VirtualObjectSuite("object_resolution_test"))
full_suite.addTest(virtual_object_suite)

unittest.TextTestRunner(verbosity=2).run(full_suite)