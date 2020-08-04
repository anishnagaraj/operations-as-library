import os
import yaml
import json

class OperationsReader:
    def configFileReader(file_path):
        #define what type of file is provided
        if '.yaml' in file_path or '.yml' in file_path:
            with open(file_path, 'r') as configFile:
                #loaded provided file in depends on type to dictionary
                configFileDict = yaml.safe_load(configFile)
            return configFileDict
        #define what type of file is provided
        elif '.json' in file_path:
            with open(file_path, 'r') as configFile:
                #loaded provided file in depends on type to dictionary
                configFileDict = json.load(configFile)
            return configFileDict
        else:
            # if incorrect file type or file path - return error
            print("Config file error, wrong path or file type")
            return -1
