import boto3
import json
import os


# Assuming VPC is already created. Using default VPC
VPCID = 'vpc-07f3a085add361764'
# Assuming Subnet is already created
SUBNETID = 'subnet-0c55b159cbfafe1f0'

# Instance type
INSTANCE_TYPE = 't3.micro'

# AWS Region
REGION = 'us-east-1'

# User Name
USER_NAME = 'hbekal005'

ec2_client = boto3.client('ec2', region_name=REGION)
s3_client = boto3.client('s3', region_name=REGION)

def create_ec2_instance(event, context):
    instance_ids = []
    for i in range(1, 11)
         instance_name = f"myinstance{i}"