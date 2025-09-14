

import pandas as pd
import numpy as np
from typing import Dict, Optional
import warnings

warnings.filterwarnings('ignore')

# Constants for better maintainability
PLATFORMS = ['Facebook', 'Google', 'TikTok']
MARKETING_COLUMNS = ['impression', 'clicks', 'spend', 'attributed revenue']
BUSINESS_COLUMNS = {
    'orders': '# of orders',
    'new_orders': '# of new orders',
    'new_customers': 'new customers',
    'revenue': 'total revenue',
    'profit': 'gross profit'
}

class DataProcessor:
    """Main data processing class for marketing intelligence dashboard"""
    
    def __init__(self):
        self.business_df: Optional[pd.DataFrame] = None
        self.marketing_dfs: Dict[str, pd.DataFrame] = {}
        self.combined_df: Optional[pd.DataFrame] = None
        
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """Load all datasets from the dataset folder"""
        try:
            self.business_df = pd.read_csv('dataset/business.csv')
            
            for platform in PLATFORMS:
                df = pd.read_csv(f'dataset/{platform}.csv')
                df['platform'] = platform
                self.marketing_dfs[platform] = df
            
            print("✅ Data loaded successfully!")
            return {'business': self.business_df, **self.marketing_dfs}
        except FileNotFoundError as e:
            print(f"❌ File not found: {e}")
            return {}
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return {}
    
    def clean_data(self) -> None:
        """Clean and standardize data formats"""
        self._clean_business_data()
        self._clean_marketing_data()
    
    def _clean_business_data(self) -> None:
        """Clean business data specifically"""
        if self.business_df is not None:
            self.business_df['date'] = pd.to_datetime(self.business_df['date'])
    
    def _clean_marketing_data(self) -> None:
        """Clean marketing data for all platforms"""
        for platform, df in self.marketing_dfs.items():
            df['date'] = pd.to_datetime(df['date'])
            self._convert_numeric_columns(df)
    
    def _convert_numeric_columns(self, df: pd.DataFrame) -> None:
        """Convert specified columns to numeric type"""
        for col in MARKETING_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
    
    def calculate_marketing_kpis(self) -> pd.DataFrame:
        """Calculate marketing KPIs for all platforms"""
        all_marketing_data = []
        
        for platform, df in self.marketing_dfs.items():
            df_with_kpis = self._calculate_platform_kpis(df)
            all_marketing_data.append(df_with_kpis)
        
        return pd.concat(all_marketing_data, ignore_index=True)
    
    def _calculate_platform_kpis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate KPIs for a single platform"""
        df_clean = df.copy()
        
        # Calculate KPIs with division by zero handling
        kpis = {
            'ctr': df_clean['clicks'] / df_clean['impression'] * 100,
            'cpc': df_clean['spend'] / df_clean['clicks'],
            'cpm': df_clean['spend'] / (df_clean['impression'] / 1000),
            'roas': df_clean['attributed revenue'] / df_clean['spend']
        }
        
        for kpi, values in kpis.items():
            df_clean[kpi] = values.fillna(0).round(2)
        
        return df_clean
    
    def calculate_business_kpis(self) -> Optional[pd.DataFrame]:
        """Calculate business KPIs"""
        if self.business_df is None:
            return None
            
        df = self.business_df.copy()
        
        # Calculate all business KPIs
        business_kpis = {
            'aov': (df['total revenue'] / df['# of orders']).round(2),
            'profit_margin': (df['gross profit'] / df['total revenue'] * 100).round(2),
            'new_customer_rate': (df['new customers'] / df['# of orders'] * 100).round(2)
        }
        
        # Add KPIs to dataframe and handle division by zero
        for kpi, values in business_kpis.items():
            df[kpi] = values.fillna(0)
        
        return df
    
    def combine_data(self) -> pd.DataFrame:
        """Combine marketing and business data by date"""
        marketing_df = self.calculate_marketing_kpis()
        business_df = self.calculate_business_kpis()
        
        if business_df is None:
            return marketing_df
        
        # Aggregate marketing data by date
        daily_marketing = marketing_df.groupby(['date', 'platform']).agg({
            'impression': 'sum',
            'clicks': 'sum', 
            'spend': 'sum',
            'attributed revenue': 'sum',
            'ctr': 'mean',
            'cpc': 'mean',
            'cpm': 'mean',
            'roas': 'mean'
        }).reset_index()
        
        # Pivot to get platforms as columns
        daily_marketing_pivot = daily_marketing.set_index('date').pivot(columns='platform')
        daily_marketing_pivot.columns = [f"{col[1]}_{col[0]}" for col in daily_marketing_pivot.columns]
        daily_marketing_pivot = daily_marketing_pivot.reset_index()
        
        # Merge with business data
        combined_df = pd.merge(business_df, daily_marketing_pivot, on='date', how='left')
        
        # Fill NaN values with 0
        combined_df = combined_df.fillna(0)
        
        self.combined_df = combined_df
        return combined_df
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics for dashboard"""
        if self.combined_df is None:
            return {}
        
        df = self.combined_df
        
        # Calculate total metrics
        total_spend = df[[col for col in df.columns if col.endswith('_spend')]].sum().sum()
        total_attributed_revenue = df[[col for col in df.columns if col.endswith('_attributed revenue')]].sum().sum()
        total_business_revenue = df['total revenue'].sum()
        
        # Calculate overall ROAS
        overall_roas = total_attributed_revenue / total_spend if total_spend > 0 else 0
        
        # Attribution gap
        attribution_gap = ((total_business_revenue - total_attributed_revenue) / total_business_revenue * 100) if total_business_revenue > 0 else 0
        
        return {
            'total_spend': total_spend,
            'total_attributed_revenue': total_attributed_revenue,
            'total_business_revenue': total_business_revenue,
            'overall_roas': overall_roas,
            'attribution_gap': attribution_gap,
            'date_range': f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}"
        }

def main():
    """Test the data processor"""
    processor = DataProcessor()
    
    # Load and process data
    data = processor.load_data()
    if data:
        processor.clean_data()
        combined_df = processor.combine_data()
        summary = processor.get_summary_stats()
        
        print(f"\n📊 Data Summary:")
        print(f"Total Spend: ${summary['total_spend']:,.2f}")
        print(f"Total Attributed Revenue: ${summary['total_attributed_revenue']:,.2f}")
        print(f"Overall ROAS: {summary['overall_roas']:.2f}")
        print(f"Attribution Gap: {summary['attribution_gap']:.1f}%")
        print(f"Date Range: {summary['date_range']}")
        
        print(f"\n📈 Combined Dataset Shape: {combined_df.shape}")
        print(f"Columns: {list(combined_df.columns)}")

if __name__ == "__main__":
    main()
