/**
 * API Client for HRMS Backend
 */
import { API_CONFIG, STORAGE_KEYS } from "@/config";
import type { ApiResponse } from "@/types";

class ApiClient {
  private baseURL: string;
  private timeout: number;

  constructor() {
    this.baseURL = API_CONFIG.BASE_URL;
    this.timeout = API_CONFIG.TIMEOUT;
  }

  /**
   * Get access token from storage
   */
  private getAccessToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  }

  /**
   * Get refresh token from storage
   */
  private getRefreshToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
  }

  /**
   * Set tokens in storage
   */
  private setTokens(access: string, refresh: string): void {
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, access);
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refresh);
  }

  /**
   * Clear tokens from storage
   */
  private clearTokens(): void {
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
    localStorage.removeItem(STORAGE_KEYS.TENANT);
  }

  /**
   * Refresh access token
   */
  private async refreshAccessToken(): Promise<string | null> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) return null;

    try {
      const response = await fetch(
        `${this.baseURL}${API_CONFIG.ENDPOINTS.AUTH.REFRESH}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ refresh: refreshToken }),
        },
      );

      if (response.ok) {
        const data = await response.json();
        this.setTokens(data.data.access, data.data.refresh);
        return data.data.access;
      }

      this.clearTokens();
      return null;
    } catch (error) {
      this.clearTokens();
      return null;
    }
  }

  /**
   * Make HTTP request
   */
  private async request<T = any>(
    endpoint: string,
    options: RequestInit = {},
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    const accessToken = this.getAccessToken();

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string> || {}),
    };

    if (accessToken && !headers["Authorization"]) {
      headers["Authorization"] = `Bearer ${accessToken}`;
    }

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.timeout);

      const response = await fetch(url, {
        ...options,
        headers,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Handle 401 Unauthorized - try to refresh token
      if (response.status === 401 && accessToken) {
        const newAccessToken = await this.refreshAccessToken();

        if (newAccessToken) {
          // Retry request with new token
          headers["Authorization"] = `Bearer ${newAccessToken}`;
          const retryResponse = await fetch(url, {
            ...options,
            headers,
          });

          return await retryResponse.json();
        } else {
          // Redirect to login
          if (typeof window !== "undefined") {
            window.location.href = "/auth/login";
          }
        }
      }

      const data = await response.json();
      return data;
    } catch (error: any) {
      if (error.name === "AbortError") {
        return {
          success: false,
          error: {
            message: "Request timeout",
            code: 408,
          },
        };
      }

      return {
        success: false,
        error: {
          message: error.message || "Network error",
          code: 500,
        },
      };
    }
  }

  /**
   * GET request
   */
  async get<T = any>(
    endpoint: string,
    options?: RequestInit,
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { ...options, method: "GET" });
  }

  /**
   * POST request
   */
  async post<T = any>(
    endpoint: string,
    data?: any,
    options?: RequestInit,
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: "POST",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * PUT request
   */
  async put<T = any>(
    endpoint: string,
    data?: any,
    options?: RequestInit,
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: "PUT",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * PATCH request
   */
  async patch<T = any>(
    endpoint: string,
    data?: any,
    options?: RequestInit,
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      ...options,
      method: "PATCH",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * DELETE request
   */
  async delete<T = any>(
    endpoint: string,
    options?: RequestInit,
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { ...options, method: "DELETE" });
  }

  /**
   * Clear authentication
   */
  clearAuth(): void {
    this.clearTokens();
  }
}

export const apiClient = new ApiClient();
