import re
from utils.ConfigReader import OperationsReader as operationsReader
from os import environ

class OperationsValidator:
    current_operation = ''
    operations = []

    def __init__(self, operation):
     self.current_operation = operation
     self.operations = operationsReader.configFileReader("./operations.yaml")

    def isSupportedOperation(self):
        operations = self.operations.keys()
        return self.current_operation in operations

    def getMisisingEnvVars(self):
        missing_params = []
        cli_command = self.operations[self.current_operation]['command']
        parameters = re.findall("\${(.*?)}", cli_command)
        for param in parameters:
            if environ.get(param) is None:
                missing_params.append(param)
        if len(missing_params) > 0:
            print(f"The operation attempted is: { self.current_operation }")
            print(f"The respective cli command is: { cli_command }")
        return missing_params
