#!/bin/bash

# AdMorph.AI AWS Deployment Script
# Deploys to AWS without requiring local Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check AWS CLI
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Test AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS credentials not configured. Please run 'aws configure'"
        exit 1
    fi
    
    log_success "AWS CLI configured correctly"
}

# Deploy using AWS CodeBuild/CodeDeploy
deploy_with_codebuild() {
    log_info "Creating CodeBuild project for AdMorph.AI..."
    
    # Create S3 bucket for artifacts if it doesn't exist
    BUCKET_NAME="admorph-deployment-artifacts-$(date +%s)"
    aws s3 mb s3://$BUCKET_NAME --region us-east-1
    
    # Upload source code to S3
    log_info "Uploading source code..."
    zip -r admorph-source.zip . -x "*.git*" "node_modules/*" "venv/*"
    aws s3 cp admorph-source.zip s3://$BUCKET_NAME/
    
    # Create CodeBuild project
    cat > codebuild-project.json << EOF
{
    "name": "admorph-build",
    "source": {
        "type": "S3",
        "location": "$BUCKET_NAME/admorph-source.zip"
    },
    "artifacts": {
        "type": "S3",
        "location": "$BUCKET_NAME"
    },
    "environment": {
        "type": "LINUX_CONTAINER",
        "image": "aws/codebuild/standard:5.0",
        "computeType": "BUILD_GENERAL1_MEDIUM",
        "environmentVariables": [
            {
                "name": "AWS_DEFAULT_REGION",
                "value": "us-east-1"
            },
            {
                "name": "AWS_ACCOUNT_ID",
                "value": "$(aws sts get-caller-identity --query Account --output text)"
            },
            {
                "name": "IMAGE_REPO_NAME",
                "value": "admorph-backend"
            }
        ]
    },
    "serviceRole": "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/service-role/codebuild-service-role"
}
EOF
    
    aws codebuild create-project --cli-input-json file://codebuild-project.json
    
    # Start build
    log_info "Starting CodeBuild..."
    BUILD_ID=$(aws codebuild start-build --project-name admorph-build --query 'build.id' --output text)
    
    log_info "Build started with ID: $BUILD_ID"
    log_info "Monitor build progress in AWS Console: https://console.aws.amazon.com/codesuite/codebuild/projects/admorph-build/build/$BUILD_ID"
}

# Deploy to EC2 using CodeDeploy
deploy_to_ec2() {
    log_info "Deploying to EC2 using CodeDeploy..."
    
    # Create application
    aws deploy create-application --application-name AdMorphApp
    
    # Create deployment group
    aws deploy create-deployment-group \
        --application-name AdMorphApp \
        --deployment-group-name AdMorphDeploymentGroup \
        --service-role-arn arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/CodeDeployServiceRole \
        --ec2-tag-filters Key=Name,Value=AdMorphServer,Type=KEY_AND_VALUE
    
    # Create deployment
    aws deploy create-deployment \
        --application-name AdMorphApp \
        --deployment-group-name AdMorphDeploymentGroup \
        --s3-location bucket=$BUCKET_NAME,key=admorph-source.zip,bundleType=zip
}

# Simple EC2 deployment
deploy_simple_ec2() {
    log_info "Setting up simple EC2 deployment..."
    
    # Create key pair if it doesn't exist
    if ! aws ec2 describe-key-pairs --key-names admorph-key &> /dev/null; then
        aws ec2 create-key-pair --key-name admorph-key --query 'KeyMaterial' --output text > admorph-key.pem
        chmod 400 admorph-key.pem
        log_success "Created new key pair: admorph-key.pem"
    fi
    
    # Create security group
    VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId' --output text)
    
    if ! aws ec2 describe-security-groups --group-names admorph-sg &> /dev/null; then
        SECURITY_GROUP_ID=$(aws ec2 create-security-group \
            --group-name admorph-sg \
            --description "AdMorph.AI Security Group" \
            --vpc-id $VPC_ID \
            --query 'GroupId' --output text)
        
        # Allow HTTP, HTTPS, and SSH
        aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr 0.0.0.0/0
        aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 80 --cidr 0.0.0.0/0
        aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 443 --cidr 0.0.0.0/0
        aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 3000 --cidr 0.0.0.0/0
        aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 8000 --cidr 0.0.0.0/0
        
        log_success "Created security group: $SECURITY_GROUP_ID"
    else
        SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --group-names admorph-sg --query 'SecurityGroups[0].GroupId' --output text)
    fi
    
    # Launch EC2 instance
    INSTANCE_ID=$(aws ec2 run-instances \
        --image-id ami-0c02fb55956c7d316 \
        --count 1 \
        --instance-type t3.medium \
        --key-name admorph-key \
        --security-group-ids $SECURITY_GROUP_ID \
        --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=AdMorphServer}]' \
        --user-data file://user-data.sh \
        --query 'Instances[0].InstanceId' --output text)
    
    log_success "Launched EC2 instance: $INSTANCE_ID"
    
    # Wait for instance to be running
    log_info "Waiting for instance to be running..."
    aws ec2 wait instance-running --instance-ids $INSTANCE_ID
    
    # Get public IP
    PUBLIC_IP=$(aws ec2 describe-instances \
        --instance-ids $INSTANCE_ID \
        --query 'Reservations[0].Instances[0].PublicIpAddress' \
        --output text)
    
    log_success "Instance is running at: $PUBLIC_IP"
    log_info "Frontend will be available at: http://$PUBLIC_IP:3000"
    log_info "Backend API will be available at: http://$PUBLIC_IP:8000"
}

