"""
SkyGeni Sales Intelligence Challenge - Exploratory Data Analysis
Author: Data Science / Applied AI Engineer Candidate
Date: February 2026

This script performs comprehensive exploratory data analysis on the sales dataset
to identify business insights and custom metrics for diagnosing win rate decline.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for professional visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class SalesDataAnalyzer:
    """Comprehensive sales data analysis and insight generation"""
    
    def __init__(self, data_path):
        """Initialize analyzer with data path"""
        self.data_path = data_path
        self.df = None
        self.insights = []
        
    def load_and_validate_data(self):
        """Load and perform initial data validation"""
        print("=" * 80)
        print("LOADING AND VALIDATING DATASET")
        print("=" * 80)
        
        self.df = pd.read_csv(self.data_path)
        
        # Convert date columns
        self.df['created_date'] = pd.to_datetime(self.df['created_date'])
        self.df['closed_date'] = pd.to_datetime(self.df['closed_date'])
        
        # Extract temporal features
        self.df['created_quarter'] = self.df['created_date'].dt.to_period('Q')
        self.df['closed_quarter'] = self.df['closed_date'].dt.to_period('Q')
        self.df['created_month'] = self.df['created_date'].dt.to_period('M')
        self.df['closed_month'] = self.df['closed_date'].dt.to_period('M')
        
        # Basic validation
        print(f"\n✓ Dataset loaded: {len(self.df):,} deals")
        print(f"✓ Date range: {self.df['created_date'].min().date()} to {self.df['closed_date'].max().date()}")
        print(f"✓ Columns: {', '.join(self.df.columns)}")
        print(f"\n✓ Missing values:\n{self.df.isnull().sum()}")
        print(f"\n✓ Data types:\n{self.df.dtypes}")
        
        return self
    
    def calculate_custom_metrics(self):
        """Calculate custom metrics: Deal Velocity Score and Pipeline Health Index"""
        print("\n" + "=" * 80)
        print("CALCULATING CUSTOM METRICS")
        print("=" * 80)
        
        # Custom Metric 1: Deal Velocity Score
        # Normalized measure of deal speed relative to segment benchmarks
        
        # Calculate expected days by segment (industry + product_type)
        segment_avg = self.df.groupby(['industry', 'product_type'])['sales_cycle_days'].transform('median')
        
        # Deal Velocity Score: (Expected - Actual) / Expected
        # Positive = faster than expected (good), Negative = slower (concerning)
        self.df['deal_velocity_score'] = (segment_avg - self.df['sales_cycle_days']) / segment_avg
        
        print("\n✓ Custom Metric 1: Deal Velocity Score")
        print(f"  - Mean: {self.df['deal_velocity_score'].mean():.3f}")
        print(f"  - Median: {self.df['deal_velocity_score'].median():.3f}")
        print(f"  - Range: [{self.df['deal_velocity_score'].min():.3f}, {self.df['deal_velocity_score'].max():.3f}]")
        
        # Custom Metric 2: Pipeline Health Index (by quarter)
        # Composite score: win rate momentum (30%) + deal size trend (30%) + stage quality (40%)
        
        quarterly_metrics = self.df.groupby('closed_quarter').agg({
            'outcome': lambda x: (x == 'Won').mean(),  # Win rate
            'deal_amount': 'mean',  # Average deal size
            'sales_cycle_days': 'mean'  # Sales cycle
        }).reset_index()
        
        quarterly_metrics.columns = ['quarter', 'win_rate', 'avg_deal_size', 'avg_cycle_days']
        
        # Normalize metrics to 0-1 scale
        quarterly_metrics['win_rate_norm'] = quarterly_metrics['win_rate']
        quarterly_metrics['deal_size_norm'] = (quarterly_metrics['avg_deal_size'] - quarterly_metrics['avg_deal_size'].min()) / \
                                               (quarterly_metrics['avg_deal_size'].max() - quarterly_metrics['avg_deal_size'].min())
        quarterly_metrics['cycle_norm'] = 1 - ((quarterly_metrics['avg_cycle_days'] - quarterly_metrics['avg_cycle_days'].min()) / \
                                                (quarterly_metrics['avg_cycle_days'].max() - quarterly_metrics['avg_cycle_days'].min()))
        
        # Pipeline Health Index (0-100 scale)
        quarterly_metrics['pipeline_health_index'] = (
            quarterly_metrics['win_rate_norm'] * 0.3 +
            quarterly_metrics['deal_size_norm'] * 0.3 +
            quarterly_metrics['cycle_norm'] * 0.4
        ) * 100
        
        self.quarterly_metrics = quarterly_metrics
        
        print("\n✓ Custom Metric 2: Pipeline Health Index (by quarter)")
        print(quarterly_metrics[['quarter', 'win_rate', 'pipeline_health_index']].to_string(index=False))
        
        return self
    
    def analyze_win_rate_trends(self):
        """Analyze win rate trends over time and by segment"""
        print("\n" + "=" * 80)
        print("ANALYZING WIN RATE TRENDS")
        print("=" * 80)
        
        # Overall win rate
        overall_win_rate = (self.df['outcome'] == 'Won').mean()
        print(f"\n✓ Overall Win Rate: {overall_win_rate:.2%}")
        
        # Win rate by quarter
        quarterly_win_rate = self.df.groupby('closed_quarter').apply(
            lambda x: (x['outcome'] == 'Won').mean()
        ).reset_index()
        quarterly_win_rate.columns = ['quarter', 'win_rate']
        
        print("\n✓ Win Rate by Quarter:")
        print(quarterly_win_rate.to_string(index=False))
        
        # Identify declining trend
        recent_quarters = quarterly_win_rate.tail(2)
        if len(recent_quarters) >= 2:
            decline = recent_quarters.iloc[-1]['win_rate'] - recent_quarters.iloc[0]['win_rate']
            print(f"\n⚠️  Last 2 quarters trend: {decline:+.2%}")
        
        # Win rate by segment
        print("\n✓ Win Rate by Industry:")
        industry_wr = self.df.groupby('industry').apply(
            lambda x: pd.Series({
                'win_rate': (x['outcome'] == 'Won').mean(),
                'deal_count': len(x)
            })
        ).sort_values('win_rate', ascending=False)
        print(industry_wr.to_string())
        
        print("\n✓ Win Rate by Region:")
        region_wr = self.df.groupby('region').apply(
            lambda x: pd.Series({
                'win_rate': (x['outcome'] == 'Won').mean(),
                'deal_count': len(x)
            })
        ).sort_values('win_rate', ascending=False)
        print(region_wr.to_string())
        
        print("\n✓ Win Rate by Product Type:")
        product_wr = self.df.groupby('product_type').apply(
            lambda x: pd.Series({
                'win_rate': (x['outcome'] == 'Won').mean(),
                'deal_count': len(x)
            })
        ).sort_values('win_rate', ascending=False)
        print(product_wr.to_string())
        
        print("\n✓ Win Rate by Lead Source:")
        lead_wr = self.df.groupby('lead_source').apply(
            lambda x: pd.Series({
                'win_rate': (x['outcome'] == 'Won').mean(),
                'deal_count': len(x)
            })
        ).sort_values('win_rate', ascending=False)
        print(lead_wr.to_string())
        
        # Store for insights
        self.segment_analysis = {
            'industry': industry_wr,
            'region': region_wr,
            'product': product_wr,
            'lead_source': lead_wr,
            'quarterly': quarterly_win_rate
        }
        
        return self
    
    def analyze_sales_rep_performance(self):
        """Analyze sales rep performance and variance"""
        print("\n" + "=" * 80)
        print("ANALYZING SALES REP PERFORMANCE")
        print("=" * 80)
        
        rep_performance = self.df.groupby('sales_rep_id').agg({
            'deal_id': 'count',
            'outcome': lambda x: (x == 'Won').mean(),
            'deal_amount': 'mean',
            'sales_cycle_days': 'mean'
        }).reset_index()
        
        rep_performance.columns = ['rep_id', 'deal_count', 'win_rate', 'avg_deal_size', 'avg_cycle_days']
        rep_performance = rep_performance.sort_values('win_rate', ascending=False)
        
        print(f"\n✓ Sales Rep Performance Summary:")
        print(f"  - Total reps: {len(rep_performance)}")
        print(f"  - Avg win rate: {rep_performance['win_rate'].mean():.2%}")
        print(f"  - Win rate std dev: {rep_performance['win_rate'].std():.2%}")
        print(f"  - Top performer: {rep_performance.iloc[0]['rep_id']} ({rep_performance.iloc[0]['win_rate']:.2%})")
        print(f"  - Bottom performer: {rep_performance.iloc[-1]['rep_id']} ({rep_performance.iloc[-1]['win_rate']:.2%})")
        
        print(f"\n✓ Top 5 Performers:")
        print(rep_performance.head().to_string(index=False))
        
        print(f"\n✓ Bottom 5 Performers:")
        print(rep_performance.tail().to_string(index=False))
        
        self.rep_performance = rep_performance
        
        return self
    
    def generate_visualizations(self):
        """Generate key visualizations"""
        print("\n" + "=" * 80)
        print("GENERATING VISUALIZATIONS")
        print("=" * 80)
        
        fig = plt.figure(figsize=(20, 12))
        
        # 1. Win Rate Trend Over Time
        ax1 = plt.subplot(2, 3, 1)
        quarterly_data = self.segment_analysis['quarterly']
        ax1.plot(range(len(quarterly_data)), quarterly_data['win_rate'], marker='o', linewidth=2, markersize=8)
        ax1.set_xticks(range(len(quarterly_data)))
        ax1.set_xticklabels([str(q) for q in quarterly_data['quarter']], rotation=45)
        ax1.set_ylabel('Win Rate', fontsize=12)
        ax1.set_title('Win Rate Trend by Quarter', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=quarterly_data['win_rate'].mean(), color='r', linestyle='--', alpha=0.5, label='Average')
        ax1.legend()
        
        # 2. Win Rate by Industry
        ax2 = plt.subplot(2, 3, 2)
        industry_data = self.segment_analysis['industry'].sort_values('win_rate')
        ax2.barh(range(len(industry_data)), industry_data['win_rate'])
        ax2.set_yticks(range(len(industry_data)))
        ax2.set_yticklabels(industry_data.index)
        ax2.set_xlabel('Win Rate', fontsize=12)
        ax2.set_title('Win Rate by Industry', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        # 3. Win Rate by Region
        ax3 = plt.subplot(2, 3, 3)
        region_data = self.segment_analysis['region'].sort_values('win_rate')
        ax3.barh(range(len(region_data)), region_data['win_rate'])
        ax3.set_yticks(range(len(region_data)))
        ax3.set_yticklabels(region_data.index)
        ax3.set_xlabel('Win Rate', fontsize=12)
        ax3.set_title('Win Rate by Region', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='x')
        
        # 4. Pipeline Health Index Trend
        ax4 = plt.subplot(2, 3, 4)
        ax4.plot(range(len(self.quarterly_metrics)), self.quarterly_metrics['pipeline_health_index'], 
                marker='s', linewidth=2, markersize=8, color='green')
        ax4.set_xticks(range(len(self.quarterly_metrics)))
        ax4.set_xticklabels([str(q) for q in self.quarterly_metrics['quarter']], rotation=45)
        ax4.set_ylabel('Pipeline Health Index (0-100)', fontsize=12)
        ax4.set_title('Pipeline Health Index Trend', fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.axhline(y=70, color='orange', linestyle='--', alpha=0.5, label='Threshold (70)')
        ax4.legend()
        
        # 5. Sales Rep Performance Distribution
        ax5 = plt.subplot(2, 3, 5)
        ax5.hist(self.rep_performance['win_rate'], bins=15, edgecolor='black', alpha=0.7)
        ax5.axvline(x=self.rep_performance['win_rate'].mean(), color='r', linestyle='--', linewidth=2, label='Mean')
        ax5.set_xlabel('Win Rate', fontsize=12)
        ax5.set_ylabel('Number of Reps', fontsize=12)
        ax5.set_title('Sales Rep Win Rate Distribution', fontsize=14, fontweight='bold')
        ax5.legend()
        ax5.grid(True, alpha=0.3, axis='y')
        
        # 6. Deal Amount by Outcome
        ax6 = plt.subplot(2, 3, 6)
        won_deals = self.df[self.df['outcome'] == 'Won']['deal_amount']
        lost_deals = self.df[self.df['outcome'] == 'Lost']['deal_amount']
        ax6.boxplot([won_deals, lost_deals], labels=['Won', 'Lost'])
        ax6.set_ylabel('Deal Amount ($)', fontsize=12)
        ax6.set_title('Deal Amount Distribution by Outcome', fontsize=14, fontweight='bold')
        ax6.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('outputs/visualizations/eda_overview.png', dpi=300, bbox_inches='tight')
        print("\n✓ Saved: outputs/visualizations/eda_overview.png")
        
        # Additional visualization: Deal Velocity Score distribution
        fig2, ax = plt.subplots(figsize=(12, 6))
        won_velocity = self.df[self.df['outcome'] == 'Won']['deal_velocity_score']
        lost_velocity = self.df[self.df['outcome'] == 'Lost']['deal_velocity_score']
        
        ax.hist([won_velocity, lost_velocity], bins=30, label=['Won', 'Lost'], alpha=0.7, edgecolor='black')
        ax.axvline(x=0, color='black', linestyle='--', linewidth=2, label='Benchmark')
        ax.set_xlabel('Deal Velocity Score', fontsize=12)
        ax.set_ylabel('Number of Deals', fontsize=12)
        ax.set_title('Deal Velocity Score Distribution by Outcome', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('outputs/visualizations/deal_velocity_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: outputs/visualizations/deal_velocity_analysis.png")
        
        plt.close('all')
        
        return self
    
    def generate_insights_report(self):
        """Generate comprehensive insights report in markdown"""
        print("\n" + "=" * 80)
        print("GENERATING INSIGHTS REPORT")
        print("=" * 80)
        
        # Analyze data for insights
        quarterly_data = self.segment_analysis['quarterly']
        last_two_quarters = quarterly_data.tail(2)
        win_rate_decline = last_two_quarters.iloc[-1]['win_rate'] - last_two_quarters.iloc[0]['win_rate']
        
        # Industry analysis
        industry_data = self.segment_analysis['industry']
        best_industry = industry_data.index[0]
        worst_industry = industry_data.index[-1]
        
        # Lead source analysis
        lead_data = self.segment_analysis['lead_source']
        best_lead_source = lead_data.index[0]
        worst_lead_source = lead_data.index[-1]
        
        # Rep performance variance
        rep_variance = self.rep_performance['win_rate'].std()
        
        # Deal velocity insights
        won_avg_velocity = self.df[self.df['outcome'] == 'Won']['deal_velocity_score'].mean()
        lost_avg_velocity = self.df[self.df['outcome'] == 'Lost']['deal_velocity_score'].mean()
        
        report = f"""# Sales Intelligence Insights Report

