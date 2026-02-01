"""
System-wide constants for HRMS SaaS Platform.
All business values should be defined here or in database.
"""

# User Roles
class UserRoles:
    SUPER_ADMIN = 'SUPER_ADMIN'
    COMPANY_ADMIN = 'COMPANY_ADMIN'
    HR_ADMIN = 'HR_ADMIN'
    MANAGER = 'MANAGER'
    EMPLOYEE = 'EMPLOYEE'
    
    CHOICES = [
        (SUPER_ADMIN, 'Super Admin'),
        (COMPANY_ADMIN, 'Company Admin'),
        (HR_ADMIN, 'HR Admin'),
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee'),
    ]
    
    @classmethod
    def get_all_roles(cls):
        return [cls.SUPER_ADMIN, cls.COMPANY_ADMIN, cls.HR_ADMIN, cls.MANAGER, cls.EMPLOYEE]


# Tenant Status
TENANT_STATUS = [
    ('PENDING_VERIFICATION', 'Pending Verification'),
    ('ACTIVE', 'Active'),
    ('SUSPENDED', 'Suspended'),
    ('CANCELLED', 'Cancelled'),
]


# User Status
USER_STATUS = [
    ('INVITED', 'Invited'),
    ('ACTIVE', 'Active'),
    ('SUSPENDED', 'Suspended'),
    ('EXITED', 'Exited'),
]


# Invitation Status
INVITATION_STATUS = [
    ('CREATED', 'Created'),
    ('SENT', 'Sent'),
    ('EXPIRED', 'Expired'),
    ('ACCEPTED', 'Accepted'),
    ('REVOKED', 'Revoked'),
]


# Login Audit Status
LOGIN_STATUS = [
    ('SUCCESS', 'Success'),
    ('FAILED_INVALID_CREDENTIALS', 'Failed - Invalid Credentials'),
    ('FAILED_USER_NOT_FOUND', 'Failed - User Not Found'),
    ('FAILED_INACTIVE', 'Failed - User Inactive'),
    ('FAILED_SUSPENDED', 'Failed - User Suspended'),
    ('FAILED_EXITED', 'Failed - User Exited'),
    ('FAILED_TENANT_SUSPENDED', 'Failed - Tenant Suspended'),
    ('FAILED_TENANT_CANCELLED', 'Failed - Tenant Cancelled'),
    ('FAILED_RATE_LIMIT', 'Failed - Rate Limit Exceeded'),
]





# Employee Status
class EmployeeStatus:
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    ON_LEAVE = 'ON_LEAVE'
    TERMINATED = 'TERMINATED'
    SUSPENDED = 'SUSPENDED'
    
    CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (ON_LEAVE, 'On Leave'),
        (TERMINATED, 'Terminated'),
        (SUSPENDED, 'Suspended'),
    ]


# Attendance Status
class AttendanceStatus:
    PRESENT = 'PRESENT'
    ABSENT = 'ABSENT'
    LATE = 'LATE'
    HALF_DAY = 'HALF_DAY'
    WORK_FROM_HOME = 'WORK_FROM_HOME'
    ON_LEAVE = 'ON_LEAVE'
    HOLIDAY = 'HOLIDAY'
    WEEKEND = 'WEEKEND'
    
    CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (LATE, 'Late'),
        (HALF_DAY, 'Half Day'),
        (WORK_FROM_HOME, 'Work From Home'),
        (ON_LEAVE, 'On Leave'),
        (HOLIDAY, 'Holiday'),
        (WEEKEND, 'Weekend'),
    ]


# Leave Request Status
class LeaveStatus:
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CANCELLED = 'CANCELLED'
    
    CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CANCELLED, 'Cancelled'),
    ]


# Leave Types (Default - can be customized per tenant)
class LeaveTypes:
    CASUAL = 'CASUAL'
    SICK = 'SICK'
    EARNED = 'EARNED'
    MATERNITY = 'MATERNITY'
    PATERNITY = 'PATERNITY'
    UNPAID = 'UNPAID'
    COMPENSATORY = 'COMPENSATORY'
    
    CHOICES = [
        (CASUAL, 'Casual Leave'),
        (SICK, 'Sick Leave'),
        (EARNED, 'Earned Leave'),
        (MATERNITY, 'Maternity Leave'),
        (PATERNITY, 'Paternity Leave'),
        (UNPAID, 'Unpaid Leave'),
        (COMPENSATORY, 'Compensatory Off'),
    ]


