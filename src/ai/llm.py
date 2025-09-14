
import os
import json
import pandas as pd
from typing import Dict, List, Optional, Any
import streamlit as st

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class LLMService:
    """Main service class for LLM integration"""
    
    def __init__(self):
        self.gemini_model = None
        if GEMINI_AVAILABLE and os.getenv('GOOGLE_API_KEY'):
            try:
                genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
            except Exception as e:
                st.warning(f"Failed to initialize Gemini: {e}")

    def get_ai_insights(self, data_summary: Dict[str, Any], platform_performance: Dict[str, Any]) -> Dict[str, Any]:
        """Generate rule-based insights for dashboard tabs"""
        return {
            'performance': self._generate_performance_insights(data_summary, platform_performance),
            'recommendations': self._generate_recommendations(data_summary, platform_performance),
            'trends': self._generate_trend_insights(data_summary),
            'attribution': self._generate_attribution_insights(data_summary)
        }

    def _generate_performance_insights(self, data_summary: Dict, platform_performance: Dict) -> str:
        roas = data_summary.get('overall_roas', 0)
        attribution_gap = data_summary.get('attribution_gap', 0)
        insight = ""
        if roas > 3.5:
            insight += f"-  Excellent Marketing ROI: Your overall ROAS of {roas:.2f}x is exceptional, indicating highly efficient marketing spend and strong profitability. "
        elif roas > 2.5:
            insight += f"-  Good Marketing Performance: Your ROAS of {roas:.2f}x is solid. There is a clear opportunity to optimize specific channels to boost this further. "
        else:
            insight += f"-  ROAS Requires Attention: At {roas:.2f}x, your overall ROAS is below the optimal 2.5x threshold. A strategic review of spend allocation is recommended. "

        if attribution_gap > 50:
            insight += f"-  Critical Attribution Gap: A high attribution gap of {attribution_gap:.1f}% suggests more than half of your revenue is not being tracked back to marketing. This should be a top priority to fix."
        elif attribution_gap > 30:
            insight += f"-  Moderate Attribution Gap: The attribution gap of {attribution_gap:.1f}% is considerable. Improving tracking would provide a much clearer picture of marketing effectiveness."
        else:
            insight += f"-  Healthy Attribution: Your attribution gap of {attribution_gap:.1f}% is within a healthy range, showing effective tracking."
        return insight

    def _generate_recommendations(self, data_summary: Dict, platform_performance: Dict) -> List[str]:
        recommendations = []
        if not platform_performance:
            return ["No platform data to generate recommendations."]

        sorted_platforms = sorted(platform_performance.items(), key=lambda item: item[1].get('roas', 0), reverse=True)
        
        best_platform_name, best_platform_stats = sorted_platforms[0]
        worst_platform_name, worst_platform_stats = sorted_platforms[-1]

        if best_platform_stats.get('roas', 0) > 3.0:
            recommendations.append(f" Capitalize on {best_platform_name}: With a stellar ROAS of {best_platform_stats.get('roas', 0):.2f}x, consider scaling up your budget here. Explore lookalike audiences based on your top-performing campaigns on this platform.")
        
        if worst_platform_stats.get('roas', 0) < 2.0 and len(sorted_platforms) > 1:
            recommendations.append(f" Optimize {worst_platform_name}: This platform's ROAS is low at {worst_platform_stats.get('roas', 0):.2f}x. Conduct a creative audit and refine audience targeting. If performance doesn't improve, consider reallocating this budget.")
        
        if data_summary.get('attribution_gap', 0) > 40:
            recommendations.append(" Enhance Tracking Precision: Your significant attribution gap may be hiding the true performance of some channels. Prioritize implementing server-side tagging or a Customer Data Platform (CDP) for more accurate data.")
        else:
            recommendations.append(" Continuous A/B Testing: Your tracking is solid. Now is a good time to aggressively A/B test ad copy, visuals, and landing pages to find new winning combinations.")
        return recommendations

    def _generate_trend_insights(self, data_summary: Dict) -> str:
        marketing_contribution = (data_summary.get('total_attributed_revenue', 0) / data_summary.get('total_business_revenue', 1) * 100)
        return f" Marketing Impact: Your marketing efforts account for {marketing_contribution:.1f}% of total revenue."

    def _generate_attribution_insights(self, data_summary: Dict) -> str:
        attribution_gap = data_summary.get('attribution_gap', 0)
        if attribution_gap < 20:
            return f" Excellent Attribution: Only {attribution_gap:.1f}% unattributed revenue indicates strong tracking."
        else:
            return f" Attribution Gap: {attribution_gap:.1f}% of revenue is unattributed, indicating a need for improved tracking."

    def generate_executive_summary(self, data_summary: Dict, platform_performance: Dict) -> str:
        roas = data_summary.get('overall_roas', 0)
        return f"""
        ##  Executive Summary
        **Key Metrics:**
        - **Overall ROAS**: {roas:.2f}x
        - **Attribution Gap**: {data_summary.get('attribution_gap', 0):.1f}%
        
        **Strategic Insight:**
        Marketing performance shows {'strong' if roas > 3 else 'moderate'} ROI with clear optimization opportunities.
        """

    def get_chat_response(self, query: str, data_summary: Dict, platform_performance: Dict) -> str:
        """Generate a response for the chat using the Gemini API."""
        if not self.gemini_model:
            return "AI chat is not configured. Please ensure your `GOOGLE_API_KEY` is set correctly."

        prompt = f"""
        You are a marketing analyst AI. A user has asked a question about their marketing data.
        Answer the user's query based on the data provided below.

        User Query: "{query}"

        High-Level Marketing Data Summary:
        {json.dumps(data_summary, indent=2)}

        Platform Performance Breakdown:
        {json.dumps(platform_performance, indent=2)}

        Provide a concise and helpful answer to the user's query based on the provided data.
        """
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while communicating with the AI: {e}"

class MockLLMService(LLMService):
    """Mock LLM service for development/testing without API keys"""
    def get_chat_response(self, query: str, data_summary: Dict, platform_performance: Dict) -> str:
        return "This is a mock chat response. Please set your `GOOGLE_API_KEY` to use the real AI chat."

def get_llm_service() -> LLMService:
    """Get LLM service instance based on configuration"""
    if GEMINI_AVAILABLE and os.getenv('GOOGLE_API_KEY'):
        return LLMService()
    else:
        return MockLLMService()
