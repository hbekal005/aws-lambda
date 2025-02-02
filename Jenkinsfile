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
                // Checkout the code from the 'main' branch of your Git repository
                git branch: 'main', url: 'https://github.com/hbekal005/aws-lambda.git'
            }
        }
        stage('Package Lambda Code') {
            steps {
                script {
                    // Zip the Lambda code into the specified file
                    sh 'zip -r ${LAMBDA_CODE_ZIP} *'
                }
            }
        }
        stage('Upload Lambda Code to S3') {
            steps {
                script {
                    // Use the withAWS block to securely use AWS credentials
                    withAWS(credentials: 'AWS-User-Acccess', region: AWS_REGION) {
                        // Upload the zip file to S3 using AWS CLI with the credentials
                        sh """
                        aws s3 cp ${LAMBDA_CODE_ZIP} s3://${LAMBDA_BUCKET}/lambda_code.zip --region ${AWS_REGION}
                        """
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
