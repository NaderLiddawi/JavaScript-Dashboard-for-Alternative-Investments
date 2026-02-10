"""
Data Processor

This module handles data loading, cleaning, and prep for the dashboard.

It also identifies Alternatives investments and calculates key metrics.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

import openpyxl


class PortfolioDataProcessor:
    """Process and analyze portfolio data for the Alternatives dashboard."""
    
    # Define which asset classes are considered "Alternatives"
    ALTERNATIVES_CLASSES = {
        'Private Equity',
        'Real Assets', 
        'Hedge Funds',
        'Credit Funds',
        'Real Estate'
    }
    
    NON_ALTERNATIVES_CLASSES = {
        'Equities',
        'Derivatives',
        'Cash',
        'Sovereigns/Treasuries',
        'CMBS',
        'Agencies',
        'Corporate Bonds',
        'Preferreds',
        'ABS',
        'Munis',
        'CLOs',
        'RMBS'
    }
    
    def __init__(self, file_path):
        """Initialize the processor with the Excel file path."""
        self.file_path = file_path
        self.df = None
        self.alts_df = None
        self.non_alts_df = None
        
    def load_data(self):
        """Load portfolio data from Excel file."""
        print("Loading portfolio data...")
        self.df = pd.read_excel(self.file_path, sheet_name='FRL_Portfolio', engine='openpyxl')
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        print(f"Loaded {len(self.df)} records from {self.df['Date'].min()} to {self.df['Date'].max()}")
        return self
    
    def classify_investments(self):
        """Separate Alternatives from Non-Alternatives investments."""
        print("\nClassifying investments...")
        
        # Create Alternatives boolean flag
        self.df['Is_Alternative'] = self.df['Asset_Class'].isin(self.ALTERNATIVES_CLASSES)
        
        # Split into two dataframes
        self.alts_df = self.df[self.df['Is_Alternative']].copy()
        self.non_alts_df = self.df[~self.df['Is_Alternative']].copy()
        
        print(f"Alternatives records: {len(self.alts_df)} ({len(self.alts_df)/len(self.df)*100:.1f}%)")
        print(f"Non-Alternatives records: {len(self.non_alts_df)} ({len(self.non_alts_df)/len(self.df)*100:.1f}%)")
        
        return self
    
    def calculate_returns(self, df):
        """Calculate returns and performance metrics."""
        # Calculate actual return (considering all components)
        df['Total_Return'] = (df['End_NAV'] - df['Beg_NAV'] - 
                               df['Contributions'] + df['Distributions'])
        
        # Calculate return percentage (handling zero beginning NAV)
        df['Return_Pct'] = np.where(
            df['Beg_NAV'] > 0,
            (df['Total_Return'] / df['Beg_NAV']) * 100,
            0
        )
        
        # Calculate change in NAV
        df['NAV_Change'] = df['End_NAV'] - df['Beg_NAV']
        
        return df
    
    def get_composition_by_asset_class(self, as_of_date=None):
        """Get portfolio composition by asset class."""
        df = self.alts_df.copy()
        
        if as_of_date:
            df = df[df['Date'] == as_of_date]
        else:
            # Use most recent date
            as_of_date = df['Date'].max()
            df = df[df['Date'] == as_of_date]
        
        composition = df.groupby('Asset_Class').agg({
            'End_NAV': 'sum',
            'Security': 'nunique'
        }).reset_index()
        
        composition.columns = ['Asset_Class', 'Total_NAV', 'Num_Securities']
        composition['Percentage'] = (composition['Total_NAV'] / composition['Total_NAV'].sum()) * 100
        composition = composition.sort_values('Total_NAV', ascending=False)
        
        return composition
    
    def get_time_series_data(self):
        """Get time series data for NAV trends."""
        # Alternatives over time
        alts_ts = self.alts_df.groupby('Date').agg({
            'End_NAV': 'sum',
            'Net_Investment_Income': 'sum',
            'Contributions': 'sum',
            'Distributions': 'sum'
        }).reset_index()
        
        # Non-Alternatives over time
        non_alts_ts = self.non_alts_df.groupby('Date').agg({
            'End_NAV': 'sum',
            'Net_Investment_Income': 'sum',
            'Contributions': 'sum',
            'Distributions': 'sum'
        }).reset_index()
        
        # Add labels
        alts_ts['Category'] = 'Alternatives'
        non_alts_ts['Category'] = 'Non-Alternatives'
        
        return alts_ts, non_alts_ts
    
    def get_asset_class_trends(self):
        """Get NAV trends by asset class."""
        trends = self.alts_df.groupby(['Date', 'Asset_Class']).agg({
            'End_NAV': 'sum'
        }).reset_index()
        
        return trends
    
    def calculate_performance_metrics(self):
        """Calculate key performance metrics for the Alternatives portfolio."""
        # Calculate for the most recent completed quarter
        recent_date = self.alts_df['Date'].max()
        recent_data = self.alts_df[self.alts_df['Date'] == recent_date]
        
        # Overall metrics
        total_nav = recent_data['End_NAV'].sum()
        total_income = recent_data['Net_Investment_Income'].sum()
        total_contributions = recent_data['Contributions'].sum()
        total_distributions = recent_data['Distributions'].sum()
        
        # Calculate returns
        recent_data = self.calculate_returns(recent_data)
        
        # Weighted average return (weighted by beginning NAV)
        total_beg_nav = recent_data['Beg_NAV'].sum()
        if total_beg_nav > 0:
            weighted_return = ((recent_data['Total_Return'].sum() / total_beg_nav) * 100)
        else:
            weighted_return = 0
        
        # Number of investments
        num_securities = recent_data['Security'].nunique()
        num_asset_classes = recent_data['Asset_Class'].nunique()
        
        metrics = {
            'total_nav': total_nav,
            'total_income': total_income,
            'total_contributions': total_contributions,
            'total_distributions': total_distributions,
            'weighted_return_pct': weighted_return,
            'num_securities': num_securities,
            'num_asset_classes': num_asset_classes,
            'as_of_date': recent_date.strftime('%Y-%m-%d')
        }
        
        return metrics
    
    def get_performance_by_asset_class(self):
        """Calculate performance metrics by asset class."""
        # Use most recent quarter
        recent_date = self.alts_df['Date'].max()
        recent_data = self.alts_df[self.alts_df['Date'] == recent_date].copy()
        
        recent_data = self.calculate_returns(recent_data)
        
        perf = recent_data.groupby('Asset_Class').agg({
            'End_NAV': 'sum',
            'Net_Investment_Income': 'sum',
            'Total_Return': 'sum',
            'Beg_NAV': 'sum',
            'Contributions': 'sum',
            'Distributions': 'sum'
        }).reset_index()
        
        # Calculate return percentage
        perf['Return_Pct'] = np.where(
            perf['Beg_NAV'] > 0,
            (perf['Total_Return'] / perf['Beg_NAV']) * 100,
            0
        )
        
        perf = perf.sort_values('Return_Pct', ascending=False)
        
        return perf
    
    def get_quarterly_performance(self):
        """Get quarterly performance metrics."""
        # Calculate returns for each quarter
        df = self.alts_df.copy()
        df = self.calculate_returns(df)
        
        quarterly = df.groupby('Date').agg({
            'End_NAV': 'sum',
            'Beg_NAV': 'sum',
            'Total_Return': 'sum',
            'Net_Investment_Income': 'sum',
            'Contributions': 'sum',
            'Distributions': 'sum'
        }).reset_index()
        
        # Calculate quarterly return percentage
        quarterly['Return_Pct'] = np.where(
            quarterly['Beg_NAV'] > 0,
            (quarterly['Total_Return'] / quarterly['Beg_NAV']) * 100,
            0
        )
        
        # Calculate income yield
        quarterly['Income_Yield'] = np.where(
            quarterly['Beg_NAV'] > 0,
            (quarterly['Net_Investment_Income'] / quarterly['Beg_NAV']) * 100,
            0
        )
        
        return quarterly
    
    def export_to_json(self):
        """Export processed data to JSON format for the dashboard."""
        print("\nExporting data to JSON...")
        
        # Get all the data
        composition = self.get_composition_by_asset_class()
        alts_ts, non_alts_ts = self.get_time_series_data()
        asset_class_trends = self.get_asset_class_trends()
        metrics = self.calculate_performance_metrics()
        performance = self.get_performance_by_asset_class()
        quarterly = self.get_quarterly_performance()
        
        # Convert to JSON-serializable format
        data = {
            'metadata': {
                'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_period': f"{self.alts_df['Date'].min().strftime('%Y-%m-%d')} to {self.alts_df['Date'].max().strftime('%Y-%m-%d')}",
                'total_records': len(self.df),
                'alternatives_records': len(self.alts_df)
            },
            'key_metrics': metrics,
            'composition': composition.to_dict(orient='records'),
            'alternatives_timeseries': alts_ts.to_dict(orient='records'),
            'non_alternatives_timeseries': non_alts_ts.to_dict(orient='records'),
            'asset_class_trends': asset_class_trends.to_dict(orient='records'),
            'performance_by_asset_class': performance.to_dict(orient='records'),
            'quarterly_performance': quarterly.to_dict(orient='records')
        }
        
        # Convert datetime objects to strings
        for key in ['alternatives_timeseries', 'non_alternatives_timeseries', 
                    'asset_class_trends', 'quarterly_performance']:
            for record in data[key]:
                if 'Date' in record:
                    record['Date'] = pd.to_datetime(record['Date']).strftime('%Y-%m-%d')
        
        print("Data export complete!")
        return data


#*** This main function does not get called by any script; it's just for testing ***
def main():
    """Main execution function for testing."""
    processor = PortfolioDataProcessor('FRL_Portfolio - Interview Use.xlsx')
    processor.load_data()
    processor.classify_investments()
    
    # Get and display key metrics
    metrics = processor.calculate_performance_metrics()
    print("\n" + "="*60)
    print("KEY METRICS FOR ALTERNATIVES PORTFOLIO")
    print("="*60)
    print(f"Total NAV: ${metrics['total_nav']:,.0f}")
    print(f"Number of Securities: {metrics['num_securities']}")
    print(f"Number of Asset Classes: {metrics['num_asset_classes']}")
    print(f"Weighted Return: {metrics['weighted_return_pct']:.2f}%")
    print(f"As of Date: {metrics['as_of_date']}")
    
    # Export data
    data = processor.export_to_json()
    
    return processor, data

#*** This conditional does not evaluate to True; it's just for testing ***
if __name__ == "__main__":
    processor, data = main()
