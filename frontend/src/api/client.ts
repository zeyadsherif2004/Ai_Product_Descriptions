import axios, { AxiosError } from "axios";
import { getIdToken } from "../auth/token";

function trimTrailingSlash(s: string) { return s.endsWith("/") ? s.slice(0, -1) : s; }
const env = (import.meta as any).env || {};
const base = env.VITE_API_BASE_URL || env.VITE_API_BASE || "http://localhost:8000";
export const API_BASE = trimTrailingSlash(String(base));
export const api = axios.create({ baseURL: API_BASE, timeout: 300000, headers: { "Content-Type": "application/json" } });

// Add authentication interceptor
api.interceptors.request.use(async (config) => {
  const token = await getIdToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  } else {
    // Add a small delay and retry once to handle race conditions
    await new Promise(resolve => setTimeout(resolve, 100));
    const retryToken = await getIdToken();
    if (retryToken) {
      config.headers.Authorization = `Bearer ${retryToken}`;
    }
  }
  return config;
});

// Enhanced error handling for rate limits and payment errors
export function handleApiError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError;

    if (axiosError.response?.status === 429) {
      const retryAfter = axiosError.response.headers['retry-after'];
      const seconds = retryAfter ? parseInt(retryAfter) : 60;
      return `Rate limit exceeded. Please wait ${seconds} seconds before trying again.`;
    }

    if (axiosError.response?.status === 400) {
      const errorData = axiosError.response.data as any;
      if (errorData?.error_code === 'INSUFFICIENT_CREDITS') {
        return "Insufficient credits. Please upgrade your plan or purchase more credits.";
      }
      if (errorData?.error_code === 'SUBSCRIPTION_REQUIRED') {
        return "Active subscription required. Please upgrade your plan to continue.";
      }
      if (errorData?.error_code === 'SUBSCRIPTION_EXPIRED') {
        return "Your subscription has expired. Please renew to continue using the service.";
      }
      return "Invalid request. Please check your input and try again.";
    }

    if (axiosError.response?.status === 401) {
      return "Authentication required. Please sign in and try again.";
    }

    if (axiosError.response?.status === 402) {
      return "Payment required. Please upgrade your plan or purchase credits to continue.";
    }

    if (axiosError.response?.status === 403) {
      const errorData = axiosError.response.data as any;
      if (errorData?.error_code === 'CREDIT_LIMIT_EXCEEDED') {
        return "Credit limit exceeded. Please upgrade your plan for higher limits.";
      }
      return "Access denied. Please check your subscription status.";
    }

    if (axiosError.response?.status === 500) {
      return "Server error. Please try again later.";
    }

    if (axiosError.code === 'ECONNABORTED') {
      return "Request timed out. Please try again.";
    }
  }

  return error instanceof Error ? error.message : "An unexpected error occurred.";
}

// Payment API functions (avoiding circular dependency)
export const paymentApi = {
  // Basic API methods that will be implemented directly
  getPlans: async () => {
    const response = await api.get('/api/payment/plans');
    return response.data.plans;
  },
  getSubscription: async () => {
    try {
      const response = await api.get('/api/payment/user/subscription');
      return response.data.data;
    } catch (error) {
      // Handle 404 as "no subscription" - this is normal for new users
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as any;
        if (axiosError.response?.status === 404) {
          return null; // No subscription exists
        }
      }
      // Re-throw other errors (500, network issues, etc.)
      throw error;
    }
  },
  getCreditBalance: async () => {
    const response = await api.get('/api/payment/user/credits');
    return response.data.data;
  },
  getUsageStats: async () => {
    const response = await api.get('/api/payment/user/usage');
    return response.data.data;
  },
  getPaymentHistory: async (page: number = 1, itemsPerPage: number = 10) => {
    const response = await api.get(`/api/payment/user/history?page=${page}&limit=${itemsPerPage}`);
    return response.data.data;
  },
  createCheckoutSession: async (variantId: string, successUrl?: string, cancelUrl?: string) => {
    const response = await api.post('/api/payment/checkout', {
      variant_id: variantId,
      success_url: successUrl,
      cancel_url: cancelUrl
    });

    // Backend returns checkout data directly, not wrapped in 'data' property
    return response.data;
  },
  cancelSubscription: async (subscriptionId: string) => {
    const response = await api.post(`/api/payment/subscription/${subscriptionId}/cancel`);
    return response.data.data;
  },
  reactivateSubscription: async (subscriptionId: string) => {
    const response = await api.post(`/api/payment/subscription/${subscriptionId}/reactivate`);
    return response.data.data;
  },
  updateSubscription: async (subscriptionId: string, updates: any) => {
    const response = await api.patch(`/api/payment/subscription/${subscriptionId}`, updates);
    return response.data.data;
  },
  handleWebhook: async (webhookData: any) => {
    const response = await api.post('/api/payment/webhook', webhookData);
    return response.data.data;
  }
};