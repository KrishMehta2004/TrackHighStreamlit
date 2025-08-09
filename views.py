import streamlit as st
import polars as pl
from datetime import datetime
import plotly.graph_objects as go

from data_processing import get_stock_highs
from components import create_stock_card, create_industry_chart
from utilities import format_number, format_metric_value

def apply_sorting(data, sort_option):
    """Apply sorting based on the selected option"""
    if sort_option == "None":
        return data
    elif sort_option == "Returns (High to Low)":
        # Sort by Returns column in descending order if it exists
        if 'Returns' in data.columns:
            return data.sort('Returns', descending=True, nulls_last=True)
    elif sort_option == "Days Since New High (High to low)":
        # Sort by Days Since High column
        if 'Days Since High' in data.columns:
            return data.sort('Days Since High', descending=True, nulls_last=True)
        
    elif sort_option == "Mcap (low to high)":
        if 'Market Cap' in data.columns:
            return data.sort('Market Cap', descending=False, nulls_last=True)
        
    elif sort_option == "P/E (low to high)":
        if 'P/E Ratio' in data.columns:
            return data.sort('P/E Ratio', descending=False, nulls_last=True)
    return data

def render_specific_date_view(filtered_data, date_display, sort_option):
    """Render the specific date view"""
    if filtered_data.height > 0:
        # Calculate returns if needed
        # filtered_data = calculate_returns(filtered_data)
        
        st.header(f"Analysis for {date_display}")

        # Metrics row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Stocks", filtered_data['symbol'].n_unique())
        with col2:
            st.metric("Total Sectors", filtered_data['Industry'].n_unique())
        with col3:
            # Use Returns for average change if available
            if 'Returns' in filtered_data.columns:
                avg_change = filtered_data['Returns'].mean()
            else:
                avg_change = filtered_data['pChange'].mean()
            st.metric("Average Change", f"{avg_change:+.2f}%")
        
        st.plotly_chart(create_industry_chart(filtered_data), use_container_width=True)

        filtered_data = apply_sorting(filtered_data, sort_option)

        for row in filtered_data.iter_rows(named = 'True'):
            create_stock_card(row)

    else:
        st.warning("No data found for the selected filters.")

