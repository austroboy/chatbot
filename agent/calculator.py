# agent/calculator.py
import re
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

def parse_date(date_str):
    """বিভিন্ন ফরম্যাটের তারিখ পার্স করে datetime object বের করে"""
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized: {date_str}")

def calculate_leave_balance(join_date_str, current_date_str, enjoyed_leave):
    """Annual leave balance calculator"""
    join_date = parse_date(join_date_str)
    current_date = parse_date(current_date_str)
    # প্রতিটি বছরের জন্য হিসাব
    total_days_worked = (current_date - join_date).days
    # ১৮ দিন কাজে ১ দিন লিভ (ডকুমেন্ট থেকে পাওয়া নিয়ম)
    leave_earned = total_days_worked // 18
    balance = leave_earned - enjoyed_leave
    return balance

# অন্যান্য ক্যালকুলেশন ফাংশন এখানে যোগ করা যাবে