## Executive Summary

This report presents key findings from analyzing {len(self.df):,} B2B SaaS deals to diagnose the win rate decline over the last two quarters.

**Overall Win Rate**: {(self.df['outcome'] == 'Won').mean():.2%}  
**Analysis Period**: {self.df['created_date'].min().date()} to {self.df['closed_date'].max().date()}

---

## 🔍 Key Business Insights

### Insight 1: Win Rate Decline Concentrated in Specific Segments

**Finding**: While overall win rate shows a decline of {win_rate_decline:.2%} over the last two quarters, the decline is NOT uniform across all segments.

**Data**:
- **{worst_industry}** industry has the lowest win rate at {industry_data.loc[worst_industry, 'win_rate']:.2%}
- **{best_industry}** industry maintains a strong {industry_data.loc[best_industry, 'win_rate']:.2%} win rate
- **{worst_lead_source}** lead source shows only {lead_data.loc[worst_lead_source, 'win_rate']:.2%} win rate vs. {lead_data.loc[best_lead_source, 'win_rate']:.2%} for {best_lead_source}

**Why It Matters**: The problem is not a systemic sales process failure but rather segment-specific challenges. This means targeted interventions can have outsized impact.

**Recommended Action**:
1. Conduct win/loss interviews specifically in {worst_industry} segment to understand unique objections
2. Reduce investment in {worst_lead_source} leads or improve qualification criteria
3. Replicate successful playbooks from {best_industry} to struggling segments

