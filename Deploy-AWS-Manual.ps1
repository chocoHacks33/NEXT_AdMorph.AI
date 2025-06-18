# AdMorph.AI AWS Manual Deployment Script
# Deploy to AWS using AWS Tools for PowerShell (alternative to AWS CLI)

param(
    [string]$Region = "us-east-1",
    [string]$KeyPairName = "admorph-keypair",
    [switch]$Help
)

function Write-Info { 
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue 
}

function Write-Success { 
    param($Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green 
}

function Write-Error { 
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red 
}

function Show-Help {
    Write-Host @"
AdMorph.AI AWS Manual Deployment Script

This script provides multiple AWS deployment options without requiring AWS CLI.

Usage: .\Deploy-AWS-Manual.ps1 [OPTIONS]

Options:
    -Region <region>        AWS region (default: us-east-1)
    -KeyPairName <name>     Key pair name (default: admorph-keypair)
    -Help                   Show this help

Deployment Options:
1. AWS Amplify (Frontend + Serverless Backend)
2. S3 + CloudFront (Static Frontend)
3. Manual EC2 Setup Instructions
4. AWS CodeBuild/CodeDeploy

Prerequisites:
- AWS account with proper permissions
- Git repository (GitHub/GitLab)
- Environment variables configured

"@
}

function Deploy-WithAmplify {
    Write-Info "Setting up AWS Amplify deployment..."
    
    Write-Info @"
AWS Amplify Deployment Steps:

1. Go to AWS Console: https://console.aws.amazon.com/amplify/
2. Click 'New app' > 'Host web app'
3. Connect your Git repository (GitHub/GitLab)
4. Select branch: main
5. Build settings will use our amplify.yml file
6. Add environment variables:
   - OPENAI_API_KEY: your-openai-key
   - ADMORPH_ENVIRONMENT: production
   - META_ACCESS_TOKEN: your-meta-token (optional)

This will deploy both frontend and backend automatically!
"@
    
    Write-Success "Amplify configuration ready! Visit AWS Console to complete setup."
}

function Deploy-ToS3 {
    Write-Info "Setting up S3 + CloudFront deployment..."
    
    # Build the frontend
    Write-Info "Building frontend for production..."
    npm run build
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Frontend built successfully!"
        Write-Info @"
S3 + CloudFront Deployment Steps:

1. Go to AWS S3 Console: https://s3.console.aws.amazon.com/
2. Create a new bucket (e.g., 'admorph-frontend-bucket')
3. Enable static website hosting
4. Upload the contents of the 'out' or '.next' folder
5. Go to CloudFront Console: https://console.aws.amazon.com/cloudfront/
6. Create a distribution pointing to your S3 bucket
7. Configure custom domain (optional)

Your built files are ready in the .next directory!
"@
    } else {
        Write-Error "Frontend build failed. Please check for errors."
    }
}

function Show-EC2Instructions {
    Write-Info @"
Manual EC2 Deployment Instructions:

1. Go to EC2 Console: https://console.aws.amazon.com/ec2/
2. Launch Instance:
   - AMI: Amazon Linux 2 AMI (ami-0c02fb55956c7d316)
   - Instance Type: t3.medium (or larger)
   - Key Pair: Create or use existing
   - Security Group: Allow ports 22, 80, 443, 3000, 8000

3. Connect to instance:
   ssh -i your-key.pem ec2-user@your-instance-ip

4. Install dependencies:
   sudo yum update -y
   sudo yum install -y nodejs npm python3 python3-pip git
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
   source ~/.bashrc
   nvm install 18
   nvm use 18

5. Upload and setup project:
   # Use SCP to upload your project files
   cd /opt/admorph
   sudo npm install --legacy-peer-deps
   sudo python3 -m pip install -r requirements.txt

6. Start services:
   # Backend
   nohup python3 simple_server.py &
   # Frontend
   nohup npm start &

7. Access your app:
   http://your-instance-ip:3000
"@
}

function Deploy-WithCodePipeline {
    Write-Info @"
AWS CodeBuild/CodeDeploy Setup:

1. Create S3 bucket for artifacts
2. Upload your code as a ZIP file
3. Create CodeBuild project:
   - Source: S3
   - Buildspec: Use our buildspec.yml
   - Environment: Standard Linux
4. Create CodeDeploy application:
   - Platform: EC2/On-premises
   - Deployment group: EC2 instances with specific tags
5. Create deployment pipeline

This uses the existing buildspec.yml and appspec.yml files in your project.
"@
}

function Create-UserDataScript {
    $UserDataScript = @"
#!/bin/bash
yum update -y

# Install Node.js
curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
yum install -y nodejs

# Install Python 3.9
yum install -y python39 python39-pip

# Install Git
yum install -y git

# Create directory for application
mkdir -p /opt/admorph
cd /opt/admorph

# Set up environment variables
cat > .env << 'EOF'
OPENAI_API_KEY=your-openai-key-here
ADMORPH_ENVIRONMENT=production
ADMORPH_HOST=0.0.0.0
ADMORPH_PORT=8000
ADMORPH_LOG_LEVEL=INFO
ADMORPH_ALLOWED_ORIGINS=*
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF

# Note: You'll need to upload your application files separately
# Then run:
# npm install --legacy-peer-deps
# python3.9 -m pip install -r requirements.txt
# npm run build
# nohup python3.9 simple_server.py &
# nohup npm start &

echo "Server setup complete. Upload your application files and start services."
"@
    
    $UserDataScript | Out-File -FilePath "ec2-user-data.sh" -Encoding UTF8
    Write-Success "Created ec2-user-data.sh file for EC2 instance setup"
}

function Show-DeploymentMenu {
    Write-Host @"

🚀 AdMorph.AI AWS Deployment Options:

1. AWS Amplify (Recommended) - Full-stack deployment
2. S3 + CloudFront - Static frontend deployment  
3. Manual EC2 Setup - Custom server deployment
4. CodeBuild/CodeDeploy - CI/CD pipeline
5. Create EC2 User Data Script
6. Exit

"@
    
    $choice = Read-Host "Select deployment option (1-6)"
    
    switch ($choice) {
        "1" { Deploy-WithAmplify }
        "2" { Deploy-ToS3 }
        "3" { Show-EC2Instructions }
        "4" { Deploy-WithCodePipeline }
        "5" { Create-UserDataScript }
        "6" { exit 0 }
        default { 
            Write-Error "Invalid choice. Please select 1-6."
            Show-DeploymentMenu
        }
    }
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

Write-Info "AdMorph.AI AWS Deployment Helper"
Write-Info "Region: $Region"

Show-DeploymentMenu

Write-Success "Deployment setup completed!" 