# Create user data script for EC2
create_user_data() {
    cat > user-data.sh << 'EOF'
#!/bin/bash
yum update -y

# Install Node.js
curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
yum install -y nodejs

# Install Python 3.9
yum install -y python39 python39-pip

# Install Git
yum install -y git

# Clone the repository (you'll need to update this with your actual repo)
cd /opt
git clone https://github.com/your-username/admorph.git
cd admorph/NEXT_AdMorph.AI

# Install Python dependencies
python3.9 -m pip install -r requirements.txt

# Install Node.js dependencies
npm install --legacy-peer-deps

# Set environment variables (update with your actual values)
cat > .env << 'ENVEOF'
OPENAI_API_KEY=your-openai-key-here
ADMORPH_ENVIRONMENT=production
ADMORPH_HOST=0.0.0.0
ADMORPH_PORT=8000
ADMORPH_LOG_LEVEL=INFO
ADMORPH_ALLOWED_ORIGINS=*
ENVEOF

# Build the frontend
npm run build

# Start the backend
nohup python3.9 simple_server.py > backend.log 2>&1 &

# Start the frontend
nohup npm start > frontend.log 2>&1 &
EOF
}

# Deploy using AWS Lambda (Serverless)
deploy_serverless() {
    log_info "Deploying as serverless using AWS Lambda..."
    
    # Install Serverless Framework if not present
    if ! command -v serverless &> /dev/null; then
        npm install -g serverless
    fi
    
    # Create serverless.yml configuration
    cat > serverless.yml << EOF
service: admorph-backend

provider:
  name: aws
  runtime: python3.9
  region: us-east-1
  environment:
    OPENAI_API_KEY: \${env:OPENAI_API_KEY}
    ADMORPH_ENVIRONMENT: production

functions:
  api:
    handler: handler.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
      - http:
          path: /
          method: ANY
          cors: true

plugins:
  - serverless-python-requirements
  - serverless-wsgi

custom:
  wsgi:
    app: admorph_backend.api.main.app
    packRequirements: false
  pythonRequirements:
    dockerizePip: non-linux
EOF
    
    # Create handler
    cat > handler.py << 'EOF'
import serverless_wsgi
from admorph_backend.api.main import app

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
EOF
    
    # Deploy
    serverless deploy
}

main() {
    log_info "Starting AdMorph.AI AWS Deployment..."
    
    # Parse arguments
    DEPLOYMENT_TYPE="ec2"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --lambda)
                DEPLOYMENT_TYPE="lambda"
                shift
                ;;
            --ecs)
                DEPLOYMENT_TYPE="ecs"
                shift
                ;;
            --ec2)
                DEPLOYMENT_TYPE="ec2"
                shift
                ;;
            --help)
                echo "Usage: $0 [OPTIONS]"
                echo "Options:"
                echo "  --ec2       Deploy to EC2 (default)"
                echo "  --lambda    Deploy as serverless Lambda"
                echo "  --ecs       Deploy using ECS/CodeBuild"
                echo "  --help      Show this help"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Check prerequisites
    check_aws_cli
    
    # Create user data if deploying to EC2
    if [ "$DEPLOYMENT_TYPE" = "ec2" ]; then
        create_user_data
    fi
    
    # Deploy based on type
    case $DEPLOYMENT_TYPE in
        "ec2")
            deploy_simple_ec2
            ;;
        "lambda")
            deploy_serverless
            ;;
        "ecs")
            deploy_with_codebuild
            ;;
    esac
    
    log_success "Deployment completed!"
}

main "$@" 