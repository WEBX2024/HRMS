/**
 * User type definitions
 */
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  phone: string;
  profile_picture?: string;
  is_active: boolean;
  date_joined: string;
  last_login?: string;
  tenant_name?: string;
  roles: string[];
}

/**
 * Authentication types
 */
export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
  tenant_id: string | null;
  tenant_name: string | null;
  roles: string[];
}

export interface TokenRefreshRequest {
  refresh: string;
}

export interface TokenRefreshResponse {
  access: string;
  refresh: string;
}

/**
 * API Response types
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export interface ApiResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
  error?: {
    message: string;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    details?: any;
    code: number;
  };
}

/**
 * Tenant types
 */
export interface Tenant {
  id: string;
  name: string;
  code: string;
  email: string;
  phone: string;
  subscription_plan: string;
  max_employees: number;
  is_active: boolean;
  logo?: string;
  primary_color: string;
}

/**
 * Employee types
 */
export interface Employee {
  id: string;
  employee_id: string;
  user: User;
  department?: Department;
  designation?: Designation;
  manager?: Employee;
  date_of_joining: string;
  employment_type: string;
  status: string;
}

export interface Department {
  id: string;
  name: string;
  code: string;
  description?: string;
}

export interface Designation {
  id: string;
  title: string;
  code: string;
  level: number;
}

/**
 * Attendance types
 */
export interface Attendance {
  id: string;
  employee: Employee;
  date: string;
  check_in?: string;
  check_out?: string;
  work_hours: number;
  status: string;
}

/**
 * Leave types
 */
export interface LeaveRequest {
  id: string;
  employee: Employee;
  leave_type: LeaveType;
  start_date: string;
  end_date: string;
  days: number;
  reason: string;
  status: string;
  approved_by?: User;
  approved_at?: string;
}

export interface LeaveType {
  id: string;
  name: string;
  code: string;
  days_per_year: number;
  is_paid: boolean;
}

export interface LeaveBalance {
  id: string;
  leave_type: LeaveType;
  year: number;
  total_days: number;
  used_days: number;
  pending_days: number;
  available_days: number;
}
