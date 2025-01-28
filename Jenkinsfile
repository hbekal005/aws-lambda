pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'  // AWS Region where your resources are located
        LAMBDA_BUCKET = 'hbekal005-lambda-bucket'  // S3 bucket for Lambda code
        LAMBDA_CODE_ZIP = 'lambda_code.zip'  // The Lambda code zip file name
        CFN_STACK_NAME = 'MyLambdaStack'
        CFN_TEMPLATE = 'lambda_deployment.yaml'
        CHANGE_SET_NAME = 'LambdaChangeSet'
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
        stage('Create Change Set') {
            steps {
                script {
                    // Use the withAWS block to securely use AWS credentials
                    withAWS(credentials: 'AWS-User-Acccess', region: AWS_REGION) {
                        // Create a change set for the CloudFormation stack
                        sh """
                        aws cloudformation create-change-set \
                            --stack-name ${CFN_STACK_NAME} \
                            --template-body file://${CFN_TEMPLATE} \
                            --change-set-name ${CHANGE_SET_NAME} \
                            --capabilities CAPABILITY_IAM \
                            --parameters ParameterKey=LambdaCodeS3Bucket,ParameterValue=${LAMBDA_BUCKET} \
                            --region ${AWS_REGION}
                        """
                        
                        // Wait for the change set to be created
                        sh "aws cloudformation wait change-set-create-complete --stack-name ${CFN_STACK_NAME} --change-set-name ${CHANGE_SET_NAME} --region ${AWS_REGION}"
                    }
                }
            }
        }
        stage('Execute Change Set') {
            steps {
                script {
                    // Use the withAWS block to securely use AWS credentials
                    withAWS(credentials: 'AWS-User-Acccess', region: AWS_REGION) {
                        try {
                            // Execute the change set to update the CloudFormation stack
                            sh """
                            aws cloudformation execute-change-set \
                                --stack-name ${CFN_STACK_NAME} \
                                --change-set-name ${CHANGE_SET_NAME} \
                                --region ${AWS_REGION}
                            """
                        } catch (Exception e) {
                            echo "Error executing change set: ${e.message}"
                            // Rollback to the previous stack state
                            sh """
                            aws cloudformation continue-update-rollback \
                                --stack-name ${CFN_STACK_NAME} \
                                --region ${AWS_REGION}
                            """
                            error "Change set execution failed. Rolled back to the previous stack state."
                        }
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