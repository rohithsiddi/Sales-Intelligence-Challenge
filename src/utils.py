"""
Utility functions for SkyGeni Sales Intelligence Challenge
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

def load_sales_data(file_path: str) -> pd.DataFrame:
    """
    Load and preprocess sales data
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Preprocessed DataFrame
    """
    df = pd.read_csv(file_path)
    df['created_date'] = pd.to_datetime(df['created_date'])
    df['closed_date'] = pd.to_datetime(df['closed_date'])
    return df

def calculate_win_rate(df: pd.DataFrame, group_by: str = None) -> pd.Series:
    """
    Calculate win rate overall or by segment
    
    Args:
        df: Sales DataFrame
        group_by: Column to group by (optional)
        
    Returns:
        Win rate(s)
    """
    if group_by:
        return df.groupby(group_by).apply(lambda x: (x['outcome'] == 'Won').mean())
    else:
        return (df['outcome'] == 'Won').mean()

def format_currency(amount: float) -> str:
    """Format number as currency"""
    return f"${amount:,.0f}"

def format_percentage(value: float) -> str:
    """Format number as percentage"""
    return f"{value:.1%}"

def get_segment_benchmarks(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Calculate benchmark metrics by segment
    
    Args:
        df: Sales DataFrame
        
    Returns:
        Dictionary of segment benchmarks
    """
    benchmarks = {}
    
    for industry in df['industry'].unique():
        industry_data = df[df['industry'] == industry]
        benchmarks[industry] = {
            'win_rate': (industry_data['outcome'] == 'Won').mean(),
            'avg_deal_size': industry_data['deal_amount'].mean(),
            'avg_cycle_days': industry_data['sales_cycle_days'].mean()
        }
    
    return benchmarks

def identify_outliers(series: pd.Series, n_std: float = 3) -> pd.Series:
    """
    Identify outliers using standard deviation method
    
    Args:
        series: Pandas Series
        n_std: Number of standard deviations for threshold
        
    Returns:
        Boolean Series indicating outliers
    """
    mean = series.mean()
    std = series.std()
    return (series < mean - n_std * std) | (series > mean + n_std * std)

def calculate_deal_velocity_score(df: pd.DataFrame) -> pd.Series:
    """
    Calculate Deal Velocity Score
    
    Args:
        df: Sales DataFrame with sales_cycle_days
        
    Returns:
        Series of velocity scores
    """
    # Calculate expected days by segment
    segment_avg = df.groupby(['industry', 'product_type'])['sales_cycle_days'].transform('median')
    
    # Velocity score: (Expected - Actual) / Expected
    velocity_score = (segment_avg - df['sales_cycle_days']) / segment_avg
    
    return velocity_score

def categorize_risk(risk_score: float) -> str:
    """
    Categorize risk score into Low/Medium/High
    
    Args:
        risk_score: Risk score (0-100)
        
    Returns:
        Risk category string
    """
    if risk_score < 33:
        return 'Low'
    elif risk_score < 66:
        return 'Medium'
    else:
        return 'High'

def generate_alert_message(deal_row: pd.Series, risk_score: float) -> str:
    """
    Generate alert message for high-risk deal
    
    Args:
        deal_row: Row from DataFrame
        risk_score: Calculated risk score
        
    Returns:
        Formatted alert message
    """
    message = f"""
🚨 High-Risk Deal Alert

Deal: {deal_row['deal_id']} - {format_currency(deal_row['deal_amount'])}
Risk Score: {risk_score:.0f}/100
Stage: {deal_row['deal_stage']}
Industry: {deal_row['industry']}
Sales Rep: {deal_row['sales_rep_id']}

Recommended Actions:
1. Schedule immediate review with sales manager
2. Assess competitive landscape
3. Consider executive engagement
"""
    return message.strip()

def print_section_header(title: str, width: int = 80):
    """Print formatted section header"""
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)

def print_metric(label: str, value: any, format_type: str = 'default'):
    """
    Print formatted metric
    
    Args:
        label: Metric label
        value: Metric value
        format_type: 'currency', 'percentage', or 'default'
    """
    if format_type == 'currency':
        formatted_value = format_currency(value)
    elif format_type == 'percentage':
        formatted_value = format_percentage(value)
    else:
        formatted_value = str(value)
    
    print(f"  {label}: {formatted_value}")
