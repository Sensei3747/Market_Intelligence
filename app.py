"""
Marketing Intelligence Dashboard
Main Streamlit application
"""

import streamlit as st
import pandas as pd
import sys
import os
from typing import Optional, Tuple, List, Dict, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data.processor import DataProcessor
from visualization.dashboard_components import DashboardComponents
from ai.ai_results import AIInsights

# Configuration constants
PAGE_CONFIG = {
    'page_title': 'Marketing Intelligence Dashboard',
    'page_icon': '📊',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}


st.set_page_config(**PAGE_CONFIG)

# Premium Dashboard CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        font-family: 'Inter', sans-serif;
        color: white;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    /* Main Container */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1400px;
    }
    
    /* Header Styles */
    .main-header {
        background: rgba(15, 32, 39, 0.5); /* Dark, semi-transparent */
        color: #FFFFFF;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(20, 184, 166, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        color: #14B8A6; /* Teal accent */
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
        color: #B0BEC5;
    }
    
    /* Sidebar Styling */
    /* Sidebar header text color fix */
    .css-1d391kg h3 {
        color: #000000 !important;
    }

    /* Alternative selector for sidebar headers */
    .stSidebar h3 {
        color: #000000 !important;
    }

    /* More specific targeting for sidebar markdown headers */
    .stSidebar [data-testid="stMarkdownContainer"] h3 {
        color: #000000 !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15, 32, 39, 0.5);
        border-radius: 15px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        margin: 0 0.25rem;
        transition: all 0.3s ease;
        color: #B0BEC5 !important;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(20, 184, 166, 0.1);
        color: #14B8A6 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #14B8A6; /* Teal accent */
        color: #FFFFFF !important;
        font-weight: 600;
    }
    
    /* KPI Cards */
    .kpi-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
        justify-content: center;
        align-items: stretch;
    }
    
    .kpi-card {
        flex: 1;
        min-width: 200px;
        max-width: 250px;
        background: rgba(44, 83, 100, 0.5);
        backdrop-filter: blur(5px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(20, 184, 166, 0.3);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(20, 184, 166, 0.7);
    }

    .insight-card {
        background: rgba(44, 83, 100, 0.5);
        border-left: 5px solid #14B8A6;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
    }
    
    .kpi-label {
        color: #B0BEC5; /* Lighter grey */
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }
    
    .kpi-value {
        color: #FFFFFF; /* White */
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Footer */
    .dashboard-footer {
        color: #B0BEC5;
        text-align: center;
        padding: 1.5rem;
        margin-top: 3rem;
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-top-color: #14B8A6;
    }
    
    /* Button Styling */
    .stButton > button {
        background: #14B8A6;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
    }
    
    /* Input Styling */
    .stSelectbox > div > div, .stDateInput > div > div {
        background: rgba(44, 83, 100, 0.7);
        border-radius: 10px;
        border: 1px solid rgba(20, 184, 166, 0.3);
        color: #FFFFFF;
    }

    .stSelectbox div[data-baseweb="select"] > div, .stDateInput input {
        color: #FFFFFF !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Style for st.metric in AI tab */
    div[data-testid="stMetric"] {
        background-color: rgba(44, 83, 100, 0.5);
        text-color: #B0BEC5 !important;
        border: 1px solid rgba(20, 184, 166, 0.3);
        border-radius: 10px;
        padding: 1rem;
    }

    /* Force color for all parts of the metric, with high specificity for the label */
    div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] > div {
        color: #B0BEC5 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    div[data-testid="stMetricDelta"] {
        color: #B0BEC5 !important;
    }

    /* Hyper-specific fix for metric labels based on user feedback */
    .st-emotion-cache-1r4qj8v {
        color: #FFFFFF !important;
    }

    /* Set AI chatbot response color to white */
    /* Fix for chat interface text visibility */
    .stChatMessage {
        color: #FFFFFF !important;
    }

    /* Chat message content */
    .stChatMessage [data-testid="stMarkdownContainer"] {
        color: #FFFFFF !important;
    }

    /* Chat message content - more specific targeting */
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
    }

    /* Assistant/AI responses specifically */
    div[data-testid="stChatMessage"][data-testid*="assistant"] {
        color: #FFFFFF !important;
    }

    /* User messages */
    div[data-testid="stChatMessage"][data-testid*="user"] {
        color: #FFFFFF !important;
    }

    /* Chat input styling */
    .stChatInput input {
        background-color: rgba(44, 83, 100, 0.7) !important;
        border: 1px solid rgba(20, 184, 166, 0.3) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }

    /* Chat input placeholder */
    .stChatInput input::placeholder {
        color: #B0BEC5 !important;
    }

    /* Spinner text fix */
    .stSpinner > div > div {
        color: #FFFFFF !important;
    }

    /* Loading text */
    .stSpinner + div {
        color: #FFFFFF !important;
    }

    /* All markdown content in chat messages */
    .stChatMessage div[class*="markdown"] {
        color: #FFFFFF !important;
    }

    .stChatMessage div[class*="markdown"] * {
        color: #FFFFFF !important;
    }

    /* Strong/bold text in chat */
    .stChatMessage strong {
        color: #14B8A6 !important;
    }

    /* Chat message containers */
    div[data-testid="stChatMessage"] {
        background-color: rgba(44, 83, 100, 0.3) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(20, 184, 166, 0.2) !important;
    }

    /* Make sure all text elements are white */
    .stChatMessage p, 
    .stChatMessage span, 
    .stChatMessage div {
        color: #FFFFFF !important;
    }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_data() -> Optional[pd.DataFrame]:
    try:
        processor = DataProcessor()
        data = processor.load_data()
        if not data:
            st.error("❌ Failed to load data. Please check your dataset files.")
            return None
        processor.clean_data()
        return processor.combine_data()
    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")
        return None

def create_header() -> None:
    st.markdown("<div class='main-header'><h1> Marketing Intelligence Pro</h1><p>Advanced AI-Powered Marketing Analytics & Insights</p></div>", unsafe_allow_html=True)

def create_sidebar_filters(df: pd.DataFrame) -> Tuple[Any, Any, Any]:
    st.sidebar.markdown("###  Control Panel")
    if df.empty:
        return None, None, []

    st.sidebar.markdown("**Time Range**")
    date_preset = st.sidebar.selectbox("Quick Select", ["Custom", "Last 7 Days", "Last 30 Days", "Last Quarter", "All Time"])
    
    max_date = df['date'].max().date()
    min_date = df['date'].min().date()

    if date_preset == "All Time":
        date_range = (min_date, max_date)
    elif date_preset == "Last 7 Days":
        date_range = (max_date - pd.Timedelta(days=6), max_date)
    elif date_preset == "Last 30 Days":
        date_range = (max_date - pd.Timedelta(days=29), max_date)
    elif date_preset == "Last Quarter":
        max_date_ts = pd.to_datetime(max_date)
        current_quarter_start = max_date_ts.to_period('Q').to_timestamp()
        last_quarter_end = current_quarter_start - pd.Timedelta(days=1)
        last_quarter_start = last_quarter_end.to_period('Q').to_timestamp()
        date_range = (last_quarter_start.date(), last_quarter_end.date())
    else: # Custom
        date_range = st.sidebar.date_input("Custom Range", value=(min_date, max_date))

    st.sidebar.markdown(" Platforms ")
    platform_options = {"Facebook": " Facebook", "Google": " Google", "TikTok": " TikTok"}
    selected_platforms = st.sidebar.multiselect("Select Platforms", options=list(platform_options.keys()), default=list(platform_options.keys()), format_func=lambda x: platform_options[x])
    
    return date_range, selected_platforms

def main():
    create_header()
    
    combined_df = load_and_process_data()
    if combined_df is None:
        st.stop()

    date_range, selected_platforms = create_sidebar_filters(combined_df)
    
    if not date_range or len(date_range) != 2:
        st.warning("Please select a valid date range.")
        st.stop()

    start_date, end_date = date_range
    filtered_df = combined_df[(combined_df['date'].dt.date >= start_date) & (combined_df['date'].dt.date <= end_date)].copy()

    # Recalculate stats based on filters
    spend_cols = [f"{p}_spend" for p in selected_platforms if f"{p}_spend" in filtered_df.columns]
    attr_rev_cols = [f"{p}_attributed revenue" for p in selected_platforms if f"{p}_attributed revenue" in filtered_df.columns]

    total_spend = filtered_df[spend_cols].sum().sum()
    total_attributed_revenue = filtered_df[attr_rev_cols].sum().sum()
    total_business_revenue = filtered_df['total revenue'].sum()
    overall_roas = total_attributed_revenue / total_spend if total_spend > 0 else 0
    attribution_gap = ((total_business_revenue - total_attributed_revenue) / total_business_revenue * 100) if total_business_revenue > 0 else 0

    filtered_summary_stats = {
        'total_spend': total_spend,
        'total_attributed_revenue': total_attributed_revenue,
        'total_business_revenue': total_business_revenue,
        'overall_roas': overall_roas,
        'attribution_gap': attribution_gap,
    }

    st.subheader(" Key Performance Indicators")
    DashboardComponents.create_kpi_cards(filtered_summary_stats)
    
    create_dashboard_tabs(filtered_df, selected_platforms, filtered_summary_stats)
    
    create_footer()

def create_dashboard_tabs(filtered_df: pd.DataFrame, selected_platforms: list, summary_stats: dict) -> None:
    tab1, tab2, tab3, tab4 = st.tabs([" Executive Summary", " Performance Analytics", " Strategic Insights", " AI Intelligence"])
    
    with tab1:
        create_overview_tab(filtered_df, selected_platforms)
    with tab2:
        create_trends_tab(filtered_df, selected_platforms)
    with tab3:
        create_insights_tab(filtered_df, selected_platforms)
    with tab4:
        create_ai_intelligence_tab(filtered_df, summary_stats, selected_platforms)

def create_overview_tab(filtered_df: pd.DataFrame, selected_platforms: List[str]) -> None:
    st.subheader("Revenue Overview")
    col1, col2 = st.columns(2)
    with col1:
        fig_revenue = DashboardComponents.create_revenue_trend_chart(filtered_df, selected_platforms)
        st.plotly_chart(fig_revenue, use_container_width=True)
    with col2:
        fig_attribution = DashboardComponents.create_attribution_analysis(filtered_df, selected_platforms)
        st.plotly_chart(fig_attribution, use_container_width=True)

def create_trends_tab(filtered_df: pd.DataFrame, selected_platforms: List[str]) -> None:
    st.subheader("Marketing Performance Trends")
    fig_comparison = DashboardComponents.create_platform_comparison_chart(filtered_df, selected_platforms)
    st.plotly_chart(fig_comparison, use_container_width=True)
    fig_scatter = DashboardComponents.create_spend_vs_revenue_scatter(filtered_df, selected_platforms)
    st.plotly_chart(fig_scatter, use_container_width=True)

def create_insights_tab(filtered_df: pd.DataFrame, selected_platforms: List[str]) -> None:
    """Create insights tab content"""
    st.subheader(" Key Insights & Recommendations")
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("####  Key Insights")
        insights = generate_insights(filtered_df, selected_platforms)
        for insight in insights:
            st.markdown(f"<div class='insight-card'>{insight}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("####  Recommendations")
        recommendations = display_recommendations(filtered_df, selected_platforms)
        for rec in recommendations:
            st.markdown(f"<div class='insight-card'>{rec}</div>", unsafe_allow_html=True)

def generate_insights(filtered_df: pd.DataFrame, selected_platforms: List[str]) -> list:
    """Generate insights based on data analysis"""
    insights = []

    # Calculate summary stats for the filtered data
    spend_cols = [f"{p}_spend" for p in selected_platforms if f"{p}_spend" in filtered_df.columns]
    attr_rev_cols = [f"{p}_attributed revenue" for p in selected_platforms if f"{p}_attributed revenue" in filtered_df.columns]
    total_spend = filtered_df[spend_cols].sum().sum()
    total_attributed_revenue = filtered_df[attr_rev_cols].sum().sum()
    total_business_revenue = filtered_df['total revenue'].sum()
    overall_roas = total_attributed_revenue / total_spend if total_spend > 0 else 0
    attribution_gap = ((total_business_revenue - total_attributed_revenue) / total_business_revenue * 100) if total_business_revenue > 0 else 0

    # ROAS insights
    if overall_roas > 3:
        insights.append(" Strong ROAS: Overall ROAS is above 3x, indicating efficient marketing spend.")
    elif overall_roas > 2:
        insights.append(" Moderate ROAS: Overall ROAS is between 2-3x. Consider optimizing underperforming campaigns.")
    else:
        insights.append(" Low ROAS: Overall ROAS is below 2x. Immediate optimization is needed.")

    # Attribution insights
    if attribution_gap > 50:
        insights.append(" High Attribution Gap: More than 50% of revenue is unattributed. Improving tracking should be a priority.")
    elif attribution_gap > 25:
        insights.append(" Moderate Attribution Gap: A gap of 25-50% suggests a review of your attribution model is needed.")
    else:
        insights.append(" Good Attribution: Your attribution gap is less than 25%, indicating healthy tracking.")

    # Platform insights
    platform_performance = []
    for platform in selected_platforms:
        spend_col = f"{platform}_spend"
        revenue_col = f"{platform}_attributed revenue"
        if spend_col in filtered_df.columns and revenue_col in filtered_df.columns:
            spend = filtered_df[spend_col].sum()
            revenue = filtered_df[revenue_col].sum()
            if spend > 0:
                roas = revenue / spend
                platform_performance.append((platform, roas, spend))

    if platform_performance:
        platform_performance.sort(key=lambda x: x[1], reverse=True)
        best_platform = platform_performance[0]
        worst_platform = platform_performance[-1]
        
        if best_platform[1] > worst_platform[1] + 0.5:
             insights.append(f" Top Performer: {best_platform[0]} is leading with a ROAS of {best_platform[1]:.2f}x.")
        if worst_platform[1] < 2.0:
             insights.append(f" Optimization Opportunity: {worst_platform[0]} shows the lowest ROAS at {worst_platform[1]:.2f}x.")

    return insights

def display_recommendations(filtered_df: pd.DataFrame, selected_platforms: List[str]) -> List[str]:
    """Generate and return strategic recommendations"""
    platform_performance = []
    for platform in selected_platforms:
        spend_col = f"{platform}_spend"
        revenue_col = f"{platform}_attributed revenue"
        if spend_col in filtered_df.columns and revenue_col in filtered_df.columns:
            spend = filtered_df[spend_col].sum()
            revenue = filtered_df[revenue_col].sum()
            if spend > 0:
                roas = revenue / spend
                platform_performance.append((platform, roas, spend))

    recommendations = []
    if platform_performance:
        platform_performance.sort(key=lambda x: x[1], reverse=True)
        best_platform = platform_performance[0]
        worst_platform = platform_performance[-1]

        if best_platform[1] > 3.0:
            recommendations.append(f"Scale Up {best_platform[0]}: With a strong ROAS of {best_platform[1]:.2f}x, consider increasing its budget.")
        
        if worst_platform[1] < 2.0 and best_platform[1] > worst_platform[1] + 1:
            recommendations.append(f"Re-evaluate {worst_platform[0]}: This platform's ROAS is low at {worst_platform[1]:.2f}x. Audit its campaigns or reallocate budget.")
        else:
            recommendations.append(f"Optimize {worst_platform[0]}: Review creatives for {worst_platform[0]} to improve its ROAS of {worst_platform[1]:.2f}x.")

    recommendations.append("A/B Test Creatives: Continuously test new ad creatives across all platforms.")
    return recommendations

def create_ai_intelligence_tab(filtered_df: pd.DataFrame, summary_stats: dict, selected_platforms: List[str]) -> None:
    ai_insights = AIInsights()
    # Pass selected_platforms to the main tab creation function
    ai_insights.create_ai_insights_tab(filtered_df, summary_stats, selected_platforms)
    
    st.markdown("---")
    # Recalculate platform_performance specifically for the chat interface
    platform_performance = ai_insights._analyze_platform_performance(filtered_df, selected_platforms)
    ai_insights.create_ai_chat_interface(summary_stats, platform_performance)

def create_footer() -> None:
    st.markdown("<div class='dashboard-footer'><p style='margin: 0; color: #64748b; font-size: 0.9rem;'> <strong>Marketing Intelligence Pro</strong> | Powered by AI & Advanced Analytics | Built with Streamlit & Google Gemini</p></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
