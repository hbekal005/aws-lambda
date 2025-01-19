import boto3
import json
import os
from boto3.exceptions import ClientError


# Assuming VPC is already created. Using default VPC
VPCID = 'vpc-07f3a085add361764'

# Assuming Subnet is already created
SUBNET_ID = 'subnet-0c55b159cbfafe1f0'

# Instance type
INSTANCE_TYPE = 't3.micro'

# AWS Region
REGION = 'us-east-1'

# User Name
USER_NAME = 'hbekal005'

# AWS AMI ID
AMI_ID = 'ami-0c55b159cbfafe1f0'

# EC2 client
ec2_client = boto3.client('ec2', region_name=REGION)

# S3 client
s3_client = boto3.client('s3', region_name=REGION)

# Function to create EC2 instance and return instance ID
def create_ec2_instance(instance_name):
    try:
        response = ec2_client.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            MinCount=1,
            MaxCount=1,
            SubnetId=SUBNET_ID,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        }
                    ]
                }
            ]
        )
        instance_id = response['Instances'][0]['InstanceId']
        print(f"Created EC2 instance: {instance_name} with ID: {instance_id}")
        return instance_id
    
    except ClientError as e:
        print(f"Error creating EC2 instance {instance_name}: {e}")
        return None



def lambda_handler(event, context):
    print("Starting EC2 instance creation and S3 bucket setup...")
    create_ec2_instance(event, context)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }