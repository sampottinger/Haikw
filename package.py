"""
Module containing classes related package management

@author: Sam Pottinger
@license: GNU General Public License v2
@copyright: 2011
@organization: Andrews Robotics Initiative at CU Boulder
"""
import os
import loaders

class PackageManager:
	"""
	Deals with varying inverse kinetmatics packages and their configuration files

	Configuration files should be in the form of
	---
	OpenRAVE:
	    colors: "./openrave_config/colors.yaml"
	    sizes: "./openrave_config/sizes.yaml"
	    positions: "./openrave_config/positions.yaml"
	    prototypes: "./openrave_config/prototypes.yaml
	    manipulation:
	        location: "./openrave/manipulation.py"
	        class: "manipulation.OpenRaveManipulationStrategy"
	    construction:
	        location: "./openrave/construction.py"
	        class: "construction.OpenRaveConstructionStrategy"
	...

	@note: Changes forward slashes to the seperator of the current platform
	"""

	COLOR_DESCRIPTOR = "colors"
	SIZE_DESCRIPTOR = "sizes"
	POSITIONS_DESCRIPTOR = "positions"
	MANIPULATION_DESCRIPTOR = "manipulation"
	CONSTRUCTION_DESCRIPTOR = "construction"
	LOCATION_DESCRIPTOR = "location"
	CLASS_DESCRIPTOR = "class"
	SETUP_DESCRIPTOR = "setups"
	ROBOT_DESCRIPTOR = "robots"
	PROTOTYPE_DESCRIPTOR = "prototypes"

	def __init__(self, language, configuration_file=None, configuration=None):
		"""
		Constructor for a PackageManager

		@param language: The name of the language the configuration file or string is written in
		@type language: String
		@keyword configuration_file: The location of the configuration file to read inverse kinematic package data from
		@type configuration_file: String
		@keyword configuration: Language encoded string containing configuration information
		@type configuration: String
		@note: Exactly one of the keywords must be specified
		"""

		# Check we are not over specified
		if configuration_file and configuration:
			raise ValueError("Only the configuration file or the configuration string should be specified")
		
		# Save language for later
		self.__language = language
		
		# Get a reader
		self.__reader = loaders.ConfigReaderFactory.get_instance().get_reader(language)

		# If we are using a file
		if configuration_file:

			self.__using_files = True

			# Get a path fixer
			fixer = loaders.PathFixer.get_instance()

			# Read data
			self.__data = self.__reader.load(fixer.fix(configuration_file))
		
		# If loading from strings
		elif configuration:

			self.__using_files = False

			# Read data
			self.__data = self.__reader.loads(configuration)

		# Need some more configuration
		else:
			raise ValueError("Please specify a configuration or configuration file")
	
	def get_supported_packages(self):
		"""
		Determines which packages this manger is tracking 

		@return: A listing of packages this manager provides support for
		@rtype: List of Strings
		"""
		return self.__data.keys()
	
	def get_colors_config(self, package_name):
		"""
		Provides the configuration defining colors attached to the given package

		@param package_name: The name of the package to look up the color configuration file for
		@type package_name: String
		@return: The colors configuration for the provided package name
		@rtype: Dict
		"""
		
		entry = self.__get_package_info(package_name)

		if not PackageManager.COLOR_DESCRIPTOR in entry:
			raise ValueError("This package does not provide color information")
		
		if self.__using_files:
			return self.__reader.load(entry[PackageManager.COLOR_DESCRIPTOR])
		
		else:
			return entry[PackageManager.COLOR_DESCRIPTOR]

	def get_sizes_config(self, package_name):
		"""
		Provides the configuration defining the named sizes attached to the given package

		@param package_name: The name of the package to look up the sizes configuration file for
		@type package_name: String
		@return: The sizes configuration for the provided package name
		@rtype: Dict
		"""
		
		entry = self.__get_package_info(package_name)

		if not PackageManager.SIZE_DESCRIPTOR in entry:
			raise ValueError("This package does not provide color information")
		
		if self.__using_files:
			return self.__reader.load(entry[PackageManager.SIZE_DESCRIPTOR])
		
		else:
			return entry[PackageManager.SIZE_DESCRIPTOR]

	def get_positions_config(self, package_name):
		"""
		Provides the configuration defining the named positions attached to the given package

		@param package_name: The name of the package to look up the named positions configuration file for
		@type package_name: String
		@return: The sizes configuration for the provided package name
		@rtype: Dict
		"""
		
		entry = self.__get_package_info(package_name)

		if not PackageManager.POSITIONS_DESCRIPTOR in entry:
			raise ValueError("This package does not provide position information")
		
		if self.__using_files:
			return self.__reader.load(entry[PackageManager.POSITIONS_DESCRIPTOR])
		
		else:
			return entry[PackageManager.POSITIONS_DESCRIPTOR]

	def get_manipulation_source_file(self, package_name):
		"""
		Determines the location of the source file for the manipulation strategy attached to the given package

		@param package_name: The name of the package to look up this source file for
		@type package_name: String
		@return: The location of the the manipulation strategy source
		@rtype: String
		"""
		
		entry = self.__get_package_info(package_name)

		if not PackageManager.MANIPULATION_DESCRIPTOR in entry:
			raise ValueError("This package does not provide manipulation information")
		
		return entry[PackageManager.MANIPULATION_DESCRIPTOR][PackageManager.LOCATION_DESCRIPTOR]
	
	def get_manipulation_class_name(self, package_name):
		"""
		Determines the name of the class to load as a manipulation strategy for this package

		@param package_name: The name of the package to look for a manipulation strategy class name to go with
		@type package_name: String
		@return: The module and class name for this manipulation strategy
		@rtype: String
		"""

		entry = self.__get_package_info(package_name)

		if not PackageManager.MANIPULATION_DESCRIPTOR in entry:
			raise ValueError("This package does not provide construction information")
		
		if not PackageManager.CLASS_DESCRIPTOR in entry[PackageManager.MANIPULATION_DESCRIPTOR]:
			raise ValueError("This package does not provide a class name to load")

		return entry[PackageManager.MANIPULATION_DESCRIPTOR][PackageManager.CLASS_DESCRIPTOR]
	
	def get_construction_source_file(self, package_name):
		"""
		Determines the location of the source file for the object construction strategy attached to the given package

		@param package_name: The name of the package to look up this source file for
		@type package_name: String
		@return: The location of the the construction strategy source
		@rtype: String
		"""
		
		entry = self.__get_package_info(package_name)

		if not PackageManager.CONSTRUCTION_DESCRIPTOR in entry:
			raise ValueError("This package does not provide construction information")

		return entry[PackageManager.CONSTRUCTION_DESCRIPTOR][PackageManager.LOCATION_DESCRIPTOR]
	
	def get_construction_class_name(self, package_name):
		"""
		Determines the name of the class to load as a manipulation strategy for this package

		@param package_name: The name of the package to look for a manipulation strategy class name to go with
		@type package_name: String
		@return: The module and class name for this construction strategy
		@rtype: String
		"""

		entry = self.__get_package_info(package_name)

		if not PackageManager.CONSTRUCTION_DESCRIPTOR in entry:
			raise ValueError("This package does not provide construction information")
		
		if not PackageManager.CLASS_DESCRIPTOR in entry[PackageManager.CONSTRUCTION_DESCRIPTOR]:
			raise ValueError("This package does not provide a class name to load")
		
		return entry[PackageManager.CONSTRUCTION_DESCRIPTOR][PackageManager.CLASS_DESCRIPTOR]

	def get_setup_config(self, package_name):
		"""
		Provides the configuration defining the named setups attached to the given package

		@param package_name: The name of the package to look up the named setup configuration file for
		@type package_name: String
		@return: The setup configurations for the provided package name
		@rtype: Dict
		"""
		entry = self.__get_package_info(package_name)

		if not PackageManager.SETUP_DESCRIPTOR in entry:
			raise ValueError("This package does not provide a location for a configuration file for named setups")
		
		if self.__using_files:
			return self.__reader.load(entry[PackageManager.SETUP_DESCRIPTOR], self.__language)
		
		else:
			return entry[PackageManager.SETUP_DESCRIPTOR]

	def get_robot_config(self, package_name):
		"""
		Provides the configuration defining the named robots attached to the given package

		@param package_name: The name of the package to look up the named robot configuration file for
		@type package_name: String
		@return: The robot configurations for the provided package name
		@rtype: Dict
		"""
		entry = self.__get_package_info(package_name)

		if not PackageManager.ROBOT_DESCRIPTOR in entry:
			raise ValueError("This package does not provide a location for a configuration file for robots")
		
		if self.__using_files:
			return self.__reader.load(entry[PackageManager.ROBOT_DESCRIPTOR], self.__language)
		
		else:
			return entry[PackageManager.ROBOT_DESCRIPTOR]
	
	def get_prototypes_config(self, package_name):
		"""
		Provides the configuration defining the named virtual object prototypes attached to the given package

		@param package_name: The name of the package to look up the named prototypes for
		@type package_name: String
		@return: The prototype configurations for the provided package name
		@rtype: Dict
		"""
		entry = self.__get_package_info(package_name)

		if not PackageManager.PROTOTYPE_DESCRIPTOR in entry:
			raise ValueError("This package does not provide a location for a configuration file for prototypes")
		
		if self.__using_files:
			return self.__reader.load(entry[PackageManager.PROTOTYPE_DESCRIPTOR])
		
		else:
			return entry[PackageManager.PROTOTYPE_DESCRIPTOR]

	def __get_package_info(self, package_name):
		if not package_name in self.__data:
			raise ValueError("The package name provided has not been given a specification")

		return self.__data[package_name]