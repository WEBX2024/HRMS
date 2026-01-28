/**
 * Authentication Service
 */
import { apiClient } from "@/lib/api-client";
import { API_CONFIG, STORAGE_KEYS } from "@/config";
import type { LoginRequest, LoginResponse, User, ApiResponse } from "@/types";

export class AuthService {
  /**
   * Login user
   */
  static async login(
    credentials: LoginRequest,
  ): Promise<ApiResponse<LoginResponse>> {
    const response = await apiClient.post<LoginResponse>(
      API_CONFIG.ENDPOINTS.AUTH.LOGIN,
      credentials,
    );

    if (response.success && response.data) {
      // Store tokens
      localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.data.access);
      localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.data.refresh);

      // Store user data
      localStorage.setItem(
        STORAGE_KEYS.USER,
        JSON.stringify(response.data.user),
      );

      // Store tenant data
      if (response.data.tenant_id) {
        localStorage.setItem(
          STORAGE_KEYS.TENANT,
          JSON.stringify({
            id: response.data.tenant_id,
            name: response.data.tenant_name,
          }),
        );
      }
    }

    return response;
  }

  /**
   * Logout user
   */
  static async logout(): Promise<void> {
    const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);

    if (refreshToken) {
      try {
        await apiClient.post(API_CONFIG.ENDPOINTS.AUTH.LOGOUT, {
          refresh: refreshToken,
        });
      } catch (error) {
        // Ignore logout errors
      }
    }

    // Clear all auth data
    apiClient.clearAuth();
  }

  /**
   * Get current user from storage
   */
  static getCurrentUser(): User | null {
    const userStr = localStorage.getItem(STORAGE_KEYS.USER);
    if (!userStr) return null;

    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  }

  /**
   * Get current tenant from storage
   */
  static getCurrentTenant(): { id: string; name: string } | null {
    const tenantStr = localStorage.getItem(STORAGE_KEYS.TENANT);
    if (!tenantStr) return null;

    try {
      return JSON.parse(tenantStr);
    } catch {
      return null;
    }
  }

  /**
   * Check if user is authenticated
   */
  static isAuthenticated(): boolean {
    return !!localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  }

  /**
   * Get user profile
   */
  static async getProfile(): Promise<ApiResponse<User>> {
    return apiClient.get<User>(API_CONFIG.ENDPOINTS.AUTH.PROFILE);
  }

  /**
   * Update user profile
   */
  static async updateProfile(data: Partial<User>): Promise<ApiResponse<User>> {
    const response = await apiClient.put<User>(
      API_CONFIG.ENDPOINTS.AUTH.PROFILE,
      data,
    );

    if (response.success && response.data) {
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data));
    }

    return response;
  }

  /**
   * Change password
   */
  static async changePassword(data: {
    old_password: string;
    new_password: string;
    confirm_password: string;
  }): Promise<ApiResponse> {
    return apiClient.post(API_CONFIG.ENDPOINTS.AUTH.CHANGE_PASSWORD, data);
  }

  /**
   * Get user roles
   */
  static getUserRoles(): string[] {
    const user = this.getCurrentUser();
    return user?.roles || [];
  }

  /**
   * Check if user has specific role
   */
  static hasRole(role: string): boolean {
    const roles = this.getUserRoles();
    return roles.includes(role);
  }

  /**
   * Check if user has any of the specified roles
   */
  static hasAnyRole(roles: string[]): boolean {
    const userRoles = this.getUserRoles();
    return roles.some((role) => userRoles.includes(role));
  }
}
