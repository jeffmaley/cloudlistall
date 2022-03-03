"""This program will list the EC2 instances in an Organization or OU
"""

import sys
import traceback
import json
import logging
import boto3
import argparse


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

def get_ec2_instances(session):
    ec2 = session.client('ec2')
    response = ec2.describe_instances()
    ec2_instances = []
    for reservation in response['Reservations']:
        ec2_instances.append(reservation)
    token = ''
    try:
        token = response['NextToken']
    except KeyError:
        logger.info('No more instances')
    while token != '':
        response = ec2.describe_instances(
                    NextToken=token
        )
        for reservation in response['Reservations']:
            ec2_instances.append(reservation)
    return ec2_instances


def get_aws_session(access_key_id='', secret_access_key='', session_token='', profile_name=''):
    """Get AWS session with provided creds"""
    session = ''
    try:
        if profile_name:
            print(f'getting session with profile {profile_name}')
            session = boto3.session.Session(
                        profile_name=profile_name)
        else:
            session = boto3.session.Session()            
    except Exception as excp: # pylint: disable=broad-except
        exception_type, exception_value, exception_traceback = sys.exc_info()
        logger_(exception_type, exception_value, exception_traceback, excp)
    print(session)
    return session

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='List cloud resources')
    parser.add_argument('--aws-profile', type=str, dest='aws_profile', help='Name of an AWS profile to use')
    args = parser.parse_args()
    session = get_aws_session(profile_name=args.aws_profile)
    regions = get_regions(session)
    try:
        print('Program starting')
        print(regions)
    except Exception as excp: # pylint: disable=broad-except
        exception_type, exception_value, exception_traceback = sys.exc_info()
        logger_(exception_type, exception_value, exception_traceback, excp)



if __name__ == "__main__":
    main()
