export const config = {
  api: {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    wsUrl: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8001',
    timeout: 30000,
  },
  aws: {
    region: process.env.NEXT_PUBLIC_AWS_REGION || 'us-east-1',
    s3BucketName: process.env.NEXT_PUBLIC_S3_BUCKET_NAME || '',
  },
  app: {
    name: 'AdMorph.AI',
    version: process.env.npm_package_version || '1.0.0',
    environment: process.env.NEXT_PUBLIC_NODE_ENV || 'development',
  },
  features: {
    voiceEnabled: process.env.NEXT_PUBLIC_VOICE_ENABLED === 'true',
    chatEnabled: process.env.NEXT_PUBLIC_CHAT_ENABLED !== 'false',
    analyticsEnabled: process.env.NEXT_PUBLIC_ANALYTICS_ENABLED !== 'false',
  },
};

export const isDevelopment = config.app.environment === 'development';
export const isProduction = config.app.environment === 'production';

export const apiEndpoints = {
  ads: '/ads',
  processing: '/processing',
  analytics: '/analytics',
  agents: '/agents',
  upload: '/upload',
} as const;