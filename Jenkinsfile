pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'  // AWS Region where your resources are located
        LAMBDA_BUCKET = 'hbekal005-lambda-bucket'  // S3 bucket for Lambda code
        LAMBDA_CODE_ZIP = 'lambda_code.zip'  // The Lambda code zip file name
        CFN_STACK_NAME = 'MyLambdaStack'
        CFN_TEMPLATE = 'lambda_deployment.yaml'
    }
    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the 'bugfix/post-submission' branch of your Git repository
                git branch: 'bugfix/post-submission', url: 'https://github.com/hbekal005/aws-lambda.git'
            }
        }
        stage('Package Lambda Code') {
            steps {
                script {
                    // Zip the Lambda code into the specified file, excluding Jenkinsfile and README.md
                    sh 'zip -r ${LAMBDA_CODE_ZIP} * -x Jenkinsfile README.md'
                }
            }
        }
        stage('Upload Lambda Code to S3') {
            steps {
                script {
                    // Use the withAWS block to securely use AWS credentials
                    withAWS(credentials: 'AWS-User-Acccess', region: AWS_REGION) {
                        // Check if the S3 bucket exists
                        def bucketExists = sh(script: "aws s3 ls s3://${LAMBDA_BUCKET} --region ${AWS_REGION}", returnStatus: true) == 0
                        
                        if (bucketExists) {
                            echo "Bucket ${LAMBDA_BUCKET} exists. Uploading the file."
                        } else {
                            echo "Bucket ${LAMBDA_BUCKET} does not exist. Creating the bucket."
                            sh "aws s3 mb s3://${LAMBDA_BUCKET} --region ${AWS_REGION}"
                        }
                        
                        // Upload the zip file to S3 using AWS CLI with the credentials
                        sh "aws s3 cp ${LAMBDA_CODE_ZIP} s3://${LAMBDA_BUCKET}/lambda_code.zip --region ${AWS_REGION}"
                    }
                }
            }
        }
        stage('Check and Delete Existing CloudFormation Stack') {
            steps {
                script {
                    // Use the withAWS block to securely use AWS credentials
                    withAWS(credentials: 'AWS-User-Acccess', region: AWS_REGION) {
                        // Check if the CloudFormation stack exists
                        def stackExists = sh(script: "aws cloudformation describe-stacks --stack-name ${CFN_STACK_NAME} --region ${AWS_REGION}", returnStatus: true) == 0
                        
                        if (stackExists) {
                            echo "Stack ${CFN_STACK_NAME} exists. Deleting the stack."
                            sh "aws cloudformation delete-stack --stack-name ${CFN_STACK_NAME} --region ${AWS_REGION}"
                            
                            // Wait for the stack to be deleted
                            sh "aws cloudformation wait stack-delete-complete --stack-name ${CFN_STACK_NAME} --region ${AWS_REGION}"
                        } else {
                            echo "Stack ${CFN_STACK_NAME} does not exist. Proceeding with deployment."
                        }
                    }
                }
            }
        }
        stage('Deploy CloudFormation Stack') {
            steps {
                script {
                    // Use the withAWS block to securely use AWS credentials
                    withAWS(credentials: 'AWS-User-Acccess', region: AWS_REGION) {
                        // Deploy the CloudFormation stack using AWS CLI with the credentials
                        sh """
                        aws cloudformation deploy \
                            --template-file ${CFN_TEMPLATE} \
                            --stack-name ${CFN_STACK_NAME} \
                            --parameter-overrides LambdaCodeS3Bucket=${LAMBDA_BUCKET} \
                            --capabilities CAPABILITY_IAM \
                            --region ${AWS_REGION}
                        """
                    }
                }
            }
        }
    }
    post {
        always {
            // Clean up the local zip file after the pipeline is run
            sh "rm -f ${LAMBDA_CODE_ZIP}"
        }
    }
}