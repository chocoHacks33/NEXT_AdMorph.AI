#!/bin/bash

# Update package manager
yum update -y

# Install Node.js 18 if not present
if ! command -v node &> /dev/null; then
    curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
    yum install -y nodejs
fi

# Install pnpm if not present
if ! command -v pnpm &> /dev/null; then
    npm install -g pnpm
fi

# Install Docker if not present (for containerized deployment)
if ! command -v docker &> /dev/null; then
    yum install -y docker
    systemctl start docker
    systemctl enable docker
fi

# Install dependencies
cd /opt/admorph-frontend
pnpm install --frozen-lockfile