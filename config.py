

import os
from typing import Dict, Optional



class Config:
    """Configuration class for managing API keys and settings"""
    
    # LLM API Keys (Gemini only)
    GOOGLE_API_KEY: Optional[str] = os.getenv('GOOGLE_API_KEY')
    
    # Dashboard Settings
    DASHBOARD_TITLE: str = "Marketing Intelligence Dashboard"
    DASHBOARD_ICON: str = "📊"
    
    # Data Settings
    DATA_FOLDER: str = "dataset"
    BUSINESS_FILE: str = "business.csv"
    MARKETING_FILES: Dict[str, str] = {
        'Facebook': 'Facebook.csv',
        'Google': 'Google.csv',
        'TikTok': 'TikTok.csv'
    }
    
    # LLM Settings (Gemini optimized)
    DEFAULT_MODEL: str = "gemini-pro"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7
    
    @classmethod
    def get_available_llm_providers(cls) -> list:
        """Get list of available LLM providers based on API keys"""
        providers = []
        
        if cls.GOOGLE_API_KEY:
            providers.append('Google')
        
        return providers
    
    @classmethod
    def is_llm_enabled(cls) -> bool:
        """Check if any LLM provider is configured"""
        return len(cls.get_available_llm_providers()) > 0
    
    @classmethod
    def get_model_options(cls, provider: str) -> list:
        """Get available models for a specific provider"""
        models = {
            'Google': ['gemini-pro', 'gemini-pro-vision']
        }
        
        return models.get(provider, [])
