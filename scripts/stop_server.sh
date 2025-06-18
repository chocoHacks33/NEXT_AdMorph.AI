#!/bin/bash

# Stop the application
pm2 stop admorph-frontend 2>/dev/null || true
pm2 delete admorph-frontend 2>/dev/null || true