
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List

COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#9467bd',
    'platforms': {'Facebook': '#1f77b4', 'Google': '#ff7f0e', 'TikTok': '#2ca02c'}
}

class DashboardComponents:
    @staticmethod
    def create_kpi_cards(data: Dict[str, float]) -> None:
        def format_currency(value):
            if abs(value) >= 1_000_000: return f"${value/1_000_000:.1f}M"
            if abs(value) >= 1_000: return f"${value/1_000:.1f}K"
            return f"${value:,.0f}"
        
        kpis = [
            ('Total Spend', format_currency(data.get('total_spend', 0)), COLORS['primary']),
            ('Attributed Revenue', format_currency(data.get('total_attributed_revenue', 0)), COLORS['secondary']),
            ('Business Revenue', format_currency(data.get('total_business_revenue', 0)), COLORS['success']),
            ('Overall ROAS', f"{data.get('overall_roas', 0):.2f}x", COLORS['danger']),
            ('Attribution Gap', f"{data.get('attribution_gap', 0):.1f}%", COLORS['warning'])
        ]
        
        cards_html = ''.join([f'<div class="kpi-card" style="border-left: 4px solid {color};"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div></div>' for label, value, color in kpis])
        st.markdown(f'<div class="kpi-container">{cards_html}</div>', unsafe_allow_html=True)

    @staticmethod
    def create_revenue_trend_chart(df: pd.DataFrame, selected_platforms: List[str]):
        attributed_cols = [f"{p}_attributed revenue" for p in selected_platforms if f"{p}_attributed revenue" in df.columns]
        df['total_attributed'] = df[attributed_cols].sum(axis=1)
        
        traces = [
            go.Scatter(x=df['date'], y=df['total revenue'], mode='lines', name='Business Revenue', line=dict(color=COLORS['primary'], width=3)),
            go.Scatter(x=df['date'], y=df['total_attributed'], mode='lines', name='Attributed Revenue', line=dict(color=COLORS['secondary'], width=3))
        ]
        
        fig = go.Figure(traces)
        fig.update_layout(title="Revenue Trends: Business vs Attributed", xaxis_title="Date", yaxis_title="Revenue ($)", hovermode='x unified', height=400)
        return fig

    @staticmethod
    def create_platform_comparison_chart(df: pd.DataFrame, selected_platforms: List[str]):
        platform_data = []
        for platform in selected_platforms:
            cols = {col: f"{platform}_{col}" for col in ['spend', 'attributed revenue', 'clicks', 'impression']}
            if cols['spend'] in df.columns:
                spend, revenue, clicks, impressions = [df[col].sum() for col in cols.values()]
                platform_data.append({
                    'Platform': platform, 'ROAS': revenue/spend if spend > 0 else 0,
                    'CTR (%)': (clicks/impressions*100) if impressions > 0 else 0,
                    'CPC ($)': spend/clicks if clicks > 0 else 0, 'Spend ($)': spend
                })
        
        if not platform_data:
            return go.Figure().update_layout(title="No platform data to display for the selected period.", height=600)

        platform_df = pd.DataFrame(platform_data)
        fig = make_subplots(rows=2, cols=2, subplot_titles=['ROAS by Platform', 'CTR by Platform', 'CPC by Platform', 'Spend by Platform'])
        metrics = [('ROAS', COLORS['success']), ('CTR (%)', COLORS['primary']), ('CPC ($)', COLORS['danger']), ('Spend ($)', COLORS['secondary'])]
        positions = [(1,1), (1,2), (2,1), (2,2)]
        
        for (metric, color), (row, col) in zip(metrics, positions):
            fig.add_trace(go.Bar(x=platform_df['Platform'], y=platform_df[metric], name=metric, marker_color=color), row=row, col=col)
        
        fig.update_layout(title="Platform Performance Comparison", height=600, showlegend=False)
        return fig

    @staticmethod
    def create_spend_vs_revenue_scatter(df: pd.DataFrame, selected_platforms: List[str]):
        fig = go.Figure()
        all_spend, all_revenue = [], []

        for platform in selected_platforms:
            spend_col, revenue_col = f"{platform}_spend", f"{platform}_attributed revenue"
            if spend_col in df.columns and revenue_col in df.columns:
                mask = (df[spend_col] > 0) & (df[revenue_col] > 0)
                fig.add_trace(go.Scatter(x=df[mask][spend_col], y=df[mask][revenue_col], mode='markers', name=platform, marker=dict(color=COLORS['platforms'].get(platform), size=8, opacity=0.7)))
                all_spend.extend(df[mask][spend_col].tolist())
                all_revenue.extend(df[mask][revenue_col].tolist())
        
        if all_spend and all_revenue:
            z = np.polyfit(all_spend, all_revenue, 1)
            p = np.poly1d(z)
            x_trend = np.linspace(min(all_spend), max(all_spend), 100)
            fig.add_trace(go.Scatter(x=x_trend, y=p(x_trend), mode='lines', name='Trend Line', line=dict(color='red', width=2, dash='dash')))
        
        fig.update_layout(title="Spend vs Attributed Revenue by Platform", xaxis_title="Daily Spend ($)", yaxis_title="Attributed Revenue ($)", height=500)
        return fig

    @staticmethod
    def create_attribution_analysis(df: pd.DataFrame, selected_platforms: List[str]):
        attributed_cols = [f"{p}_attributed revenue" for p in selected_platforms if f"{p}_attributed revenue" in df.columns]
        df['total_attributed'] = df[attributed_cols].sum(axis=1)
        df['attribution_gap'] = df['total revenue'] - df['total_attributed']
        df['attribution_gap_pct'] = (df['attribution_gap'] / df['total revenue'] * 100).replace([np.inf, -np.inf], 0)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['date'], y=df['attribution_gap_pct'], name='Attribution Gap %', marker_color='rgba(220, 20, 60, 0.7)'))
        fig.update_layout(title="Daily Attribution Gap (Unattributed Revenue %)", xaxis_title="Date", yaxis_title="Attribution Gap (%)", height=400)
        return fig