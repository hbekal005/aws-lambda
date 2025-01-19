import boto3
import json
import os
from botocore.exceptions import ClientError
from datetime import datetime

# Assuming VPC is already created. Using default VPC
VPCID = 'vpc-0aaa2e11615b15db2'

# Assuming Subnet is already created
SUBNET_ID = 'subnet-0f13ec32e6b368c21'

# Instance type
INSTANCE_TYPE = 't3.micro'

# AWS Region
REGION = 'us-east-1'

# User Name
USER_NAME = 'hbekal005'

# Amazon Linux 2 AMI (HVM), SSD Volume Type
AMI_ID = 'ami-043a5a82b6cf98947'

# Security Group ID
SECURITY_GROUP_ID = 'sg-09027de0c67feb1d8'

# EC2 client
ec2_client = boto3.client('ec2', region_name=REGION)

# S3 client
s3_client = boto3.client('s3', region_name=REGION)

# Function to create EC2 instance and s3 bucket and upload instance ID to the bucket
def create_ec2_instance_and_s3_bucket(instance_name, index):
    try:
        # Create EC2 instance
        response = ec2_client.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            MinCount=1,
            MaxCount=1,
            SubnetId=SUBNET_ID,
            SecurityGroupIds=[SECURITY_GROUP_ID],
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

        # Create a file with the EC2 instance ID in the /tmp directory
        file_name = os.path.join("/tmp", f"instance_id_{index}.txt")
        with open(file_name, 'w') as file:
            file.write(instance_id)  # Writing the EC2 instance ID to the file
        
        # Create S3 bucket with a unique name
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        bucket_name = f"{USER_NAME}-mys3bucket{index}-{timestamp}"
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': REGION
            }
        )
        print(f"Created S3 bucket: {bucket_name}")
        
        # Upload the file to the S3 bucket (each bucket gets its own instance ID)
        s3_client.upload_file(file_name, bucket_name, file_name)
        print(f"Uploaded instance ID file to {bucket_name}")
        
        # Clean up the local file after upload
        os.remove(file_name)
        
        return instance_id, bucket_name
    
    except ClientError as e:
        print(f"Error creating EC2 instance or S3 bucket {instance_name}: {e}")
        return None, None

def lambda_handler(event, context):
    """AWS Lambda entry point"""
    print("Starting EC2 instance and S3 bucket creation...")

    instance_ids_and_buckets = []
    
    # Loop to create 10 EC2 instances and corresponding S3 buckets
    for i in range(1, 11):
        instance_name = f"myinstance{i}"
        instance_id, bucket_name = create_ec2_instance_and_s3_bucket(instance_name, i)
        
        if instance_id and bucket_name:
            instance_ids_and_buckets.append((instance_id, bucket_name))
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Successfully created 10 EC2 instances and 10 S3 buckets. Instance IDs uploaded.")
    }