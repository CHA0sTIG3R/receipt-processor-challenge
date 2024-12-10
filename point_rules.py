from datetime import datetime, date, time
import math
from typing import Any, Dict, List

# points awarded for each rule
DAY_PURCHASE_ODD_POINTS = 6
TIME_WINDOW_POINTS = 10
PAIR_OF_ITEMS_POINTS = 5
WHOLE_NUMBER_TOTAL_POINTS = 75
DIVISIBLE_BY_QUARTER_POINTS = 25

# time window
START_TIME = time(14, 0)  # 2:00 PM
END_TIME = time(16, 0)    # 4:00 PM

def points_for_retailer_name(retailer: str) -> int:
    """Return points for each alphanumeric character in the retailer name."""
    return sum(1 for char in retailer if char.isalnum())

def points_for_purchase_day(purchase_date: date) -> int:
    """Return points if the purchase day is odd."""
    return DAY_PURCHASE_ODD_POINTS if (purchase_date.day % 2 == 1) else 0

def points_for_purchase_time(purchase_time_str: str) -> int:
    """Return points if the purchase time is between 2:00 PM and 4:00 PM (exclusive)."""
    purchase_time = datetime.strptime(purchase_time_str, '%H:%M:%S').time()
    return TIME_WINDOW_POINTS if START_TIME < purchase_time < END_TIME else 0

def points_for_item_count(items: List[Dict]) -> int:
    """Return points based on the number of items (5 points per pair of items)."""
    return (len(items) // 2) * PAIR_OF_ITEMS_POINTS

def points_for_item_description_length(items: List[Dict[str, str]]) -> int:
    """
    For each item whose description length (after stripping whitespace)
    is divisible by 3, add ceil(item_price * 0.2) points.
    """
    total_points = 0
    for item in items:
        description = item['shortDescription'].strip()
        price = float(item['price'])
        if len(description) % 3 == 0:
            total_points += math.ceil(price * 0.2)
    return total_points

def is_divisible_by_quarter(value: float) -> bool:
    """Check if a float value is divisible by 0.25."""
    # Multiplying by 100 and checking divisibility by 25 avoids floating point issues.
    return (value * 100) % 25 == 0

def points_for_total(total: float) -> int:
    """
    If total is a whole number, add 75 points.
    Else if total is divisible by 0.25, add 25 points.
    """
    if total.is_integer():
        return WHOLE_NUMBER_TOTAL_POINTS
    elif is_divisible_by_quarter(total):
        return DIVISIBLE_BY_QUARTER_POINTS
    return 0

def calculate_points(receipt_data: Dict[str, Any]) -> int:
    """
    Calculate reward points based on certain rules derived from the receipt data.
    """
    items = receipt_data['items']

    # Aggregate points from all rules
    total_points = 0
    print(total_points)
    total_points += points_for_retailer_name(receipt_data['retailer'])
    print(total_points)
    total_points += points_for_purchase_day(receipt_data['purchaseDate'])
    print(total_points)
    total_points += points_for_purchase_time(receipt_data['purchaseTime'])
    print(total_points)
    total_points += points_for_item_count(items)
    print(total_points)
    total_points += points_for_item_description_length(items)
    print(total_points)
    total_points += points_for_total(receipt_data['total'])
    print(total_points)

    return total_points
