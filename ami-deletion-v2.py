import boto3
import collections
from datetime import datetime
import time
import sys
from dateutil import parser

#since the Lambda is a regional scoped resource, it needs to be created & configured in the specific aws region it aims to run against
def lambda_handler(event, context):
    
    #define your aws region where you got some AMIs 
    ec = boto3.client('ec2', 'us-east-1') 
    ec2 = boto3.resource('ec2', 'us-east-1')
    response = ec.describe_images(Owners=["self"])             #which means describe all the AMI images owned by me 
    
    #for every single AMI image it finds under AMIs under ec2
    for image in response['Images']:
     
        creationdate = image['CreationDate']                   #define & hold its created date under the following variable 
        amiid = image['ImageId']                               #define & hold its AMI ID under the following variable
        #print("We found this ami in the account %a" % amiid)  #display all the AMIs
        yourdate = parser.parse(creationdate)                  #parse its created date under the following variable 
        today = datetime.now()                                 #hold today's date under the following variable 
        
        diff = (today - yourdate.replace(tzinfo=None)).days    #make a math
        
        
        #if (diff >= 60) remove absolutely all the AMIs which are older than 60 days and keep all the AMIs before 60 days
        #if (diff =< 60) remove all the AMIs only up to 60 days and keep anything after
        if (diff >= 60 ):
            print(f"Below amis are older than 60 days {amiid}")
        
            #print("deregistering ami %s" % amiid)
            amideletion = ec.deregister_image(
                DryRun=False,
                ImageId=amiid,
            )
            print("Deleted the amis %a" % amideletion)
        else:
            print("No AMIs older than 60 days found")