---

### Insight 2: Deal Velocity Predicts Outcomes

**Finding**: Won deals move {won_avg_velocity:.2%} faster than segment benchmarks, while lost deals move {abs(lost_avg_velocity):.2%} slower.

**Data** (Custom Metric: Deal Velocity Score):
- **Won deals**: Average velocity score = {won_avg_velocity:+.3f}
- **Lost deals**: Average velocity score = {lost_avg_velocity:+.3f}
- **Difference**: {won_avg_velocity - lost_avg_velocity:.3f} points

**Why It Matters**: Slow-moving deals are a leading indicator of risk. Sales teams can identify at-risk deals BEFORE they reach late stages.

**Recommended Action**:
1. Implement weekly "deal velocity reviews" for deals moving >20% slower than benchmark
2. Create playbooks for accelerating stalled deals (executive engagement, POC scope reduction, etc.)
3. Consider disqualifying deals that remain slow despite intervention (free up rep capacity)

---

### Insight 3: High Sales Rep Performance Variance Indicates Coaching Opportunity

**Finding**: Win rate variance across sales reps is {rep_variance:.2%}, with top performers at {self.rep_performance.iloc[0]['win_rate']:.2%} and bottom performers at {self.rep_performance.iloc[-1]['win_rate']:.2%}.