# Document Types
class DocumentTypes:
    RESUME = 'RESUME'
    OFFER_LETTER = 'OFFER_LETTER'
    APPOINTMENT_LETTER = 'APPOINTMENT_LETTER'
    ID_PROOF = 'ID_PROOF'
    ADDRESS_PROOF = 'ADDRESS_PROOF'
    EDUCATION_CERTIFICATE = 'EDUCATION_CERTIFICATE'
    EXPERIENCE_LETTER = 'EXPERIENCE_LETTER'
    PAYSLIP = 'PAYSLIP'
    TAX_DOCUMENT = 'TAX_DOCUMENT'
    OTHER = 'OTHER'
    
    CHOICES = [
        (RESUME, 'Resume'),
        (OFFER_LETTER, 'Offer Letter'),
        (APPOINTMENT_LETTER, 'Appointment Letter'),
        (ID_PROOF, 'ID Proof'),
        (ADDRESS_PROOF, 'Address Proof'),
        (EDUCATION_CERTIFICATE, 'Education Certificate'),
        (EXPERIENCE_LETTER, 'Experience Letter'),
        (PAYSLIP, 'Payslip'),
        (TAX_DOCUMENT, 'Tax Document'),
        (OTHER, 'Other'),
    ]


# Subscription Plans
class SubscriptionPlans:
    FREE = 'FREE'
    BASIC = 'BASIC'
    PROFESSIONAL = 'PROFESSIONAL'
    ENTERPRISE = 'ENTERPRISE'
    
    CHOICES = [
        (FREE, 'Free'),
        (BASIC, 'Basic'),
        (PROFESSIONAL, 'Professional'),
        (ENTERPRISE, 'Enterprise'),
    ]
    
    # Plan limits
    LIMITS = {
        FREE: {'max_employees': 10, 'max_storage_mb': 100},
        BASIC: {'max_employees': 50, 'max_storage_mb': 1000},
        PROFESSIONAL: {'max_employees': 200, 'max_storage_mb': 5000},
        ENTERPRISE: {'max_employees': -1, 'max_storage_mb': -1},  # Unlimited
    }

SUBSCRIPTION_PLANS = SubscriptionPlans.CHOICES


# Gender
class Gender:
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'
    PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY'
    
    CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (PREFER_NOT_TO_SAY, 'Prefer not to say'),
    ]


# Error Messages
class ErrorMessages:
    TENANT_NOT_FOUND = 'Tenant not found'
    UNAUTHORIZED_ACCESS = 'You do not have permission to perform this action'
    INVALID_CREDENTIALS = 'Invalid email or password'
    USER_NOT_FOUND = 'User not found'
    EMPLOYEE_NOT_FOUND = 'Employee not found'
    INVALID_TOKEN = 'Invalid or expired token'
    TENANT_MISMATCH = 'Resource does not belong to your organization'
    INSUFFICIENT_LEAVE_BALANCE = 'Insufficient leave balance'
    OVERLAPPING_LEAVE = 'Leave request overlaps with existing leave'
    INVALID_DATE_RANGE = 'Invalid date range'
    MAX_EMPLOYEES_REACHED = 'Maximum employee limit reached for your subscription plan'


# Success Messages
class SuccessMessages:
    LOGIN_SUCCESS = 'Login successful'
    LOGOUT_SUCCESS = 'Logout successful'
    EMPLOYEE_CREATED = 'Employee created successfully'
    EMPLOYEE_UPDATED = 'Employee updated successfully'
    ATTENDANCE_MARKED = 'Attendance marked successfully'
    LEAVE_REQUESTED = 'Leave request submitted successfully'
    LEAVE_APPROVED = 'Leave request approved'
    LEAVE_REJECTED = 'Leave request rejected'
