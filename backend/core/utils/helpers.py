"""
Helper utilities for HRMS platform.
"""
from typing import Optional
from django.utils import timezone
from datetime import datetime, timedelta
import re


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate Indian phone number format"""
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, phone) is not None


def calculate_work_hours(check_in: datetime, check_out: Optional[datetime]) -> float:
    """Calculate work hours between check-in and check-out"""
    if not check_out:
        return 0.0
    
    delta = check_out - check_in
    hours = delta.total_seconds() / 3600
    return round(hours, 2)


def calculate_leave_days(start_date, end_date, include_weekends=False) -> float:
    """
    Calculate number of leave days between two dates.
    Excludes weekends by default.
    """
    if start_date > end_date:
        return 0.0
    
    total_days = (end_date - start_date).days + 1
    
    if include_weekends:
        return float(total_days)
    
    # Exclude weekends
    weekdays = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday = 0, Sunday = 6
            weekdays += 1
        current_date += timedelta(days=1)
    
    return float(weekdays)


def get_financial_year(date: Optional[datetime] = None) -> tuple:
    """
    Get financial year start and end dates.
    Indian financial year: April 1 to March 31
    """
    if date is None:
        date = timezone.now()
    
    if date.month >= 4:
        start_year = date.year
        end_year = date.year + 1
    else:
        start_year = date.year - 1
        end_year = date.year
    
    start_date = datetime(start_year, 4, 1).date()
    end_date = datetime(end_year, 3, 31).date()
    
    return start_date, end_date


def generate_employee_id(tenant_code: str, sequence: int) -> str:
    """Generate employee ID in format: TENANT-YYYY-NNNN"""
    year = timezone.now().year
    return f"{tenant_code}-{year}-{sequence:04d}"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove special characters and spaces
    filename = re.sub(r'[^\w\s.-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename.lower()


def get_current_month_date_range() -> tuple:
    """Get start and end date of current month"""
    now = timezone.now()
    start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Get last day of month
    if now.month == 12:
        end_date = now.replace(year=now.year + 1, month=1, day=1, hour=23, minute=59, second=59)
    else:
        end_date = now.replace(month=now.month + 1, day=1, hour=23, minute=59, second=59)
    
    end_date = end_date - timedelta(days=1)
    
    return start_date, end_date
