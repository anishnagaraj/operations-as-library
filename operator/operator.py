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
  import argparse
  import sys
  from utils.Validator import OperationsValidator
  from utils.ConfigReader import OperationsReader as operationsReader

except ImportError as e:
  print ("ERROR: Couldn't import required Python module: {0}".format (e))
  sys.exit (70)


# ============================================================================
# Check if running under a minimum supported Python runtime
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


#setup argument parser with necessary commands
def setup_argument_parser():
    parser = argparse.ArgumentParser(description="Entrypoint for the aem-operation CD pipeline")
    parser.add_argument('--operation', type=str, help='Action which will be performed for this call', required=True)
    return vars(parser.parse_args())

def main():
    try:
        console_arguments = setup_argument_parser()
        operation = console_arguments['operation']
        operationsValidator = OperationsValidator(operation)

        isSupportedOperation = operationsValidator.isSupportedOperation()
        if not isSupportedOperation:
            raise Exception(f"{ operation } is not supported")

        missing_params = operationsValidator.getMisisingEnvVars()
        if(len(missing_params)>1):
            raise Exception(f" These params:{ missing_params } are not set")
        elif(len(missing_params)==1):
            raise Exception(f" This param:{ missing_params } is not set")


        operations = operationsReader.configFileReader("./operations.yaml")
        cmd = operations[operation]['command']
        return cmd
    except Exception as e:
        print(f" {e} ")
        sys.exit(10)


if __name__ == "__main__":
    print(main())
