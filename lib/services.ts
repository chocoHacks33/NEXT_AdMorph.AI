import { apiClient, createWebSocketClient } from './api';

export interface Ad {
  id: string;
  title: string;
  description: string;
  imageUrl?: string;
  status: 'draft' | 'processing' | 'completed' | 'failed';
  createdAt: string;
  updatedAt: string;
}

export interface ProcessingJob {
  id: string;
  adId: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  message?: string;
  createdAt: string;
}

export interface PerformanceMetrics {
  adId: string;
  impressions: number;
  clicks: number;
  conversions: number;
  ctr: number;
  cost: number;
  revenue: number;
}

export const adService = {
  async getAds(): Promise<Ad[]> {
    const response = await apiClient.get<Ad[]>('/ads');
    return response.data;
  },

  async getAd(id: string): Promise<Ad> {
    const response = await apiClient.get<Ad>(`/ads/${id}`);
    return response.data;
  },

  async createAd(adData: Partial<Ad>): Promise<Ad> {
    const response = await apiClient.post<Ad>('/ads', adData);
    return response.data;
  },

  async updateAd(id: string, adData: Partial<Ad>): Promise<Ad> {
    const response = await apiClient.put<Ad>(`/ads/${id}`, adData);
    return response.data;
  },

  async deleteAd(id: string): Promise<void> {
    await apiClient.delete(`/ads/${id}`);
  },

  async uploadAdAssets(adId: string, files: File[]): Promise<string[]> {
    const uploadPromises = files.map(file => 
      apiClient.uploadFile<{ url: string }>(`/ads/${adId}/assets`, file)
    );
    const responses = await Promise.all(uploadPromises);
    return responses.map(response => response.data.url);
  },
};

export const processingService = {
  async getJobs(): Promise<ProcessingJob[]> {
    const response = await apiClient.get<ProcessingJob[]>('/processing/jobs');
    return response.data;
  },

  async getJob(id: string): Promise<ProcessingJob> {
    const response = await apiClient.get<ProcessingJob>(`/processing/jobs/${id}`);
    return response.data;
  },

  async startProcessing(adId: string, options?: any): Promise<ProcessingJob> {
    const response = await apiClient.post<ProcessingJob>('/processing/start', {
      adId,
      options,
    });
    return response.data;
  },

  async cancelProcessing(jobId: string): Promise<void> {
    await apiClient.post(`/processing/jobs/${jobId}/cancel`);
  },

  createProcessingWebSocket(onUpdate: (job: ProcessingJob) => void) {
    const wsClient = createWebSocketClient('/processing');
    wsClient.connect(
      (data) => {
        if (data.type === 'job_update') {
          onUpdate(data.job);
        }
      },
      (error) => {
        console.error('Processing WebSocket error:', error);
      }
    );
    return wsClient;
  },
};

export const analyticsService = {
  async getPerformanceMetrics(adId?: string): Promise<PerformanceMetrics[]> {
    const endpoint = adId ? `/analytics/performance/${adId}` : '/analytics/performance';
    const response = await apiClient.get<PerformanceMetrics[]>(endpoint);
    return response.data;
  },

  async getPerformanceMetricsRange(
    startDate: string,
    endDate: string,
    adId?: string
  ): Promise<PerformanceMetrics[]> {
    const params = new URLSearchParams({
      startDate,
      endDate,
      ...(adId && { adId }),
    });
    const response = await apiClient.get<PerformanceMetrics[]>(
      `/analytics/performance?${params}`
    );
    return response.data;
  },
};

export const agentService = {
  async sendChatMessage(message: string, sessionId?: string): Promise<{
    response: string;
    sessionId: string;
  }> {
    const response = await apiClient.post<{
      response: string;
      sessionId: string;
    }>('/agents/chat', {
      message,
      sessionId,
    });
    return response.data;
  },

  async getVoiceNarration(text: string, voice?: string): Promise<{ audioUrl: string }> {
    const response = await apiClient.post<{ audioUrl: string }>('/agents/voice/narrate', {
      text,
      voice,
    });
    return response.data;
  },

  createChatWebSocket(
    sessionId: string,
    onMessage: (message: any) => void
  ) {
    const wsClient = createWebSocketClient(`/agents/chat/${sessionId}`);
    wsClient.connect(
      (data) => {
        onMessage(data);
      },
      (error) => {
        console.error('Chat WebSocket error:', error);
      }
    );
    return wsClient;
  },
};