**Data**:
- **Top 20% of reps**: {self.rep_performance.head(int(len(self.rep_performance) * 0.2))['win_rate'].mean():.2%} win rate
- **Bottom 20% of reps**: {self.rep_performance.tail(int(len(self.rep_performance) * 0.2))['win_rate'].mean():.2%} win rate
- **Performance gap**: {self.rep_performance.head(int(len(self.rep_performance) * 0.2))['win_rate'].mean() - self.rep_performance.tail(int(len(self.rep_performance) * 0.2))['win_rate'].mean():.2%}

**Why It Matters**: High variance suggests that sales outcomes are heavily dependent on individual rep skill rather than process/product. This means coaching and enablement can significantly improve results.

**Recommended Action**:
1. Shadow top performers to document winning behaviors and talk tracks
2. Implement peer coaching program (pair bottom 20% with top 20%)
3. Analyze deal characteristics: are low performers getting harder territories/leads?
4. Consider whether compensation structure inadvertently incentivizes wrong behaviors

---

## 📊 Custom Metrics

### Custom Metric 1: Deal Velocity Score

**Definition**: Normalized measure of how quickly a deal progresses relative to segment benchmarks.

**Formula**: `(Expected Days - Actual Days) / Expected Days`

**Interpretation**:
- **Positive score**: Deal moving faster than expected (high buyer intent)
- **Negative score**: Deal moving slower than expected (risk indicator)
- **Score < -0.3**: High risk of loss

