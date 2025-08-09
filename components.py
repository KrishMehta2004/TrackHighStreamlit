import streamlit as st
import plotly.graph_objects as go
from utilities import format_metric_value, format_number
import polars as pl

def create_metric_container(label, value, unit="", color="white", trend=None):
    """Create an enhanced metric container with better typography and colors"""
    trend_color = {
        "up": "#22C55E",
        "down": "#EF4444",
        None: "white"
    }
    
    trend_icon = {
        "up": "↑",
        "down": "↓",
        None: ""
    }
    
    st.markdown(
        f"""
        <div style="background-color: rgba(30, 34, 45, 0.98); padding: 15px; border-radius: 8px; 
                    margin: 8px 0; border: 1px solid rgba(255, 255, 255, 0.1);">
            <div style="color: #A5B4FC; font-size: 13px; font-weight: 500; 
                        letter-spacing: 0.5px; text-transform: uppercase;">{label}</div>
            <div style="color: {color}; font-size: 20px; font-weight: 600; 
                        margin-top: 8px; display: flex; align-items: center;">
                <span style="color: {trend_color[trend]}">
                    {value}{' ' + unit if unit else ''} {trend_icon[trend]}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_stock_card(row):
    """Create a stock card with simple background color based on performance"""
    bg_color = "rgba(255, 255, 255, 0.5)"  # Default background color

    st.markdown(f"""
        <style>
        .stock-card {{
            background-color: {bg_color};
            border-radius: 12px;
            padding: 5px;
            margin-bottom: 24px;
            border: 1px solid rgba(255, 255, 255, 1);
        }}
        .stock-header {{
            display: flex;
            align-items: center;
            margin-bottom: 24px;
        }}
        .stock-title {{
            font-size: 28px;
            font-weight: 700;
            color: #A5B4FC;
        }}
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="stock-card">', unsafe_allow_html=True)
        
        # Header Section
        symbol = row['symbol']
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            # Handle NaN values for Series Type, Sector, and Industry
            # series_type = row.get('Series Type', 'N/A') if pl.notna(row.get('Series Type')) else 'N/A'
            # sector = row.get('Sector', 'N/A') if pl.notna(row.get('Sector')) else 'N/A'
            # industry = row.get('Industry', 'N/A') if pl.notna(row.get('Industry')) else 'N/A'
            series_type = row.get('Series Type', 'N/A') if row.get('Series Type') is not None else 'N/A'
            sector = row.get('Sector', 'N/A') if row.get('Sector') is not None else 'N/A'
            industry = row.get('Industry', 'N/A') if row.get('Industry') is not None else 'N/A'
            
            st.markdown(f"""
            <div class="stock-header">
                <div>
                    <div class="stock-title">
                        <span style="display: flex; align-items: center; gap: 12px;">
                            {symbol} <strong>({series_type})</strong>
                            <a href="https://www.screener.in/company/{symbol}" target="_blank"
                            style="color: #A5B4FC; font-size: 14px; text-decoration: none;">🔍 Screener</a>
                            <a href="https://www.tradingview.com/chart/?symbol=NSE:{symbol}" target="_blank"
                            style="color: #60A5FA; font-size: 14px; text-decoration: none;">📊 TradingView</a>
                        </span>
                    </div>
                    <div>
                        <span style="margin-right: 20px; color: #E2E8F0;">
                            <strong>Sector:</strong> {sector}
                        </span>
                    </div>
                    <div>
                        <span style="color: #E2E8F0;">
                            <strong>Industry:</strong> {industry}     
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        
        with col2:
            # Handle NaN values for price and price_change
            # price = format_number(row['ltp']) if pl.notna(row['ltp']) else 'N/A'
            # price_change = row['pChange'] if pl.notna(row['pChange']) else 0
            price = format_number(row['ltp']) if row['ltp'] is not None else 'N/A'
            price_change = row['pChange'] if row['pChange'] is not None else 0
            price_color = "#22C55E" if price_change >= 0 else "#EF4444"
            date_current = row["Today's Date"].strftime('%d-%b-%y')

            
            # Format the price change display properly
            if row['pChange'] is not None:
                price_change_display = f"{price_change:+.2f}% {' ↑' if price_change >= 0 else ' ↓'}"
            else:
                price_change_display = "N/A"
                
            st.markdown(f"""
                <div style="text-align: right; width: 180%;">
                    <div style="font-size: 30px; font-weight: 700; color: white;">{price}</div>
                    <div style="font-size: 20px; font-weight: 600; color: {price_color};">
                        {price_change_display}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Metrics Grid
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Safely handle potentially missing or NaN values
            # market_cap = format_number(row.get('Market Cap')) if pl.notna(row.get('Market Cap')) else 'N/A'
            
            # days_since_high = format_metric_value(row.get('Days Since High')) if pl.notna(row.get('Days Since High')) else 'N/A'

            market_cap = format_number(row.get('Market Cap')) if row.get('Market Cap') is not None else 'N/A'
            days_since_high = format_metric_value(row.get('Days Since High')) if row.get('Days Since High') is not None else 'N/A'
            
            create_metric_container("Market Cap", market_cap, color="#A5B4FC")
            create_metric_container("Days Since New High", days_since_high, color="#BAE6FD")


        with col2:
            # Safely handle potentially missing or NaN values
            pe_ratio = format_metric_value(row.get('P/E Ratio')) if row.get('P/E Ratio') is not None else 'N/A'
            roe = format_metric_value(row.get('ROE')) if row.get('ROE') is not None else 'N/A'

            
            create_metric_container("Stock P/E", pe_ratio, color="#93C5FD")
            create_metric_container("ROE", roe, unit="%", color="#FDA4AF")

        with col3:
            # Safely handle potentially missing or NaN values
            ltp_1 = format_number(row.get('LATESTPRICE')) if row.get('LATESTPRICE') is not None else 'N/A'
            returns = row.get('Returns') if row.get('Returns') is not None else 'N/A'

            # st.display(df['Latest Price'])

            # Handle display for returns
            if returns is not None:
                # returns_color = "#22C55E" if returns >= 0 else "#EF4444"
                try:
                    returns_value = round(float(returns),2)
                    returns_color = "#22C55E" if returns_value >= 0 else "#EF4444"
                    returns_icon = "↑" if returns_value >= 0 else "↓"

                except ValueError: 
                    returns_color = "#D1D5DB"
                    returns_icon = '↑'  # Gray color for invalid or missing returns

                # returns_icon = "↑" if returns >= 0 else "↓"
                
                returns_display = f'(<span style="color:{returns_color};">{returns}% {returns_icon}</span>)'
            else:
                returns_display = '(N/A)'

            create_metric_container(
                "Latest Price & Returns",
                f'<span style="color:white;">{ltp_1}</span> {returns_display}',
                color="white"
            )

            # Safely handle potentially missing or NaN values
            # roce = format_metric_value(row.get('ROCE')) if pl.notna(row.get('ROCE')) else 'N/A'
            roce = format_metric_value(row.get('ROCE')) if row.get('ROCE') is not None else 'N/A'    
            create_metric_container("ROCE", roce, unit="%")

        # About Section
        if 'About' in row and str(row['About']) != 'nan':
            st.markdown(f"""
                <div style="margin-top: 20px; padding: 16px; background: rgba(30, 41, 59, 0.4); 
                            border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <div style="color: #A5B4FC; font-size: 16px; font-weight: 600; margin-bottom: 8px;">About</div>
                    <div style="color: #FFFFFF; font-size: 20px; line-height: 1.6;">{row['About']}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

def create_sector_chart(filtered_data):
    """Create an enhanced sector distribution chart with proper NaN handling"""
    # Drop NaN values before counting sectors
    sector_counts = filtered_data['Sector'].drop_nulls().value_counts()
    
    if sector_counts.empty:
        # Return empty chart with message if no valid sectors
        fig = go.Figure()
        fig.add_annotation(
            text="No sector data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(color="white", size=16)
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(17, 24, 39, 0.7)',
            plot_bgcolor='rgba(17, 24, 39, 0.7)',
            height=400,
        )
        return fig
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sector_counts.index,
        y=sector_counts.values,
        marker_color='rgb(165, 180, 252)',
        marker_line_color='rgb(129, 140, 248)',
        marker_line_width=1.5,
        opacity=0.8,
        text=sector_counts.values,
        textposition='outside',
        textfont=dict(color='#A5B4FC', size=12)  # Added text styling
    ))
    
    # Calculate the maximum value to set appropriate y-axis range
    max_value = sector_counts.values.max()
    
    fig.update_layout(
        title={
            'text': "Sector Distribution",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24, 'color': '#A5B4FC'}
        },
        xaxis_tickangle=-45,
        template='plotly_dark',
        showlegend=False,
        xaxis_title="Sector",
        yaxis_title="Number of Companies",
        height=400,
        margin=dict(t=100, b=80, l=60, r=40),  # Increased top margin
        paper_bgcolor='rgba(17, 24, 39, 0.7)',
        plot_bgcolor='rgba(17, 24, 39, 0.7)',
        font={'color': '#9CA3AF'},
        xaxis={'gridcolor': 'rgba(255, 255, 255, 0.1)'},
        yaxis={
            'gridcolor': 'rgba(255, 255, 255, 0.1)',
            'range': [0, max_value * 1.2]  # Add 15% padding above highest bar
        },
    )
    
    return fig

def create_industry_chart(filtered_data: pl.DataFrame):
    """Create an enhanced sector distribution chart with proper NaN handling for Polars"""

    # Drop NaN values before counting sectors
    sector_counts = (
        filtered_data
        .select("Industry")
        .drop_nulls()
        .group_by("Industry")
        .count()
        .sort("count", descending=True)
    )

    # If no data after dropping nulls
    if sector_counts.height == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No sector data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(color="white", size=16)
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(17, 24, 39, 0.7)',
            plot_bgcolor='rgba(17, 24, 39, 0.7)',
            height=400,
        )
        return fig

    # Convert Polars DF to Python lists for Plotly
    industries = sector_counts["Industry"].to_list()
    counts = sector_counts["count"].to_list()
    max_value = max(counts)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=industries,
        y=counts,
        marker_color='rgb(165, 180, 252)',
        marker_line_color='rgb(129, 140, 248)',
        marker_line_width=1.5,
        opacity=0.8,
        text=counts,
        textposition='outside',
        textfont=dict(color='#A5B4FC', size=12)
    ))

    fig.update_layout(
        title={
            'text': "Industry Distribution",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24, 'color': '#A5B4FC'}
        },
        xaxis_tickangle=-45,
        template='plotly_dark',
        showlegend=False,
        xaxis_title="Industry",
        yaxis_title="Number of Companies",
        height=400,
        margin=dict(t=100, b=80, l=60, r=40),
        paper_bgcolor='rgba(17, 24, 39, 0.7)',
        plot_bgcolor='rgba(17, 24, 39, 0.7)',
        font={'color': '#9CA3AF'},
        xaxis={'gridcolor': 'rgba(255, 255, 255, 0.1)'},
        yaxis={
            'gridcolor': 'rgba(255, 255, 255, 0.1)',
            'range': [0, max_value * 1.2]
        },
    )

    return fig