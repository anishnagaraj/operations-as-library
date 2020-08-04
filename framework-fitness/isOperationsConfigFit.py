""" Framework Fitness Functions

This library is built on the basis of a configuration file called operations.yaml file present in the
root of this project. This class has a list of fitnessness functions that should be executed whenver a build happens
on the pipeline. Basically these functions test how fit is your operations.yaml file. Basic checks that these
function makes are as follows,

* Is operations.yaml file present?
* At any point does the operations.yaml file has the correct number of operations supported?
* Checks if all operations supported are present in operations.yaml file
* Checks if any newly introduced operation has been incoporated in this fitness functions
* Checks if there are any duplication in operations
* Checks if the operations.yaml file strictly follows the allowed schema

"""

# ============================================================================
# Require at least this (major, minor) Python runtime version:
PY_REQUIRED_VERSION = (3, 6)


# ============================================================================
# Main contact responsible for handling the archiving process
CONTACT="khanh-vinh.duong-luu@eon.com"
MAIL_FROM="no-reply@mail.eon-cds.de"


# ============================================================================
# Import base libraries
try:
  import sys
  sys.path.append('../')

  import unittest
  from utils.ConfigReader import OperationsReader as operationsReader
  from strictyaml import load, exceptions, DuplicateKeysDisallowed, MapPattern, Map, Str, Int, Seq, YAMLError
  from path import Path

except ImportError as e:
  print ("ERROR: Couldn't import required Python module: {0}".format (e))
  sys.exit (70)


# ============================================================================
# Check if running under a minimum supported Python runtime
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


class FitnessFunctions(unittest.TestCase):

    def setUp(self):
        self.operations = operationsReader.configFileReader("../operations.yaml")
        self.config_operations = list(self.operations.keys())

        self.supported_operations_file = operationsReader.configFileReader("supported_operations.yaml")
        self.defined_operations = self.supported_operations_file['supported_operations']
        self.total_supported_operations = self.supported_operations_file['supported_operations_count']


    def tearDown(self):
        pass

    def test_does_operations_config_file_exist(self):
        self.assertTrue(any(self.operations))

    def test_check_number_of_supported_operations(self):
        self.assertEqual(len(self.operations),self.total_supported_operations, f"The operations defined in operations.yaml file are { len(self.operations) } and the total number the fitness function known(from supported_operations.json) are { self.total_supported_operations }")

    def test_check_if_all_operations_exist_in_config(self):
        operations_missing_in_config = list(set(self.defined_operations) - set(self.config_operations))
        self.assertEqual(len(operations_missing_in_config),0, f"These are the operations that are missing from the operations.yaml file { operations_missing_in_config }")

    def test_check_if_all_operations_are_defined(self):
        operations_missing_from_defined_list = list(set(self.config_operations) - set(self.defined_operations))
        self.assertEqual(len(operations_missing_from_defined_list),0, f"Looks like these operations { operations_missing_from_defined_list } are being introduced. Plese define them!")

    def test_if_any_duplicate_operations(self):
        try:
            config = load(Path("../operations.yaml").bytes().decode('utf8'))
        except DuplicateKeysDisallowed:
            self.fail("Duplicate keys Found!")

    def test_operations_yaml_schema(self):
        try:
            load(Path("../operations.yaml").bytes().decode('utf8'), MapPattern(Str(), Map({"command": Str(), "tags": Str()})))
        except YAMLError as error:
            self.fail("Something wrong with your schema")

if __name__ == '__main__':
    unittest.main()
