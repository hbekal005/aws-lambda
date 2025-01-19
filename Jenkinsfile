pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'
        LAMBDA_BUCKET = 'my-lambda-code-bucket' // The S3 bucket to store the Lambda code
        LAMBDA_CODE_ZIP = 'lambda_code.zip'  // The Lambda zip file
        CFN_STACK_NAME = 'MyLambdaStack'
        CFN_TEMPLATE = 'lambda_deployment.yaml'
        AWS_ACCESS_KEY_ID = 'your-access-key-id'
        AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'

    }
    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from your Git repository
                git 'https://github.com/hbekal005/aws-lambda.git' 
            }
        }
        stage('Package Lambda Code') {
            steps {
                script {
                    // Zip the Lambda code
                    sh 'zip -r ${LAMBDA_CODE_ZIP} *'
                }
            }
        }
        stage('Upload Lambda Code to S3') {
            steps {
                script {
                    // Upload the zip to S3
                    sh """
                    aws s3 cp ${LAMBDA_CODE_ZIP} s3://${LAMBDA_BUCKET}/lambda_code.zip --region ${AWS_REGION}
                    """
                }
            }
        }
        stage('Deploy CloudFormation Stack') {
            steps {
                script {
                    // Deploy the CloudFormation stack
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
    post {
        always {
            // Clean up the local zip file after the pipeline is run
            sh "rm -f ${LAMBDA_CODE_ZIP}"
        }
    }
}
