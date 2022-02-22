"""This program will list the EC2 instances in an Organization or OU
"""

import sys
import traceback
import json
import logging
import boto3


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


def get_regions(session):
    """Get current list of active regions"""
    ec2 = session.client('ec2')
    response = ''
    try:
        response = ec2.describe_regions()
    except Exception as excp: # pylint: disable=broad-except
        exception_type, exception_value, exception_traceback = sys.exc_info()
        logger_(exception_type, exception_value, exception_traceback, excp)
    return response['Regions']

def get_ec2_instances(session, regions):
    """Get EC2 instance information across regions"""
    instance_data = ''
    return instance_data


def get_aws_session(access_key_id='', secret_access_key='', session_token='', profile_name=''):
    """Get AWS session with provided creds"""
    try:
        session = boto3.session.Session(
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    aws_session_token=session_token,
                    profile_name=profile_name)
    except Exception as excp: # pylint: disable=broad-except
        exception_type, exception_value, exception_traceback = sys.exc_info()
        logger_(exception_type, exception_value, exception_traceback, excp)
    return session

def main():
    """Main entry point"""
    regions = get_regions(session)
    try:
        print('Program starting')
    except Exception as excp: # pylint: disable=broad-except
        exception_type, exception_value, exception_traceback = sys.exc_info()
        logger_(exception_type, exception_value, exception_traceback, excp)



if __name__ == "__main__":
    main()
