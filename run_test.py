""" Driver for unit testing """
import unittest
from test import initalization
from test import virtualstructtest
from test import configtests
from test import loadertests

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

config_suite = unittest.TestSuite()
config_suite.addTest(configtests.ConfigTests("test_color_resolution"))
config_suite.addTest(configtests.ConfigTests("test_named_size_resolution"))
config_suite.addTest(configtests.ConfigTests("test_position_factory"))
full_suite.addTest(config_suite)

loader_suite = unittest.TestSuite()
loader_suite.addTest(loadertests.LoaderTests("test_yaml_file"))
loader_suite.addTest(loadertests.LoaderTests("test_yaml_string"))
full_suite.addTest(loader_suite)

unittest.TextTestRunner(verbosity=2).run(full_suite)