import boto3
import collections
from datetime import datetime
import time
import sys
from dateutil import parser

def lambda_handler(event, context):
    
    client = boto3.client('sns')
    snsArn = ''
    message = "Hello Cloud-DevOps-team, the usual housekeeping of AMIs are performed and 60 days old AMIs are successfully deregistered, happy devopsing everyone!"
    response = client.publish(
        TopicArn = snsArn,
        Message = message ,
        Subject='housekeeping-of-amis-in-us-west-2'
    )

    client = boto3.client('ec2', 'us-west-2') 
    ec2 = boto3.resource('ec2', 'us-west-2')
    response = client.describe_images(Owners=["self"])             
    
    for image in response['Images']:
        print(image)
#{'Architecture': 'x86_64', 'CreationDate': '2022-03-04T22:25:05.000Z', 'ImageId': 'ami-03510faea73bda9f8', 'ImageLocation': '326014234008/image-from-ec2', 'ImageType': 'machine', 'Public': False, 'OwnerId': '326014234008', 'PlatformDetails': 'Linux/UNIX', 'UsageOperation': 'RunInstances', 'ProductCodes': [{'ProductCodeId': 'aw0evgkw8e5c1q413zgy5pjce', 'ProductCodeType': 'marketplace'}], 'State': 'available', 'BlockDeviceMappings': [{'DeviceName': '/dev/sda1', 'Ebs': {'DeleteOnTermination': False, 'SnapshotId': 'snap-070fcd82a580b869a', 'VolumeSize': 8, 'VolumeType': 'gp2', 'Encrypted': False}}], 'Description': '[Copied ami-011e88cdebaf4409e from us-east-1] image-from-ec2', 'EnaSupport': True, 'Hypervisor': 'xen', 'Name': 'image-from-ec2', 'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs', 'SriovNetSupport': 'simple', 'VirtualizationType': 'hvm'}
#{'Architecture': 'x86_64', 'CreationDate': '2022-03-04T22:20:52.000Z', 'ImageId': 'ami-0bf3322fe88fc4614', 'ImageLocation': '326014234008/image-from-ec2', 'ImageType': 'machine', 'Public': False, 'OwnerId': '326014234008', 'PlatformDetails': 'Linux/UNIX', 'UsageOperation': 'RunInstances', 'ProductCodes': [{'ProductCodeId': 'aw0evgkw8e5c1q413zgy5pjce', 'ProductCodeType': 'marketplace'}], 'State': 'available', 'BlockDeviceMappings': [{'DeviceName': '/dev/sda1', 'Ebs': {'DeleteOnTermination': False, 'SnapshotId': 'snap-0ee1146230bc0ce47', 'VolumeSize': 8, 'VolumeType': 'gp2', 'Encrypted': False}}], 'Description': '[Copied ami-011e88cdebaf4409e from us-east-1] image-from-ec2', 'EnaSupport': True, 'Hypervisor': 'xen', 'Name': 'image-from-ec2', 'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs', 'SriovNetSupport': 'simple', 'Tags': [{'Key': 'environment', 'Value': 'production'}], 'VirtualizationType': 'hvm'}
        for tag in image['Tags']:
            print("OUTPUT: ", tag)
#Function Logs
#START RequestId: 269caac3-96fb-466d-951e-e3639bf2854d Version: $LATEST
#{'Architecture': 'x86_64', 'CreationDate': '2022-03-04T22:25:05.000Z', 'ImageId': 'ami-03510faea73bda9f8', 'ImageLocation': '326014234008/image-from-ec2', 'ImageType': 'machine', 'Public': False, 'OwnerId': '326014234008', 'PlatformDetails': 'Linux/UNIX', 'UsageOperation': 'RunInstances', 'ProductCodes': [{'ProductCodeId': 'aw0evgkw8e5c1q413zgy5pjce', 'ProductCodeType': 'marketplace'}], 'State': 'available', 'BlockDeviceMappings': [{'DeviceName': '/dev/sda1', 'Ebs': {'DeleteOnTermination': False, 'SnapshotId': 'snap-070fcd82a580b869a', 'VolumeSize': 8, 'VolumeType': 'gp2', 'Encrypted': False}}], 'Description': '[Copied ami-011e88cdebaf4409e from us-east-1] image-from-ec2', 'EnaSupport': True, 'Hypervisor': 'xen', 'Name': 'image-from-ec2', 'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs', 'SriovNetSupport': 'simple', 'Tags': [{'Key': 'environment', 'Value': 'production'}], 'VirtualizationType': 'hvm'}
#OUTPUT:  {'Key': 'environment', 'Value': 'production'}
#{'Architecture': 'x86_64', 'CreationDate': '2022-03-04T22:20:52.000Z', 'ImageId': 'ami-0bf3322fe88fc4614', 'ImageLocation': '326014234008/image-from-ec2', 'ImageType': 'machine', 'Public': False, 'OwnerId': '326014234008', 'PlatformDetails': 'Linux/UNIX', 'UsageOperation': 'RunInstances', 'ProductCodes': [{'ProductCodeId': 'aw0evgkw8e5c1q413zgy5pjce', 'ProductCodeType': 'marketplace'}], 'State': 'available', 'BlockDeviceMappings': [{'DeviceName': '/dev/sda1', 'Ebs': {'DeleteOnTermination': False, 'SnapshotId': 'snap-0ee1146230bc0ce47', 'VolumeSize': 8, 'VolumeType': 'gp2', 'Encrypted': False}}], 'Description': '[Copied ami-011e88cdebaf4409e from us-east-1] image-from-ec2', 'EnaSupport': True, 'Hypervisor': 'xen', 'Name': 'image-from-ec2', 'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs', 'SriovNetSupport': 'simple', 'Tags': [{'Key': 'environment', 'Value': 'production'}], 'VirtualizationType': 'hvm'}
#OUTPUT:  {'Key': 'environment', 'Value': 'production'}
            if tag["Key"] == "environment" and tag["Value"] == "production":
                continue
            else:
#                print("dev")
#            print("The End")
                creationdate = image['CreationDate']                  
                amiid = image['ImageId']                              
                yourdate = parser.parse(creationdate)                 
                today = datetime.now()                                
        
                diff = (today - yourdate.replace(tzinfo=None)).days 
        
                if (diff >= 0 ):
                    print(f"Below amis are older than 60 days {amiid}")
                    amideletion = client.deregister_image(DryRun=False,ImageId=amiid,)
                    print("Deleted the amis %a" % amideletion)
                else:
                    print("No AMIs older than 60 days found and deregisted successfully!")
