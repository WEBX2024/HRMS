/**
 * API Configuration
 */
export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  ENDPOINTS: {
    AUTH: {
      LOGIN: "/api/v1/auth/login/",
      LOGOUT: "/api/v1/auth/logout/",
      REFRESH: "/api/v1/auth/refresh/",
      PROFILE: "/api/v1/auth/profile/",
      CHANGE_PASSWORD: "/api/v1/auth/change-password/",
    },
  },
  TIMEOUT: 30000, // 30 seconds
};

/**
 * App Configuration
 */
export const APP_CONFIG = {
  NAME: "HRMS Pro",
  DESCRIPTION: "Professional Human Resource Management System",
  VERSION: "1.0.0",
};

/**
 * Storage Keys
 */
export const STORAGE_KEYS = {
  ACCESS_TOKEN: "hrms_access_token",
  REFRESH_TOKEN: "hrms_refresh_token",
  USER: "hrms_user",
  TENANT: "hrms_tenant",
};

/**
 * User Roles
 */
export const USER_ROLES = {
  SUPER_ADMIN: "SUPER_ADMIN",
  COMPANY_ADMIN: "COMPANY_ADMIN",
  HR_ADMIN: "HR_ADMIN",
  MANAGER: "MANAGER",
  EMPLOYEE: "EMPLOYEE",
} as const;

export type UserRole = (typeof USER_ROLES)[keyof typeof USER_ROLES];

/**
 * Route Paths
 */
export const ROUTES = {
  HOME: "/",
  LOGIN: "/auth/login",
  REGISTER: "/auth/register",
  FORGOT_PASSWORD: "/auth/forgot-password",

  // Dashboards
  SUPER_ADMIN: "/super-admin",
  COMPANY_ADMIN: "/company-admin",
  HR: "/hr",
  MANAGER: "/manager",
  EMPLOYEE: "/employee",

  // Features
  EMPLOYEES: "/employees",
  ATTENDANCE: "/attendance",
  LEAVE: "/leave",
  PAYROLL: "/payroll",
  DOCUMENTS: "/documents",
  REPORTS: "/reports",
  SETTINGS: "/settings",
} as const;

/**
 * Animation Variants for Framer Motion
 */
export const ANIMATION_VARIANTS = {
  fadeIn: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
  },
  fadeInUp: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 20 },
  },
  fadeInDown: {
    initial: { opacity: 0, y: -20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -20 },
  },
  slideInLeft: {
    initial: { opacity: 0, x: -30 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -30 },
  },
  slideInRight: {
    initial: { opacity: 0, x: 30 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: 30 },
  },
  scaleIn: {
    initial: { opacity: 0, scale: 0.95 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 0.95 },
  },
};