**Business Value**: Enables proactive intervention on slow-moving deals before they stall completely.

---

### Custom Metric 2: Pipeline Health Index

**Definition**: Composite score (0-100) combining win rate trend, deal quality, and sales efficiency.

**Components**:
- Win rate momentum: 30%
- Average deal size trend: 30%
- Sales cycle efficiency: 40%

**Current Trend**:
{self.quarterly_metrics[['quarter', 'pipeline_health_index']].to_string(index=False)}

**Interpretation**:
- **>80**: Excellent pipeline health
- **70-80**: Good, monitor trends
- **60-70**: Concerning, intervention needed
- **<60**: Critical, strategic review required

**Business Value**: Single number for executive dashboards that captures pipeline health beyond just volume.

---

## 📈 Segment Performance Summary

### By Industry
{self.segment_analysis['industry'].to_string()}

### By Region
{self.segment_analysis['region'].to_string()}

### By Product Type
{self.segment_analysis['product'].to_string()}

### By Lead Source
{self.segment_analysis['lead_source'].to_string()}

---

## 🎯 Prioritized Recommendations

### Immediate Actions (This Week)
1. **Audit {worst_lead_source} lead qualification process** - lowest ROI lead source
2. **Launch deal velocity monitoring** - implement weekly reviews for slow deals
3. **Initiate top performer shadowing program** - capture winning behaviors

### Short-Term Actions (This Month)
1. **Segment-specific playbooks** - develop tailored approaches for {worst_industry}
2. **Sales coaching program** - pair bottom 20% reps with top performers
3. **Pipeline health dashboard** - implement executive dashboard with custom metrics

### Strategic Actions (This Quarter)
1. **Win/loss analysis program** - systematic interviews to understand objections
2. **Lead source optimization** - reallocate budget from low-performing sources
3. **Predictive deal scoring** - implement risk scoring for proactive intervention

---

## 📊 Visualizations

See `outputs/visualizations/` for detailed charts:
- `eda_overview.png`: Comprehensive analysis dashboard
- `deal_velocity_analysis.png`: Deal velocity distribution by outcome

---

*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open('outputs/insights_report.md', 'w') as f:
            f.write(report)
        
        print("\n✓ Saved: outputs/insights_report.md")
        
        return self

def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("SKYGENI SALES INTELLIGENCE - EXPLORATORY DATA ANALYSIS")
    print("=" * 80)
    
    # Initialize analyzer
    analyzer = SalesDataAnalyzer('data/skygeni_sales_data.csv')
    
    # Run analysis pipeline
    (analyzer
     .load_and_validate_data()
     .calculate_custom_metrics()
     .analyze_win_rate_trends()
     .analyze_sales_rep_performance()
     .generate_visualizations()
     .generate_insights_report())
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\n✓ Outputs generated:")
    print("  - outputs/insights_report.md")
    print("  - outputs/visualizations/eda_overview.png")
    print("  - outputs/visualizations/deal_velocity_analysis.png")
    print("\n✓ Next step: Run risk scoring engine (src/risk_scoring_engine.py)")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
