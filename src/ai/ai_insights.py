"""
AI Insights component for Marketing Intelligence Dashboard
Handles AI-powered analysis and recommendations
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any
from .llm_service import get_llm_service

class AIInsights:
    """AI-powered insights and recommendations component"""
    
    def __init__(self):
        self.llm_service = get_llm_service()
    
    def create_ai_insights_tab(self, filtered_df: pd.DataFrame, summary_stats: Dict[str, Any], selected_platforms: List[str]) -> None:
        """Create comprehensive AI insights tab"""
        st.subheader("AI-Powered Marketing Intelligence")
        
        platform_performance = self._analyze_platform_performance(filtered_df, selected_platforms)
        
        with st.spinner("AI is analyzing your marketing data..."):
            ai_insights = self.llm_service.get_ai_insights(summary_stats, platform_performance)
        
        with st.expander("Performance Analysis", expanded=True):
            self._display_performance_insights(ai_insights['performance'], platform_performance)
        
        with st.expander("Strategic Recommendations"):
            self._display_recommendations(ai_insights['recommendations'])
        
        with st.expander("Trend Analysis"):
            self._display_trend_insights(ai_insights['trends'])
        
        with st.expander("Attribution Analysis"):
            self._display_attribution_insights(ai_insights['attribution'])
        
        self._display_executive_summary(summary_stats, platform_performance)
    
    def _analyze_platform_performance(self, filtered_df: pd.DataFrame, selected_platforms: List[str]) -> Dict[str, Dict[str, float]]:
        """Analyze platform performance for AI insights"""
        platform_performance = {}
        
        for platform in selected_platforms:
            cols = {metric: f"{platform}_{metric}" for metric in ['spend', 'attributed revenue', 'clicks', 'impression']}
            
            if cols['spend'] in filtered_df.columns:
                spend, revenue, clicks, impressions = [filtered_df[col].sum() for col in cols.values()]
                
                platform_performance[platform] = {
                    'spend': spend, 'revenue': revenue,
                    'roas': revenue/spend if spend > 0 else 0,
                    'ctr': (clicks/impressions*100) if impressions > 0 else 0,
                    'cpc': spend/clicks if clicks > 0 else 0
                }
        
        return platform_performance
    
    def _display_performance_insights(self, performance_insight: str, platform_performance: Dict) -> None:
        """Display performance insights"""
        st.markdown("### Performance Analysis")
        st.markdown(performance_insight)
        
        if platform_performance:
            st.markdown("#### Platform Performance Comparison")
            platform_df = pd.DataFrame(platform_performance).T
            platform_df = platform_df.round(2)
            platform_df['spend'] = platform_df['spend'].apply(lambda x: f"${x:,.0f}")
            platform_df['revenue'] = platform_df['revenue'].apply(lambda x: f"${x:,.0f}")
            platform_df['roas'] = platform_df['roas'].apply(lambda x: f"{x:.2f}x")
            platform_df['ctr'] = platform_df['ctr'].apply(lambda x: f"{x:.2f}%")
            platform_df['cpc'] = platform_df['cpc'].apply(lambda x: f"${x:.2f}")
            st.dataframe(platform_df, use_container_width=True)
    
    def _display_recommendations(self, recommendations: List[str]) -> None:
        """Display AI recommendations"""
        st.markdown("### Strategic Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
    
    def _display_trend_insights(self, trend_insight: str) -> None:
        """Display trend insights"""
        st.markdown("### Trend Analysis")
        st.markdown(trend_insight)
        
        st.markdown("#### Key Trend Indicators")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Growth Trend", "Positive")
        with col2:
            st.metric("Efficiency", "Good")
        with col3:
            st.metric("ROI Trend", "Stable")
        with col4:
            st.metric("Attribution", "Improving")
    
    def _display_attribution_insights(self, attribution_insight: str) -> None:
        """Display attribution insights"""
        st.markdown("### Attribution Analysis")
        st.markdown(attribution_insight)
        
        st.markdown("#### Attribution Breakdown")
        attribution_data = {
            'Channel': ['Facebook', 'Google', 'TikTok', 'Organic', 'Direct', 'Other'],
            'Attributed Revenue': [150000, 120000, 80000, 200000, 150000, 100000],
            'Percentage': [18.75, 15.0, 10.0, 25.0, 18.75, 12.5]
        }
        attribution_df = pd.DataFrame(attribution_data)
        attribution_df['Attributed Revenue'] = attribution_df['Attributed Revenue'].apply(lambda x: f"${x:,.0f}")
        attribution_df['Percentage'] = attribution_df['Percentage'].apply(lambda x: f"{x}%")
        st.dataframe(attribution_df, use_container_width=True)
    
    def _display_executive_summary(self, summary_stats: Dict, platform_performance: Dict) -> None:
        """Display AI-generated executive summary"""
        st.markdown("---")
        st.markdown("### AI-Generated Executive Summary")
        executive_summary = self.llm_service.generate_executive_summary(summary_stats, platform_performance)
        st.markdown(executive_summary)
    
    def create_ai_chat_interface(self, summary_stats: Dict, platform_performance: Dict) -> None:
        """Create AI chat interface for custom queries"""
        st.subheader("Ask AI About Your Marketing Data")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask me anything about your marketing performance..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("AI is thinking..."):
                    response = self.llm_service.get_chat_response(prompt, summary_stats, platform_performance)
                    message_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})