""" Driver for unit testing """
import unittest
from test import initalization
from test import virtualstructtest
from test import configtests
from test import loadertests
from test import midleveltests
from test import topleveltests

full_suite = unittest.TestSuite()

loader_suite = unittest.TestSuite()
loader_suite.addTest(loadertests.LoaderTests("test_yaml_file"))
loader_suite.addTest(loadertests.LoaderTests("test_yaml_string"))
full_suite.addTest(loader_suite)

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

midlevel_suite = unittest.TestSuite()
midlevel_suite.addTest(midleveltests.MidlevelTests("test_object_resolver_color"))
midlevel_suite.addTest(midleveltests.MidlevelTests("test_object_resolver_size"))
midlevel_suite.addTest(midleveltests.MidlevelTests("test_object_resolver_descriptor"))
midlevel_suite.addTest(midleveltests.MidlevelTests("test_built_color"))
midlevel_suite.addTest(midleveltests.MidlevelTests("test_built_position"))
midlevel_suite.addTest(midleveltests.MidlevelTests("test_built_descriptor"))
full_suite.addTest(midlevel_suite)

toplevel_suite = unittest.TestSuite()
toplevel_suite.addTest(topleveltests.ToplevelTests("test_external_builder_prototype_position"))
toplevel_suite.addTest(topleveltests.ToplevelTests("test_external_builder_prototype_color"))
toplevel_suite.addTest(topleveltests.ToplevelTests("test_external_builder_prototype_position"))
toplevel_suite.addTest(topleveltests.ToplevelTests("test_facade_access"))
toplevel_suite.addTest(topleveltests.ToplevelTests("test_facade_builder"))
toplevel_suite.addTest(topleveltests.ToplevelTests("test_facade_update"))
toplevel_suite.addTest(topleveltests.ToplevelTests("test_facade_grab"))
toplevel_suite.addTest(topleveltests.ToplevelTests("test_facade_face_position"))
toplevel_suite.addTest(topleveltests.ToplevelTests("test_facade_face_object"))
toplevel_suite.addTest(topleveltests.ToplevelTests("test_facade_face_prefab_position"))
toplevel_suite.addTest(topleveltests.ToplevelTests("test_facade_face_registered_object"))
toplevel_suite.addTest(topleveltests.ToplevelTests("test_facade_put"))
full_suite.addTest(toplevel_suite)

unittest.TextTestRunner().run(full_suite)
