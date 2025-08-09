import polars as pl
import streamlit as st
from datetime import datetime, timedelta
import numpy as np

# def get_stock_highs(data, symbol):
#     """Get all dates when a stock hit new 52-week highs"""
#     stock_data = data[data['symbol'] == symbol]
    
#     if stock_data.height == 0:
#         return pl.DataFrame(), stock_data
    
#     # Sort by date
#     # stock_data = stock_data.sort_values(by="Today's Date")
#     stock_data = stock_data.sort("Today's Date", descending=True, nulls_last=True)
    
#     # Get high dates
#     high_dates = pl.DataFrame()
    
#     for idx, row in stock_data.iterrows():
#         # Consider this a high date if it exists in our data
#         if row['High52W'] == 'Yes':
#             high_dates = pl.concat([high_dates, pl.DataFrame([row])])
    
#     return high_dates, stock_data

def get_stock_highs(data: pl.DataFrame, search_symbol: str) -> tuple[pl.DataFrame, pl.DataFrame]:
    """
    Get all dates when a stock hit new 52-week highs (Polars version).
    Returns:
        (high_dates, stock_data) — both as Polars DataFrames
    """
    # Filter by symbol
    # stock_data = data.filter(pl.col("symbol") == search_symbol)

    if data.height == 0:
        return pl.DataFrame(), data

    # Sort by date (descending)
    stock_data = data.sort("Today's Date", descending=True, nulls_last=True)


    high_dates = pl.DataFrame()
    print(high_dates)

    return high_dates, stock_data
