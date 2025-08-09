# import pandas as pd
import polars as pl

def format_metric_value(value, precision=2):
    """Format metric value with proper type checking"""
    try:
        if value is None:
            return "N/A"
        if isinstance(value, str):
            # Try to convert string to float
            value = float(value.replace('₹', '').replace(',', '').strip())
        return f"{value:.{precision}f}"
    except (ValueError, TypeError):
        return "N/A"

def format_number(num):
    """Format numbers with appropriate scale and currency symbol"""
    try:
        if num is None:
            return "N/A"
        if isinstance(num, str):
            num = float(num.replace('₹', '').replace(',', '').strip())
        
        if num >= 1e9:
            return f"₹{num/1e9:.2f}B"
        elif num >= 1e7:
            return f"₹{num/1e7:.2f}Cr"
        elif num >= 1e5:
            return f"₹{num/1e5:.2f}L"
        else:
            return f"₹{num:,.2f}"
    except (ValueError, TypeError):
        return "N/A"