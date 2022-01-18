#!/usr/bin/python3

#source code was taken from =>  https://github.com/mohit614/AWSome-Scripts

import boto3
from dateutil.parser import parse
import datetime
import re

def lambda_handler(event, context): 
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::123456789101112:role/lambda_admin",
        RoleSessionName="cross_acct_lambda"
    )
    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']
    
    client = boto3.client(
        'ec2',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
        
    )
    return "Hello from Lambda"


age = 0 #Default it is 7 days #you can change it

def days_old(date):
    get_date_obj = parse(date)
    date_obj = get_date_obj.replace(tzinfo=None)
    diff = datetime.datetime.now() - date_obj
    return diff.days

ec2 = boto3.client('ec2')
sts_client = boto3.client('sts')
response = sts_client.get_caller_identity()

print("\n\nScript running------------------>")
#print("The script is using following role permissions: " + str(response['Arn']));



amis = ec2.describe_images(Owners=['self'])

#another for loop that go through all aws accounts 

for ami in amis['Images']:
    ami_id = ami['ImageId']
    create_date = ami['CreationDate']
    snapshot_id = ami['BlockDeviceMappings'][0]['Ebs']['SnapshotId']

    day_old = days_old(create_date)
    # print( "AMI-ID: " + ami['ImageId'] + "\t\tCreation Date: "+ ami['CreationDate']+"\t\tDays old:"+ str(day_old) )
    if day_old >= age:
        print("Deleting below AMIs with corresponding snapshot : \n")
        print( "AMI-ID: " + ami['ImageId'] + "\t\tCreation Date: "+ ami['CreationDate']+"\t\tDays old:"+ str(day_old) + "Snapshot : " + snapshot_id)
        ec2.deregister_image(ImageId=ami_id)
        ec2.delete_snapshot(SnapshotId=snapshot_id) #deleting snapshot
