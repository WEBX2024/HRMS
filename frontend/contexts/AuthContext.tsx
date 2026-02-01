"use client";

/**
 * Authentication Context Provider
 */
import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { AuthService } from "@/services/auth.service";
import type { User, LoginRequest } from "@/types";
import { ROUTES } from "@/config";

interface AuthContextType {
  user: User | null;
  tenant: { id: string; name: string } | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (
    credentials: LoginRequest,
  ) => Promise<{ success: boolean; error?: string }>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [tenant, setTenant] = useState<{ id: string; name: string } | null>(
    null,
  );
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Initialize auth state
  useEffect(() => {
    const initAuth = () => {
      const currentUser = AuthService.getCurrentUser();
      const currentTenant = AuthService.getCurrentTenant();

      setUser(currentUser);
      setTenant(currentTenant);
      setIsLoading(false);
    };

    initAuth();
  }, []);

  /**
   * Login function
   */
  const login = async (credentials: LoginRequest) => {
    try {
      const response = await AuthService.login(credentials);

      if (response.success && response.data) {
        setUser(response.data.user);

        if (response.data.tenant_id) {
          setTenant({
            id: response.data.tenant_id,
            name: response.data.tenant_name || "",
          });
        }

        // Redirect based on role
        const roles = response.data.roles;
        if (roles.includes("SUPER_ADMIN")) {
          router.push(ROUTES.SUPER_ADMIN);
        } else if (roles.includes("COMPANY_ADMIN")) {
          router.push(ROUTES.COMPANY_ADMIN);
        } else if (roles.includes("HR_ADMIN")) {
          router.push(ROUTES.HR);
        } else if (roles.includes("MANAGER")) {
          router.push(ROUTES.MANAGER);
        } else {
          router.push(ROUTES.EMPLOYEE);
        }

        return { success: true };
      }

      return {
        success: false,
        error: response.error?.message || "Login failed",
      };
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "An error occurred";
      return {
        success: false,
        error: errorMessage,
      };
    }
  };

  /**
   * Logout function
   */
  const logout = async () => {
    await AuthService.logout();
    setUser(null);
    setTenant(null);
    router.push(ROUTES.LOGIN);
  };

  /**
   * Refresh user data
   */
  const refreshUser = async () => {
    try {
      const response = await AuthService.getProfile();
      if (response.success && response.data) {
        setUser(response.data);
      }
    } catch (error) {
      console.error("Failed to refresh user:", error);
    }
  };

  const value: AuthContextType = {
    user,
    tenant,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to use auth context
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
