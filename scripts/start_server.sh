#!/bin/bash

cd /opt/admorph-frontend

# Build the application
pnpm run build

# Start the application using PM2 for production
if ! command -v pm2 &> /dev/null; then
    npm install -g pm2
fi

# Stop any existing process
pm2 stop admorph-frontend 2>/dev/null || true
pm2 delete admorph-frontend 2>/dev/null || true

# Start the application
pm2 start npm --name "admorph-frontend" -- start
pm2 save