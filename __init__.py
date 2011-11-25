"""
Haikw: helpful ARI inverse kinematics wrapper, a carefully crafted software package that will make your robotics research easier

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""

def get_facade_factory(self, location):
	""" Convenience function to create a facade factory """

	return ObjectManipulationFactory(location)