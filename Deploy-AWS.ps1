# AdMorph.AI AWS Deployment PowerShell Script
# Deploys to AWS from Windows without requiring Docker

param(
    [string]$DeploymentType = "ec2",
    [switch]$Help
)

# Colors for output
function Write-Info { 
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue 
}

function Write-Success { 
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green 
}

function Write-Warning { 
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow 
}

function Write-Error { 
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red 
}

function Test-AWSCli {
    Write-Info "Checking AWS CLI..."
    
    if (!(Get-Command aws -ErrorAction SilentlyContinue)) {
        Write-Error "AWS CLI is not installed. Please install it first from: https://aws.amazon.com/cli/"
        exit 1
    }
    
    # Test AWS credentials
    try {
        aws sts get-caller-identity | Out-Null
        Write-Success "AWS CLI configured correctly"
    }
    catch {
        Write-Error "AWS credentials not configured. Please run 'aws configure'"
        exit 1
    }
}

function Deploy-SimpleEC2 {
    Write-Info "Setting up simple EC2 deployment..."
    
    # Get AWS account info
    $AccountId = (aws sts get-caller-identity --query Account --output text)
    $Region = "us-east-1"
    
    # Create key pair if it doesn't exist
    try {
        aws ec2 describe-key-pairs --key-names admorph-key --region $Region | Out-Null
    }
    catch {
        Write-Info "Creating new key pair..."
        aws ec2 create-key-pair --key-name admorph-key --region $Region --query 'KeyMaterial' --output text | Out-File -FilePath "admorph-key.pem" -Encoding ASCII
        Write-Success "Created new key pair: admorph-key.pem"
    }
    
    # Get default VPC
    $VpcId = (aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --region $Region --query 'Vpcs[0].VpcId' --output text)
    
    # Create security group
    $SecurityGroupId = $null
    try {
        $SecurityGroupId = (aws ec2 describe-security-groups --group-names admorph-sg --region $Region --query 'SecurityGroups[0].GroupId' --output text)
    }
    catch {
        Write-Info "Creating security group..."
        $SecurityGroupId = (aws ec2 create-security-group --group-name admorph-sg --description "AdMorph.AI Security Group" --vpc-id $VpcId --region $Region --query 'GroupId' --output text)
        
        # Allow HTTP, HTTPS, and SSH
        aws ec2 authorize-security-group-ingress --group-id $SecurityGroupId --protocol tcp --port 22 --cidr 0.0.0.0/0 --region $Region
        aws ec2 authorize-security-group-ingress --group-id $SecurityGroupId --protocol tcp --port 80 --cidr 0.0.0.0/0 --region $Region
        aws ec2 authorize-security-group-ingress --group-id $SecurityGroupId --protocol tcp --port 443 --cidr 0.0.0.0/0 --region $Region
        aws ec2 authorize-security-group-ingress --group-id $SecurityGroupId --protocol tcp --port 3000 --cidr 0.0.0.0/0 --region $Region
        aws ec2 authorize-security-group-ingress --group-id $SecurityGroupId --protocol tcp --port 8000 --cidr 0.0.0.0/0 --region $Region
        
        Write-Success "Created security group: $SecurityGroupId"
    }
    
    # Create user data script
    $UserData = @"
#!/bin/bash
yum update -y

# Install Node.js
curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
yum install -y nodejs

# Install Python 3.9
yum install -y python39 python39-pip

# Install Git
yum install -y git

# Create directory and copy files (you'll need to upload your code separately)
mkdir -p /opt/admorph
cd /opt/admorph

# Set environment variables
cat > .env << 'ENVEOF'
OPENAI_API_KEY=your-openai-key-here
ADMORPH_ENVIRONMENT=production
ADMORPH_HOST=0.0.0.0
ADMORPH_PORT=8000
ADMORPH_LOG_LEVEL=INFO
ADMORPH_ALLOWED_ORIGINS=*
ENVEOF

# Install dependencies will be done after file upload
"@
    
    $UserData | Out-File -FilePath "user-data.sh" -Encoding UTF8
    
    # Launch EC2 instance
    Write-Info "Launching EC2 instance..."
    $InstanceId = (aws ec2 run-instances --image-id ami-0c02fb55956c7d316 --count 1 --instance-type t3.medium --key-name admorph-key --security-group-ids $SecurityGroupId --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=AdMorphServer}]' --user-data file://user-data.sh --region $Region --query 'Instances[0].InstanceId' --output text)
    
    Write-Success "Launched EC2 instance: $InstanceId"
    
    # Wait for instance to be running
    Write-Info "Waiting for instance to be running..."
    aws ec2 wait instance-running --instance-ids $InstanceId --region $Region
    
    # Get public IP
    $PublicIp = (aws ec2 describe-instances --instance-ids $InstanceId --region $Region --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
    
    Write-Success "Instance is running at: $PublicIp"
    Write-Info "You can SSH to the instance using: ssh -i admorph-key.pem ec2-user@$PublicIp"
    Write-Info "Frontend will be available at: http://$PublicIp:3000"
    Write-Info "Backend API will be available at: http://$PublicIp:8000"
    
    Write-Info "Next steps:"
    Write-Info "1. Upload your code to the instance"
    Write-Info "2. Install dependencies and start services"
    Write-Info "3. Configure your API keys"
}

function Start-LocalDevelopment {
    Write-Info "Starting local development servers..."
    
    # Check if Python is installed
    if (!(Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Warning "Python is not installed. Please install Python 3.8+ from https://python.org"
        return
    }
    
    # Create virtual environment if it doesn't exist
    if (!(Test-Path "venv")) {
        Write-Info "Creating Python virtual environment..."
        python -m venv venv
    }
    
    # Activate virtual environment and install dependencies
    Write-Info "Installing Python dependencies..."
    & ".\venv\Scripts\Activate.ps1"
    pip install -r requirements.txt
    
    Write-Info "Starting backend server..."
    Start-Process powershell -ArgumentList "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; python simple_server.py" -WindowStyle Normal
    
    Write-Info "Starting frontend development server..."
    Start-Process powershell -ArgumentList "-Command", "cd '$PWD'; npm run dev" -WindowStyle Normal
    
    Write-Success "Development servers started!"
    Write-Info "Frontend: http://localhost:3000"
    Write-Info "Backend: http://localhost:8001"
}

function Show-Help {
    Write-Host @"
AdMorph.AI Deployment Script

Usage: .\Deploy-AWS.ps1 [OPTIONS]

Options:
    -DeploymentType <type>   Deployment type: ec2, local (default: ec2)
    -Help                    Show this help message

Examples:
    .\Deploy-AWS.ps1 -DeploymentType local    # Start local development
    .\Deploy-AWS.ps1 -DeploymentType ec2      # Deploy to AWS EC2
    .\Deploy-AWS.ps1 -Help                    # Show this help

Prerequisites:
    - AWS CLI installed and configured
    - Node.js and npm installed
    - Python 3.8+ installed (for local development)
"@
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

Write-Info "Starting AdMorph.AI deployment..."
Write-Info "Deployment type: $DeploymentType"

switch ($DeploymentType.ToLower()) {
    "local" {
        Start-LocalDevelopment
    }
    "ec2" {
        Test-AWSCli
        Deploy-SimpleEC2
    }
    default {
        Write-Error "Unknown deployment type: $DeploymentType"
        Show-Help
        exit 1
    }
}

Write-Success "Deployment completed!" 