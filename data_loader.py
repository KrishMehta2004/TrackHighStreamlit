import streamlit as st
import polars as pl
# import pandas as pd

@st.cache_data
def load_data():
    """Load and preprocess the data"""
    try:
        # url = "https://raw.githubusercontent.com/KrishMehta2004/TrackHigh_Data/refs/heads/main/Data.csv"
        # df = pl.read_csv(url)

        df = pl.read_csv("demo.csv")

        df = df.with_columns([
            # Convert date column
            pl.col("Today's Date").str.to_datetime(format="%d-%b-%y", strict=False),
            # Calculate returns
            ((pl.col("LATESTPRICE") - pl.col("ltp")) * 100 / pl.col("ltp")).round(2).alias("Returns"),
            # Clean and convert P/E Ratio
            pl.col("P/E Ratio").str.replace("Book Value", "").cast(pl.Float64, strict=False)
        ])

        df = df.with_columns(
            pl.col("Today's Date").dt.strftime('%B %Y').alias("Month")
        )

        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pl.DataFrame()