import sys
import traceback
import json
import logging
import boto3
import argparse
import aws


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def logger_(exception_type, exception_value, exception_traceback, excp): #pylint: disable=unused-argument
    """Simple logger"""
    traceback_string = traceback.format_exception(
                        exception_type,
                        exception_value,
                        exception_traceback
                        )
    err_msg = json.dumps({
        "errorType": exception_type.__name__,
        "errorMessage": str(exception_value),
        "stackTrace": traceback_string
    })
    logger.error(err_msg)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='List cloud resources')
    parser.add_argument('--aws-profile', type=str, dest='aws_profile', help='Name of an AWS profile to use')
    args = parser.parse_args()
    session = aws.get_aws_session(profile_name=args.aws_profile)
    regions = aws.get_regions(session)
    instances = aws.get_ec2_instances(session)
    try:
        print('Program starting')
        print(regions)
        print(instances)
    except Exception as excp: # pylint: disable=broad-except
        exception_type, exception_value, exception_traceback = sys.exc_info()
        logger_(exception_type, exception_value, exception_traceback, excp)
    return

if __name__ == "__main__":
    main()