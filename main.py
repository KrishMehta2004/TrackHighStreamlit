import streamlit as st
import polars as pl
from datetime import datetime
from data_loader import load_data
from views import (
    render_specific_date_view, 
    render_search_stock_view, 
    render_month_view, 
    render_date_range_view,
    apply_sorting
)

def main():

    st.set_page_config(layout="wide", page_title='TrackHigh | 52 Week High | NSE Stocks |', page_icon="https://img.icons8.com/ios-filled/100/ffffff/line-chart.png", )

    st.markdown("""
        <style>
        /* Unified input, select, date, and multiselect styling */
        .stSelectbox, .stDateInput, .stMultiSelect > div > div {
            background-color: rgba(51, 65, 85, 0.4) !important;
            border: 1px solid rgba(148, 163, 184, 0.1) !important;
            border-radius: 10px !important;
            color: #E2E8F0 !important;
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            padding: 2.5px 8px !important;
            transition: all 0.3s ease !important;
            box-sizing: border-box !important;
        }

        .stSelectbox:hover, .stDateInput:hover, .stMultiSelect > div > div:hover {
            background-color: rgba(61, 75, 95, 0.5) !important;
            border: 1px solid #94a3b8 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
        }

        .stSelectbox:focus-within, .stDateInput:focus-within, .stMultiSelect > div > div:focus-within {
            box-shadow: 0 4px 16px rgba(0,0,0,0.25) !important;
        }

        .stDateInput input, .stSelectbox input, .stMultiSelect input {
            background-color: transparent !important;
            color: #E2E8F0 !important;
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            border: none !important;
            outline: none !important;
        }

        .stDateInput input:hover, .stSelectbox input:hover, .stMultiSelect input:hover {
            background-color: transparent !important;
        }

        .stDateInput input:focus, .stSelectbox input:focus, .stMultiSelect input:focus {
            background-color: transparent !important;
            outline: none !important;
        }

        .stSelectbox label, .stDateInput label, .stMultiSelect label {
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            color: #E2E8F0 !important;
        }

        /* Updated Radio Button Styling - More specific selectors */
        .stRadio > div {
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            color: #E2E8F0 !important;
        }

        /* Target the radio button labels specifically */
        .stRadio > div > label {
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            color: #E2E8F0 !important;
            transition: all 0.3s ease !important;
        }

        /* Target the radio button text spans */
        .stRadio > div > label > div {
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            color: #E2E8F0 !important;
        }

        /* More specific targeting for radio text */
        .stRadio > div > label > div > div {
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            color: #E2E8F0 !important;
        }

        /* Hover effects for radio buttons */
        .stRadio > div > label:hover {
            color: #60A5FA !important;
            transform: scale(1.02) !important;
        }

        .stRadio > div > label:hover > div {
            color: #60A5FA !important;
        }

        .stRadio > div > label:hover > div > div {
            color: #60A5FA !important;
        }

        /* Alternative approach - target all text within radio container */
        div[data-testid="stRadio"] * {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #E2E8F0 !important;
        }

        div[Data-testid="stSelectbox"] * {
            font-size: 1.1rem !important;
        }

        div[Data-testid="stDateInput"] * {
            font-size: 1.1rem !important;
        }

        .dashboard-title {
            font-size: 3rem;
            font-weight: 800;
            color: #f9fafb;
            display: flex;
            align-items: center;
        }

        .css-1d391kg h2 {
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            color: #E2E8F0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="dashboard-title">
            <img src="https://img.icons8.com/ios-filled/100/ffffff/line-chart.png" alt="TrackHigh Logo" style="height: 2.5rem; margin-right: 0.75rem;" />
            52 Week High Dashboard
        </div>
        """, unsafe_allow_html=True)

    st.markdown("Track and view NSE 52-week high stocks.")

    st.info("""
        **Comprehensive Tracking Tool:**
        - Track specific dates or date ranges
        - Track Returns of the stocks
        - Search and monitor individual stocks
    """)

    # Load data
    data = load_data()
    if data.height == 0:
        st.error("No data available for this date")
        return

    # Sidebar for filters
    with st.sidebar:
        st.header("Filters")
        view_type = st.radio(
            "Select View Type",
            ["Specific Date📆", "Month📅", "Date Range⏳", "Search Stock🔎"]
        )

        if view_type == "Specific Date📆":

            selected_date = st.date_input(
                "Select Date",
                data["Today's Date"].max(),
                min_value=data["Today's Date"].min(),
                max_value=data["Today's Date"].max()
            )
            
            filtered_data = data.filter(data["Today's Date"].dt.date() == selected_date)

            available_sectors = ['All'] + sorted(
                filtered_data["Industry"].drop_nulls().unique().to_list()
            )
            available_series = ['All'] + sorted(
                filtered_data['Series Type'].drop_nulls().unique().to_list()
            ) 

            selected_sectors = st.selectbox("Filter by Sector:", available_sectors)
            selected_series = st.selectbox("Filter by Series:", available_series)
            sort_option = st.selectbox("Sort By:", ["None", "Returns (High to Low)", "Mcap (low to high)", "P/E (low to high)", "Days Since New High (High to low)"])
            
            if selected_sectors != 'All':
                filtered_data = filtered_data.filter(filtered_data["Industry"] == selected_sectors)
            if selected_series != 'All':
                filtered_data = filtered_data.filter(filtered_data["Series Type"] == selected_series)

        elif view_type == "Month📅":

            # Get months sorted in chronological order
            months = sorted(
                data["Month"].unique().to_list(),
                key=lambda x: datetime.strptime(x, '%B %Y')
            )

            selected_month = st.selectbox("Select Month", months)

            # Filter data for selected month
            filtered_data = data.filter(
                pl.col("Today's Date").dt.strftime('%B %Y') == selected_month
            )

            # Handle sectors
            sectors = filtered_data["Industry"].drop_nulls().unique().to_list()
            available_sectors = ["All"] + sorted(sectors)
            selected_sectors = st.selectbox("Filter by Sector:", available_sectors)

            # Handle series
            series = filtered_data["Series Type"].drop_nulls().unique().to_list()
            available_series = ["All"] + sorted(series)
            selected_series = st.selectbox("Filter by Series:", available_series)

            sort_option = st.selectbox("Sort By:", ["Returns (High to Low)", "Occurrences (High to Low)"])

            # Apply sector filter
            if selected_sectors != "All":
                filtered_data = filtered_data.filter(
                    pl.col("Industry") == selected_sectors
                )

            # Apply series filter
            if selected_series != "All":
                filtered_data = filtered_data.filter(
                    pl.col("Series Type") == selected_series
                )

            # Apply sorting after filtering
            # filtered_data = apply_sorting(filtered_data, sort_option)

        elif view_type == "Date Range⏳":
            # Convert to Python date objects for Streamlit
            min_date = data["Today's Date"].min().date()
            max_date = data["Today's Date"].max().date()

            start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
            end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

            # Filter data for date range
            filtered_data = data.filter(
                (pl.col("Today's Date").dt.date() >= start_date) &
                (pl.col("Today's Date").dt.date() <= end_date)
            )

            # Handle sectors
            sectors = filtered_data["Industry"].drop_nulls().unique().to_list()
            available_sectors = ["All"] + sorted(sectors)
            selected_sectors = st.selectbox("Filter by Sector:", available_sectors)

            # Handle series
            series = filtered_data["Series Type"].drop_nulls().unique().to_list()
            available_series = ["All"] + sorted(series)
            selected_series = st.selectbox("Filter by Series:", available_series)

            sort_option = st.selectbox("Sort By:", ["Returns (High to Low)", "Occurrences (High to Low)"])

            # Sorting options
            # sort_by = st.selectbox(
            #     "Sort By:",
            #     ["None", "Returns (High to Low)", "Days Since High (Highest First)"]
            # )

            # Apply sector filter
            if selected_sectors != "All":
                filtered_data = filtered_data.filter(
                    pl.col("Industry") == selected_sectors
                )

            # Apply series filter
            if selected_series != "All":
                filtered_data = filtered_data.filter(
                    pl.col("Series Type") == selected_series
                )

        elif view_type == "Search Stock🔎":
            all_symbols = sorted(data['symbol'].unique())
            search_symbol = st.selectbox(
                "Search Stock Symbol",
                options=all_symbols,
                placeholder="Select stock symbols to analyze"
            )

    if view_type == "Specific Date📆":
        render_specific_date_view(filtered_data, selected_date.strftime('%d %B %Y'), sort_option)

    elif view_type == "Month📅":
        render_month_view(filtered_data, selected_month, sort_option)

    elif view_type == "Date Range⏳":
        date_display = f"{start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}"
        render_date_range_view(filtered_data, date_display, sort_option)

    elif view_type == "Search Stock🔎":
        data = data.filter(pl.col("symbol") == search_symbol)
        render_search_stock_view(data, search_symbol)

if __name__ == "__main__":
    main()