def render_search_stock_view(data, search_symbol):
    """Render the search stock view with modern futuristic styling"""
    if search_symbol:
        # Title with stock symbol and current metrics
        st.markdown(f"""
            <div style='background-color: rgba(17, 24, 39, 0.7); padding: 20px; border-radius: 10px; margin-bottom: 25px'>
                <h2 style='margin: 0; color: #00FFFF'>{search_symbol} Analysis</h2>
            </div>
        """, unsafe_allow_html=True)
        
        high_dates = data
        if not data.height == 0:
            # Key metrics in a clean layout
            # highest_price = data['ltp'].max()
            # metrics_container = st.container()
            # with metrics_container:
            #     col1, col2, col3 = st.columns(3)
            #     with col1:
            #         st.metric(
            #             "52-Week High",
            #             format_number(highest_price),
            #             delta=None
            #         )
            #     with col3:
            #         st.metric(
            #             "High Points Found",
            #             f"{len(high_dates)} dates" if not high_dates.is_empty() else "0"
            #         )
                    
            # High points table with enhanced styling
            if not high_dates.is_empty():
                # Add the same CSS styling as the month view
                st.markdown("""
                    <style>
                        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
                        
                        /* Modern search table container */
                        .modern-search-container {
                            background: linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#334155 100%);
                            border-radius: 20px;
                            padding: 0;
                            margin: 20px 0;
                            box-shadow: 
                                0 20px 25px -5px rgba(0, 0, 0, 0.4),
                                0 10px 10px -5px rgba(0, 0, 0, 0.3),
                                inset 0 1px 0 rgba(255, 255, 255, 0.1);
                            border: 1px solid rgba(14, 165, 233, 0.3);
                            overflow: hidden;
                        }
                        
                        /* Search table header */
                        .search-table-header {
                            padding: 25px 30px;
                            position: relative;
                            overflow: hidden;
                            background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
                        }
                        
                        .search-table-header::before {
                            content: '';
                            position: absolute;
                            top: 0;
                            left: 0;
                            right: 0;
                            bottom: 0;
                            background: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%2300ffff' fill-opacity='0.03'%3E%3Cpath d='M20 20l10-10v20l-10-10zm-10 0L0 10v20l10-10z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
                            pointer-events: none;
                        }
                        
                        .search-table-title {
                            color: #00FFFF;
                            font-size: 24px;
                            font-weight: 600;
                            margin: 0;
                            font-family: 'Inter', sans-serif;
                            text-shadow: 0 2px 4px rgba(0, 255, 255, 0.3);
                            position: relative;
                            z-index: 1;
                            letter-spacing: -0.5px;
                        }
                        
                        .search-table-subtitle {
                            color: rgba(0, 255, 255, 0.7);
                            font-size: 16px;
                            margin: 8px 0 0 0;
                            font-family: 'Inter', sans-serif;
                            position: relative;
                            z-index: 1;
                        }
                        
                        /* Search table styling */
                        .search-stock-table {
                            width: 100%;
                            border-collapse: separate;
                            border-spacing: 0;
                            font-family: 'Inter', sans-serif;
                            border-radius: 20px; 
                            overflow: hidden;
                            background: transparent;
                        }
                        
                        /* Search table header */
                        .search-stock-table thead th {
                            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                            color: #00FFFF;
                            font-weight: 600;
                            padding: 20px 20px;
                            text-align: left;
                            font-size: 16px;
                            letter-spacing: 1px;
                            text-transform: uppercase;
                            border: none;
                            border-bottom: 2px solid #0ea5e9;
                            position: relative;
                        }
                        
                        .search-stock-table thead th::after {
                            content: '';
                            position: absolute;
                            bottom: -2px;
                            left: 0;
                            width: 100%;
                            height: 1.5px;
                            background: linear-gradient(90deg, transparent 0%, #00FFFF 50%, transparent 100%);
                            animation: searchShimmer 3s ease-in-out infinite;
                        }
                        
                        @keyframes searchShimmer {
                            0%, 100% { opacity: 0.5; }
                            50% { opacity: 1; }
                        }
                        
                        /* Search table rows */
                        .search-stock-table tbody tr {
                            background: rgba(15, 23, 42, 0.6);
                            backdrop-filter: blur(5px);
                            border-bottom: 1px solid rgba(0, 255, 255, 0.1);
                            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                            position: relative;
                        }
                        
                        .search-stock-table tbody tr:nth-child(even) {
                            background: rgba(30, 41, 59, 0.4);
                        }
                        
                        .search-stock-table tbody tr:hover {
                            background: linear-gradient(135deg, rgba(14, 165, 233, 0.3) 0%, rgba(6, 182, 212, 0.3) 100%);
                            transform: translateX(8px);
                            border-left: 3px solid #00FFFF;
                            box-shadow: 0 8px 20px rgba(0, 255, 255, 0.4);
                        }
                        
                        /* Search table cells */
                        .search-stock-table tbody td {
                            padding: 20px 25px;
                            color: #e2e8f0;
                            border: none;
                            font-size: 15px;
                            vertical-align: middle;
                        }
                        
                        /* Date styling for search table */
                        .date-badge {
                            background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
                            color: white;
                            padding: 10px 16px;
                            border-radius: 12px;
                            font-weight: 600;
                            font-size: 14px;
                            display: inline-flex;
                            align-items: center;
                            gap: 8px;
                            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
                            border: 1px solid rgba(14, 165, 233, 0.6);
                            min-width: 140px;
                            justify-content: center;
                        }
                        
                        /* Price styling for search table */
                        .price-display {
                            background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
                            color: #22c55e;
                            border: 1px solid rgba(34, 197, 94, 0.4);
                            padding: 12px 20px;
                            border-radius: 10px;
                            font-size: 16px;
                            font-weight: 700;
                            text-align: center;
                            backdrop-filter: blur(5px);
                            min-width: 120px;
                        }
                        
                        /* Change styling for search table */
                        .change-positive-search {
                            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                            color: white;
                            padding: 10px 16px;
                            border-radius: 12px;
                            font-weight: 700;
                            font-size: 14px;
                            display: inline-flex;
                            align-items: center;
                            gap: 8px;
                            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
                            border: 1px solid rgba(16, 185, 129, 0.6);
                            min-width: 100px;
                            justify-content: center;
                        }
                        
                        .change-negative-search {
                            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                            color: white;
                            padding: 10px 16px;
                            border-radius: 12px;
                            font-weight: 700;
                            font-size: 14px;
                            display: inline-flex;
                            align-items: center;
                            gap: 8px;
                            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
                            border: 1px solid rgba(239, 68, 68, 0.6);
                            min-width: 100px;
                            justify-content: center;
                        }
                        
                        .change-neutral-search {
                            background: linear-gradient(135deg, rgba(100, 116, 139, 0.3) 0%, rgba(71, 85, 105, 0.3) 100%);
                            color: #94a3b8;
                            padding: 10px 16px;
                            border-radius: 12px;
                            font-weight: 600;
                            font-size: 14px;
                            display: inline-flex;
                            align-items: center;
                            gap: 8px;
                            border: 1px solid rgba(100, 116, 139, 0.4);
                            min-width: 100px;
                            justify-content: center;
                        }
                        
                        /* Responsive design for search table */
                        @media (max-width: 768px) {
                            .search-table-title { font-size: 20px; }
                            .search-stock-table { font-size: 13px; }
                            .search-stock-table tbody td { padding: 15px 12px; }
                            .date-badge, .price-display, .change-positive-search, .change-negative-search { 
                                font-size: 12px; 
                                padding: 8px 12px; 
                                min-width: 80px;
                            }
                        }
                    </style>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📊 High Points Timeline")
                
                # Modern container for the search table
                st.markdown("""
                    <div class="modern-search-container">
                        <div class="search-table-header">
                            <h3 class="search-table-title">Stock Performance Timeline</h3>
                            <p class="search-table-subtitle">Historical high points and price movements</p>
                        </div>
                """, unsafe_allow_html=True)
                
                display_df = high_dates.sort("Today's Date", descending=True)
               
                # Enhanced data preparation - convert to pandas for display
                display_pandas = display_df.to_pandas()
                
                # Create futuristic HTML table for search results
                def create_search_table_html(df):
                    html = '<table class="search-stock-table">'
                    
                    # Header
                    html += '<thead><tr>'
                    html += '<th>📅 Date</th>'
                    html += '<th>Stock Price</th>'
                    html += '<th>Returns</th>'
                    html += '</tr></thead>'
                    
                    # Body
                    html += '<tbody>'
                    for _, row in df.iterrows():
                        html += '<tr>'
                        
                        # Date with enhanced styling
                        date_str = row["Today's Date"].strftime('%d %B %Y')
                        date_html = f'<span class="date-badge">📅 {date_str}</span>'
                        html += f'<td>{date_html}</td>'
                        
                        # Price with modern styling
                        price_formatted = format_number(row['ltp'])
                        price_html = f'<span class="price-display">₹ {price_formatted}</span>'
                        html += f'<td>{price_html}</td>'
                        
                        # Change with enhanced styling
                        if 'Returns' in df.columns:
                            change_value = row['Returns']
                            
                        if change_value is not None and not pl.DataFrame({'x': [change_value]})['x'].is_null().item():
                            if change_value > 0:
                                change_html = f'<span class="change-positive-search">📈 +{change_value:.2f}%</span>'
                            elif change_value < 0:
                                change_html = f'<span class="change-negative-search">📉 {change_value:.2f}%</span>'
                            else:
                                change_html = f'<span class="change-neutral-search">➖ {change_value:.2f}%</span>'
                        else:
                            change_html = '<span class="change-neutral-search">❓ N/A</span>'
                        
                        html += f'<td>{change_html}</td>'
                        html += '</tr>'
                    
                    html += '</tbody></table></div>'
                    return html
                
                # Display the futuristic search table
                table_html = create_search_table_html(display_pandas)
                st.markdown(table_html, unsafe_allow_html=True)
                
        else:
            st.warning(f"No data found for symbol {search_symbol}")
       
    else:
        st.info("Please select one or more stock symbols to view their analysis")

def render_month_view(filtered_data, date_display, sort_option):
    """Render the month view"""
    if not filtered_data.is_empty():

        st.header(f"Analysis for {date_display}")
        
        # Metrics row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Stocks", filtered_data['symbol'].n_unique())
        with col2:
            st.metric("Total Sectors", filtered_data['Industry'].n_unique())
        with col3:
            # Use Returns for average change if available
            if 'Returns' in filtered_data.columns:
                avg_change = filtered_data['Returns'].mean()
            else:
                avg_change = filtered_data['Pchange'].mean()
            st.metric("Average Change", f"{avg_change:+.2f}%")
        
        # Sector chart - full width
        st.plotly_chart(create_industry_chart(filtered_data), use_container_width=True)
        
        st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
                
                /* Remove default streamlit styling */
                .stRadio > div {
                    background: none !important;
                }
                
                /* Main container with dark theme */
                .modern-stock-container {
                    background: linear-gradient(90deg,#0e7490 0%,#1e3a8a 50%,#4338ca 100%);
                    border-radius: 20px;
                    padding: 0;
                    margin: 20px 0;
                    box-shadow: 
                        0 20px 25px -5px rgba(0, 0, 0, 0.3),
                        0 10px 10px -5px rgba(0, 0, 0, 0.2),
                        inset 0 1px 0 rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    overflow: hidden;
                }
                
                /* Header section */
                .table-header {

                    padding: 25px 30px;
                    position: relative;
                    overflow: hidden;
                }
                
                .table-header::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
                    pointer-events: none;
                }
                
                .table-title {
                    color: white;
                    font-size: 24px;
                    font-weight: 600;
                    margin: 0;
                    font-family: 'Inter', sans-serif;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                    position: relative;
                    z-index: 1;
                    letter-spacing: -0.5px;
                }
                
                .table-subtitle {
                    color: rgba(255, 255, 255, 0.8);
                    font-size: 16px;
                    margin: 8px 0 0 0;
                    font-family: 'Inter', sans-serif;
                    position: relative;
                    z-index: 1;
                }
                
                /* Modern table styling */
                .futuristic-table {
                    width: 100%;
                    border-collapse: separate;
                    border-spacing: 0;
                    font-family: 'Inter', sans-serif;
                    border-radius: 20px; 
                    overflow: hidden;
                    background: transparent;
                }
                
                /* Table header */
                .futuristic-table thead th {
                    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                    color: #f1f5f9;
                    font-weight: 600;
                    padding: 20px 20px;
                    text-align: left;
                    font-size: 17px;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                    border: none;
                    border-bottom: 2px solid #6366f1;
                    position: relative;
                }
                
                .futuristic-table thead th::after {
                    content: '';
                    position: absolute;
                    bottom: -2px;
                    left: 0;
                    width: 100%;
                    height: 1.5px;
                    background: linear-gradient(90deg, transparent 0%, #6366f1 50%, transparent 100%);
                    animation: shimmer 3s ease-in-out infinite;
                }
                
                @keyframes shimmer {
                    0%, 100% { opacity: 0.5; }
                    50% { opacity: 1; }
                }
                
                /* Table rows */
                .futuristic-table tbody tr {
                    background: rgba(30, 41, 59, 0.4);
                    backdrop-filter: blur(5px);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    position: relative;
                }
                
                .futuristic-table tbody tr:nth-child(even) {
                    background: rgba(51, 65, 85, 0.3);
                }
                
                .futuristic-table tbody tr:hover {
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
                    transform: translateX(5px);
                    border-left: 3px solid #6366f1;
                    box-shadow: 0 5px 15px rgba(99, 102, 241, 0.3);
                }
                
                /* Table cells */
                .futuristic-table tbody td {
                    padding: 18px 25px;
                    color: #e2e8f0;
                    border: none;
                    font-size: 15px;
                    vertical-align: middle;
                }
                
                /* Stock symbol styling */
                .stock-symbol {
                    color: #60a5fa;
                    font-weight: 700;
                    font-size: 16px;
                    text-decoration: none;
                    padding: 8px 16px;
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
                    border: 1px solid rgba(99, 102, 241, 0.3);
                    border-radius: 8px;
                    transition: all 0.3s ease;
                    display: inline-block;
                    position: relative;
                    overflow: hidden;
                }
                
                .stock-symbol::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
                    transition: left 0.5s;
                }
                
                .stock-symbol:hover {
                    color: #ffffff;
                    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
                    border-color: #a855f7;
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4);
                    text-decoration: none;
                }
                
                .stock-symbol:hover::before {
                    left: 100%;
                }
                
                /* Frequency counter */
                .frequency-counter {
                    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                    color: #e2e8f0;
                    border: 1px solid rgba(99, 102, 241, 0.3);
                    padding: 8px 16px;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 16px;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    min-width: 50px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
                }
                
                /* Returns styling */
                .returns-positive {
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    color: white;
                    padding: 10px 16px;
                    border-radius: 12px;
                    font-weight: 700;
                    font-size: 13px;
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
                    border: 1px solid rgba(16, 185, 129, 0.6);
                }
                
                .returns-negative {
                    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                    color: white;
                    padding: 10px 16px;
                    border-radius: 12px;
                    font-weight: 700;
                    font-size: 12px;
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
                    border: 1px solid rgba(239, 68, 68, 0.6);
                }
                
                /* Series and sector styling */
                .series-badge {
                    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 16px;
                    font-size: 11px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
                }
                
                .sector-tag {
                    background: linear-gradient(135deg, rgba(251, 146, 60, 0.2) 0%, rgba(251, 146, 60, 0.1) 100%);
                    color: #fb923c;
                    border: 1px solid rgba(251, 146, 60, 0.3);
                    padding: 8px 14px;
                    border-radius: 20px;
                    font-size: 16px;
                    font-weight: 600;
                    text-transform: capitalize;
                    backdrop-filter: blur(5px);
                }
                
                /* Responsive design */
                @media (max-width: 768px) {
                    .table-title { font-size: 24px; }
                    .futuristic-table { font-size: 13px; }
                    .futuristic-table tbody td { padding: 12px 15px; }
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Stock occurrences table with new modern design
        st.markdown("""
            <div class="modern-stock-container">
                <div class="table-header">
                    <h2 class="table-title">Most Frequent Stocks</h2>
                    <p class="table-subtitle">High-performance stocks with frequent appearances</p>
                </div>
        """, unsafe_allow_html=True)
        
        # Count unique dates for each stock symbol
        stock_occurrences = (filtered_data
                           .group_by('symbol')
                           .agg(pl.col("Today's Date").n_unique().alias('Occurrences')))
        
        # Calculate max returns for each stock using 'Returns' column
        if 'Returns' in filtered_data.columns:
            max_returns = (filtered_data
                         .group_by('symbol')
                         .agg(pl.col('Returns').max().alias('Max Returns')))
        else:
            # Fallback to %chng if Returns doesn't exist
            if '%chng' in filtered_data.columns:
                max_returns = (filtered_data
                             .group_by('symbol')
                             .agg(pl.col('%chng').max().alias('Max Returns')))
            else:
                # Create empty dataframe with required columns if both don't exist
                unique_symbols = filtered_data.select(pl.col('symbol').unique())
                max_returns = unique_symbols.with_columns(pl.lit(0).alias('Max Returns'))
        
        # Get additional information for each stock
        stock_info = (filtered_data
                     .group_by('symbol')
                     .agg([
                         pl.col('Series Type').first(),
                         pl.col('Industry').first()
                     ]))
        
        # Merge occurrences with stock info and returns
        stock_table = (stock_occurrences
                      .join(stock_info, on='symbol', how='left')
                      .join(max_returns, on='symbol', how='left'))
        
        # Sort controls in the container
        # st.markdown('<div class="sort-controls">', unsafe_allow_html=True)
        # sort_option = st.radio(
        #     "Sort by Performance Metric:",
        #     ["Returns (High to Low)", "Occurrences (High to Low)"],
        #     horizontal=True
        # )
        # st.markdown('</div>', unsafe_allow_html=True)
        
        if sort_option == "Returns (High to Low)":
            stock_table = stock_table.sort('Max Returns', descending=True, nulls_last = True)
        else:  # Default to Occurrences
            stock_table = stock_table.sort('Occurrences', descending=True, nulls_last = True)
        
        # Convert to pandas for HTML table generation
        stock_table_pandas = stock_table.to_pandas()
        
        # Create futuristic HTML table
        def create_futuristic_table_html(df):
            html = '<table class="futuristic-table">'
            
            # Header
            html += '<thead><tr>'
            html += '<th>Symbol</th>'
            html += '<th>Sector</th>'
            html += '<th>Returns</th>'
            html += '<th>Series</th>'
            html += '<th>Count</th>'
            html += '</tr></thead>'
            
            # Body
            html += '<tbody>'
            for _, row in df.iterrows():
                html += '<tr>'
                
                # Symbol with enhanced link
                symbol_link = f'<a href="https://www.screener.in/company/{row["symbol"]}" target="_blank" class="stock-symbol">{row["symbol"]}</a>'
                html += f'<td>{symbol_link}</td>'

                # Sector with modern tag
                sector_tag = f'<span class="sector-tag">{row["Industry"]}</span>'
                html += f'<td>{sector_tag}</td>'
                
                # Returns with enhanced styling
                if not pl.DataFrame({'x': [row['Max Returns']]})['x'].is_null().item():
                    returns_value = row['Max Returns']
                    if returns_value > 0:
                        returns_html = f'<span class="returns-positive">+{returns_value:.2f}%</span>'
                    else:
                        returns_html = f'<span class="returns-negative">{returns_value:.2f}%</span>'
                else:
                    returns_html = '<span style="color: #64748b;">—</span>'
                html += f'<td>{returns_html}</td>'
                
                # Series Type with badge
                series_badge = f'<span class="series-badge">{row["Series Type"]}</span>'
                html += f'<td>{series_badge}</td>'
                
                # Frequency with fire animation
                frequency_badge = f'<span class="frequency-counter">{row["Occurrences"]}</span>'
                html += f'<td>{frequency_badge}</td>'

                
                html += '</tr>'
            
            html += '</tbody></table></div>'
            return html
        
        # Display the futuristic table
        table_html = create_futuristic_table_html(stock_table_pandas)
        st.markdown(table_html, unsafe_allow_html=True)
        
    else:
        st.warning(f"No data found for {date_display}")

def render_date_range_view(filtered_data, date_display, sort_option):
    """Render the month view"""
    if not filtered_data.is_empty():

        st.header(f"Analysis for {date_display}")
        
        # Metrics row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Stocks", filtered_data['symbol'].n_unique())
        with col2:
            st.metric("Total Sectors", filtered_data['Industry'].n_unique())
        with col3:
            # Use Returns for average change if available
            if 'Returns' in filtered_data.columns:
                avg_change = filtered_data['Returns'].mean()
            else:
                avg_change = filtered_data['Pchange'].mean()
            st.metric("Average Change", f"{avg_change:+.2f}%")
        
        # Sector chart - full width
        st.plotly_chart(create_industry_chart(filtered_data), use_container_width=True)
        
        st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
                
                /* Remove default streamlit styling */
                .stRadio > div {
                    background: none !important;
                }
                
                /* Main container with dark theme */
                .modern-stock-container {
                    background: linear-gradient(90deg,#0e7490 0%,#1e3a8a 50%,#4338ca 100%);
                    border-radius: 20px;
                    padding: 0;
                    margin: 20px 0;
                    box-shadow: 
                        0 20px 25px -5px rgba(0, 0, 0, 0.3),
                        0 10px 10px -5px rgba(0, 0, 0, 0.2),
                        inset 0 1px 0 rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    overflow: hidden;
                }
                
                /* Header section */
                .table-header {

                    padding: 25px 30px;
                    position: relative;
                    overflow: hidden;
                }
                
                .table-header::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
                    pointer-events: none;
                }
                
                .table-title {
                    color: white;
                    font-size: 24px;
                    font-weight: 600;
                    margin: 0;
                    font-family: 'Inter', sans-serif;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                    position: relative;
                    z-index: 1;
                    letter-spacing: -0.5px;
                }
                
                .table-subtitle {
                    color: rgba(255, 255, 255, 0.8);
                    font-size: 16px;
                    margin: 8px 0 0 0;
                    font-family: 'Inter', sans-serif;
                    position: relative;
                    z-index: 1;
                }
                
                /* Modern table styling */
                .futuristic-table {
                    width: 100%;
                    border-collapse: separate;
                    border-spacing: 0;
                    font-family: 'Inter', sans-serif;
                    border-radius: 20px; 
                    overflow: hidden;
                    background: transparent;
                }
                
                /* Table header */
                .futuristic-table thead th {
                    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                    color: #f1f5f9;
                    font-weight: 600;
                    padding: 20px 20px;
                    text-align: left;
                    font-size: 17px;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                    border: none;
                    border-bottom: 2px solid #6366f1;
                    position: relative;
                }
                
                .futuristic-table thead th::after {
                    content: '';
                    position: absolute;
                    bottom: -2px;
                    left: 0;
                    width: 100%;
                    height: 1.5px;
                    background: linear-gradient(90deg, transparent 0%, #6366f1 50%, transparent 100%);
                    animation: shimmer 3s ease-in-out infinite;
                }
                
                @keyframes shimmer {
                    0%, 100% { opacity: 0.5; }
                    50% { opacity: 1; }
                }
                
                /* Table rows */
                .futuristic-table tbody tr {
                    background: rgba(30, 41, 59, 0.4);
                    backdrop-filter: blur(5px);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    position: relative;
                }
                
                .futuristic-table tbody tr:nth-child(even) {
                    background: rgba(51, 65, 85, 0.3);
                }
                
                .futuristic-table tbody tr:hover {
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
                    transform: translateX(5px);
                    border-left: 3px solid #6366f1;
                    box-shadow: 0 5px 15px rgba(99, 102, 241, 0.3);
                }
                
                /* Table cells */
                .futuristic-table tbody td {
                    padding: 18px 25px;
                    color: #e2e8f0;
                    border: none;
                    font-size: 15px;
                    vertical-align: middle;
                }
                
                /* Stock symbol styling */
                .stock-symbol {
                    color: #60a5fa;
                    font-weight: 700;
                    font-size: 16px;
                    text-decoration: none;
                    padding: 8px 16px;
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
                    border: 1px solid rgba(99, 102, 241, 0.3);
                    border-radius: 8px;
                    transition: all 0.3s ease;
                    display: inline-block;
                    position: relative;
                    overflow: hidden;
                }
                
                .stock-symbol::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
                    transition: left 0.5s;
                }
                
                .stock-symbol:hover {
                    color: #ffffff;
                    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
                    border-color: #a855f7;
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4);
                    text-decoration: none;
                }
                
                .stock-symbol:hover::before {
                    left: 100%;
                }
                
                /* Frequency counter */
                .frequency-counter {
                    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                    color: #e2e8f0;
                    border: 1px solid rgba(99, 102, 241, 0.3);
                    padding: 8px 16px;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 16px;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    min-width: 50px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
                }
                
                /* Returns styling */
                .returns-positive {
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    color: white;
                    padding: 10px 16px;
                    border-radius: 12px;
                    font-weight: 700;
                    font-size: 13px;
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
                    border: 1px solid rgba(16, 185, 129, 0.6);
                }
                
                .returns-negative {
                    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                    color: white;
                    padding: 10px 16px;
                    border-radius: 12px;
                    font-weight: 700;
                    font-size: 12px;
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
                    border: 1px solid rgba(239, 68, 68, 0.6);
                }
                
                /* Series and sector styling */
                .series-badge {
                    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 16px;
                    font-size: 11px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
                }
                
                .sector-tag {
                    background: linear-gradient(135deg, rgba(251, 146, 60, 0.2) 0%, rgba(251, 146, 60, 0.1) 100%);
                    color: #fb923c;
                    border: 1px solid rgba(251, 146, 60, 0.3);
                    padding: 8px 14px;
                    border-radius: 20px;
                    font-size: 16px;
                    font-weight: 600;
                    text-transform: capitalize;
                    backdrop-filter: blur(5px);
                }
                
                /* Responsive design */
                @media (max-width: 768px) {
                    .table-title { font-size: 24px; }
                    .futuristic-table { font-size: 13px; }
                    .futuristic-table tbody td { padding: 12px 15px; }
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Stock occurrences table with new modern design
        st.markdown("""
            <div class="modern-stock-container">
                <div class="table-header">
                    <h2 class="table-title">Most Frequent Stocks</h2>
                    <p class="table-subtitle">High-performance stocks with frequent appearances</p>
                </div>
        """, unsafe_allow_html=True)
        
        # Count unique dates for each stock symbol
        stock_occurrences = (filtered_data
                           .group_by('symbol')
                           .agg(pl.col("Today's Date").n_unique().alias('Occurrences')))
        
        # Calculate max returns for each stock using 'Returns' column
        if 'Returns' in filtered_data.columns:
            max_returns = (filtered_data
                         .group_by('symbol')
                         .agg(pl.col('Returns').max().alias('Max Returns')))
        else:
            # Fallback to %chng if Returns doesn't exist
            if '%chng' in filtered_data.columns:
                max_returns = (filtered_data
                             .group_by('symbol')
                             .agg(pl.col('%chng').max().alias('Max Returns')))
            else:
                # Create empty dataframe with required columns if both don't exist
                unique_symbols = filtered_data.select(pl.col('symbol').unique())
                max_returns = unique_symbols.with_columns(pl.lit(0).alias('Max Returns'))
        
        # Get additional information for each stock
        stock_info = (filtered_data
                     .group_by('symbol')
                     .agg([
                         pl.col('Series Type').first(),
                         pl.col('Industry').first()
                     ]))
        
        # Merge occurrences with stock info and returns
        stock_table = (stock_occurrences
                      .join(stock_info, on='symbol', how='left')
                      .join(max_returns, on='symbol', how='left'))
        
        # Sort controls in the container
        # st.markdown('<div class="sort-controls">', unsafe_allow_html=True)
        # sort_option = st.radio(
        #     "Sort by Performance Metric:",
        #     ["Returns (High to Low)", "Occurrences (High to Low)"],
        #     horizontal=True
        # )
        # st.markdown('</div>', unsafe_allow_html=True)
        
        if sort_option == "Returns (High to Low)":
            stock_table = stock_table.sort('Max Returns', descending=True, nulls_last = True)
        else:  # Default to Occurrences
            stock_table = stock_table.sort('Occurrences', descending=True, nulls_last = True)
        
        # Convert to pandas for HTML table generation
        stock_table_pandas = stock_table.to_pandas()
        
        # Create futuristic HTML table
        def create_futuristic_table_html(df):
            html = '<table class="futuristic-table">'
            
            # Header
            html += '<thead><tr>'
            html += '<th>Symbol</th>'
            html += '<th>Sector</th>'
            html += '<th>Returns</th>'
            html += '<th>Series</th>'
            html += '<th>Count</th>'
            html += '</tr></thead>'
            
            # Body
            html += '<tbody>'
            for _, row in df.iterrows():
                html += '<tr>'
                
                # Symbol with enhanced link
                symbol_link = f'<a href="https://www.screener.in/company/{row["symbol"]}" target="_blank" class="stock-symbol">{row["symbol"]}</a>'
                html += f'<td>{symbol_link}</td>'

                # Sector with modern tag
                sector_tag = f'<span class="sector-tag">{row["Industry"]}</span>'
                html += f'<td>{sector_tag}</td>'
                
                # Returns with enhanced styling
                if not pl.DataFrame({'x': [row['Max Returns']]})['x'].is_null().item():
                    returns_value = row['Max Returns']
                    if returns_value > 0:
                        returns_html = f'<span class="returns-positive">+{returns_value:.2f}%</span>'
                    else:
                        returns_html = f'<span class="returns-negative">{returns_value:.2f}%</span>'
                else:
                    returns_html = '<span style="color: #64748b;">—</span>'
                html += f'<td>{returns_html}</td>'
                
                # Series Type with badge
                series_badge = f'<span class="series-badge">{row["Series Type"]}</span>'
                html += f'<td>{series_badge}</td>'
                
                # Frequency with fire animation
                frequency_badge = f'<span class="frequency-counter">{row["Occurrences"]}</span>'
                html += f'<td>{frequency_badge}</td>'

                
                html += '</tr>'
            
            html += '</tbody></table></div>'
            return html
        
        # Display the futuristic table
        table_html = create_futuristic_table_html(stock_table_pandas)
        st.markdown(table_html, unsafe_allow_html=True)
        
    else:
        st.warning(f"No data found for {date_display}")