import boto3
import collections
from datetime import datetime
import time
import sys
from dateutil import parser

def lambda_handler(event, context):

#0. Query for array of images (first loop AMIs) (second loop ec2s) 
#1. Validate based on a date (60 days) -> deregister anything older than 60 days 
#2. But make sure if that AMI is used by ec2 instance , so it needs to look up is that AMIs in use ? and if it's not in use, delete them

#1. Create list [] of AMIs used by ec2 = ami_used_by_ec2
#2. Create list [] of AMIs older than 60 days = old_ami_to_delete
#3. Loop through "old_ami_to_delete" list and deregister if not in "ami_used_by_ec2" var list
################
#SPECIFY A DATE#
################
    date = 0
##########
#SNS PART#
##########

    number_of_deleted_amis = 0
    old_ami_to_delete = []
    ami_used_by_ec2 = []

####################
#QUERY FOR ALL AMIs# 
####################
    client = boto3.client('ec2', 'us-west-2') 
    ec2 = boto3.resource('ec2', 'us-west-2')
    response = client.describe_images(Owners=["self"]) 
    Myec2=client.describe_instances()
    
 
     
    for image in response['Images']:
        
        creationdate = image['CreationDate']                  
        yourdate = parser.parse(creationdate)                 
        today = datetime.now()
        diff = (today - yourdate.replace(tzinfo=None)).days
        
        if diff >= date: 
        
            amiid = image['ImageId']  
#        print("AMI in account: ", amiid)
        
#        print("AMI_under_AMIs: ", amiid)
            old_ami_to_delete.append(amiid)
#        print("old_ami_to_delete:", old_ami_to_delete)
        else:
            print("NO AMIs created older than that date")
            break 
            
    for all_ec2s in Myec2['Reservations']:
            
        for every_single_ec2 in all_ec2s['Instances']:
#           print("AMIs_USED_BY_EC2: ", every_single_ec2['ImageId'])
            ami_used_by_ec2.append(every_single_ec2['ImageId'])
#            print("ami_used_by_ec2: ", ami_used_by_ec2)
    
    print("old_ami_to_delete:", old_ami_to_delete)
    print("ami_used_by_ec2: ", ami_used_by_ec2)


    
#    if diff >= date:
    for every_ami in old_ami_to_delete:
        if every_ami in ami_used_by_ec2:
            print("that ami", every_ami, "is used by ec2, so it cannot be deregistered")
        else:
            print("that", every_ami, "is not being used by any ec2s, so it can be deregistered")
            amideletion = client.deregister_image(DryRun=False,ImageId=every_ami,)
            print("Deleted the amis %a" % amideletion)                
            number_of_deleted_amis = number_of_deleted_amis + 1


    print("The_following_unused_and_old_AMIs_have_been_successfully_deregistered: ", number_of_deleted_amis)   
    
    if number_of_deleted_amis > 0:
        
        client = boto3.client('sns')
        snsArn = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'
        message = f"Hello Cloud-SRE-team, the usual housekeeping of AMIs is performed and {date} days old {number_of_deleted_amis} AMIs are successfully deregistered, happy devopsing everyone!"
        response = client.publish(
            TopicArn = snsArn,
            Message = message ,
            Subject='housekeeping-of-amis-in-us-west-2'
        )
