"""
SkyGeni Sales Intelligence Challenge - Deal Risk Scoring Engine
Author: Data Science / Applied AI Engineer Candidate
Date: February 2026

This script implements a deal risk scoring system to help sales teams
prioritize intervention efforts on deals most likely to be lost.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

class DealRiskScoringEngine:
    """Deal risk scoring system using logistic regression"""
    
    def __init__(self, data_path):
        """Initialize the risk scoring engine"""
        self.data_path = data_path
        self.df = None
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.feature_importance = {}
        
    def load_and_prepare_data(self):
        """Load data and engineer features for risk scoring"""
        print("=" * 80)
        print("DEAL RISK SCORING ENGINE - DATA PREPARATION")
        print("=" * 80)
        
        self.df = pd.read_csv(self.data_path)
        
        # Convert dates
        self.df['created_date'] = pd.to_datetime(self.df['created_date'])
        self.df['closed_date'] = pd.to_datetime(self.df['closed_date'])
        
        # Create binary outcome (1 = Lost, 0 = Won) - we're predicting RISK of loss
        self.df['risk_outcome'] = (self.df['outcome'] == 'Lost').astype(int)
        
        print(f"\n✓ Loaded {len(self.df):,} deals")
        print(f"✓ Lost deals (high risk): {self.df['risk_outcome'].sum():,} ({self.df['risk_outcome'].mean():.2%})")
        print(f"✓ Won deals (low risk): {(1-self.df['risk_outcome']).sum():,} ({(1-self.df['risk_outcome']).mean():.2%})")
        
        return self
    
    def engineer_features(self):
        """Engineer features for risk prediction"""
        print("\n" + "=" * 80)
        print("FEATURE ENGINEERING")
        print("=" * 80)
        
        # Feature 1: Sales cycle length (already provided)
        self.df['sales_cycle_days_norm'] = self.df['sales_cycle_days']
        
        # Feature 2: Deal amount (log transform to handle skewness)
        self.df['deal_amount_log'] = np.log1p(self.df['deal_amount'])
        
        # Feature 3: Historical win rate by industry
        industry_win_rate = self.df.groupby('industry')['risk_outcome'].transform(lambda x: 1 - x.mean())
        self.df['industry_win_rate'] = industry_win_rate
        
        # Feature 4: Historical win rate by region
        region_win_rate = self.df.groupby('region')['risk_outcome'].transform(lambda x: 1 - x.mean())
        self.df['region_win_rate'] = region_win_rate
        
        # Feature 5: Historical win rate by product type
        product_win_rate = self.df.groupby('product_type')['risk_outcome'].transform(lambda x: 1 - x.mean())
        self.df['product_win_rate'] = product_win_rate
        
        # Feature 6: Historical win rate by lead source
        lead_win_rate = self.df.groupby('lead_source')['risk_outcome'].transform(lambda x: 1 - x.mean())
        self.df['lead_source_win_rate'] = lead_win_rate
        
        # Feature 7: Sales rep historical performance
        rep_win_rate = self.df.groupby('sales_rep_id')['risk_outcome'].transform(lambda x: 1 - x.mean())
        self.df['rep_win_rate'] = rep_win_rate
        
        # Feature 8: Deal size relative to segment average
        segment_avg = self.df.groupby(['industry', 'product_type'])['deal_amount'].transform('median')
        self.df['deal_size_vs_segment'] = self.df['deal_amount'] / segment_avg
        
        # Feature 9: Deal stage encoding (ordinal)
        stage_order = {
            'Demo': 1,
            'Qualified': 2,
            'Proposal': 3,
            'Negotiation': 4,
            'Closed': 5
        }
        self.df['deal_stage_encoded'] = self.df['deal_stage'].map(stage_order)
        
        # Feature 10: Is Enterprise deal (typically longer cycles)
        self.df['is_enterprise'] = (self.df['product_type'] == 'Enterprise').astype(int)
        
        # Select features for modeling
        self.feature_names = [
            'sales_cycle_days_norm',
            'deal_amount_log',
            'industry_win_rate',
            'region_win_rate',
            'product_win_rate',
            'lead_source_win_rate',
            'rep_win_rate',
            'deal_size_vs_segment',
            'deal_stage_encoded',
            'is_enterprise'
        ]
        
        print(f"\n✓ Engineered {len(self.feature_names)} features:")
        for i, feat in enumerate(self.feature_names, 1):
            print(f"  {i}. {feat}")
        
        return self
    
    def train_model(self):
        """Train logistic regression model for risk scoring"""
        print("\n" + "=" * 80)
        print("MODEL TRAINING")
        print("=" * 80)
        
        # Prepare feature matrix and target
        X = self.df[self.feature_names].fillna(0)
        y = self.df['risk_outcome']
        
        # Split data (80/20 train/test)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\n✓ Training set: {len(X_train):,} deals")
        print(f"✓ Test set: {len(X_test):,} deals")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train logistic regression
        self.model = LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight='balanced'  # Handle class imbalance
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        print("\n✓ Model Performance on Test Set:")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Won', 'Lost']))
        
        print(f"\nROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.3f}")
        
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(f"                Predicted Won  Predicted Lost")
        print(f"Actual Won      {cm[0,0]:>13}  {cm[0,1]:>14}")
        print(f"Actual Lost     {cm[1,0]:>13}  {cm[1,1]:>14}")
        
        # Feature importance
        self.feature_importance = dict(zip(self.feature_names, self.model.coef_[0]))
        
        print("\n✓ Feature Importance (Logistic Regression Coefficients):")
        sorted_features = sorted(self.feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)
        for feat, coef in sorted_features:
            direction = "↑ INCREASES" if coef > 0 else "↓ DECREASES"
            print(f"  {feat:30s}: {coef:+.3f} {direction} risk")
        
        return self
    
    def score_deals(self):
        """Score all deals and generate risk scores"""
        print("\n" + "=" * 80)
        print("SCORING DEALS")
        print("=" * 80)
        
        # Prepare features
        X = self.df[self.feature_names].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        # Get risk probabilities (0-1 scale)
        risk_probabilities = self.model.predict_proba(X_scaled)[:, 1]
        
        # Convert to 0-100 risk score
        self.df['risk_score'] = (risk_probabilities * 100).round(1)
        
        # Categorize risk
        self.df['risk_category'] = pd.cut(
            self.df['risk_score'],
            bins=[0, 33, 66, 100],
            labels=['Low', 'Medium', 'High'],
            include_lowest=True
        )
        
        print(f"\n✓ Scored {len(self.df):,} deals")
        print(f"\n✓ Risk Score Distribution:")
        print(f"  - Mean: {self.df['risk_score'].mean():.1f}")
        print(f"  - Median: {self.df['risk_score'].median():.1f}")
        print(f"  - Min: {self.df['risk_score'].min():.1f}")
        print(f"  - Max: {self.df['risk_score'].max():.1f}")
        
        print(f"\n✓ Risk Category Distribution:")
        print(self.df['risk_category'].value_counts().to_string())
        
        return self
    
    def generate_actionable_insights(self):
        """Generate actionable insights and recommendations"""
        print("\n" + "=" * 80)
        print("ACTIONABLE INSIGHTS & RECOMMENDATIONS")
        print("=" * 80)
        
        # Identify high-risk deals (only those not yet closed or still in pipeline)
        # For this analysis, we'll focus on deals in earlier stages
        pipeline_deals = self.df[self.df['deal_stage'].isin(['Demo', 'Qualified', 'Proposal', 'Negotiation'])]
        high_risk_deals = pipeline_deals[pipeline_deals['risk_category'] == 'High'].sort_values('risk_score', ascending=False)
        
        print(f"\n🚨 HIGH-RISK DEALS REQUIRING IMMEDIATE ATTENTION:")
        print(f"   Total high-risk deals in pipeline: {len(high_risk_deals)}")
        
        if len(high_risk_deals) > 0:
            print(f"\n   Top 10 Highest Risk Deals:")
            top_risk = high_risk_deals.head(10)[['deal_id', 'risk_score', 'deal_amount', 'industry', 'sales_rep_id', 'deal_stage']]
            print(top_risk.to_string(index=False))
        
        # Analyze risk drivers
        print(f"\n📊 RISK DRIVER ANALYSIS:")
        
        # Which segments have highest average risk?
        print(f"\n   Average Risk Score by Industry:")
        industry_risk = self.df.groupby('industry')['risk_score'].mean().sort_values(ascending=False)
        print(industry_risk.to_string())
        
        print(f"\n   Average Risk Score by Lead Source:")
        lead_risk = self.df.groupby('lead_source')['risk_score'].mean().sort_values(ascending=False)
        print(lead_risk.to_string())
        
        # Sales reps with highest average deal risk
        print(f"\n   Sales Reps with Highest Average Deal Risk:")
        rep_risk = self.df.groupby('sales_rep_id').agg({
            'risk_score': 'mean',
            'deal_id': 'count'
        }).sort_values('risk_score', ascending=False).head(5)
        rep_risk.columns = ['avg_risk_score', 'deal_count']
        print(rep_risk.to_string())
        
        return self
    
    def export_results(self):
        """Export risk scores and insights"""
        print("\n" + "=" * 80)
        print("EXPORTING RESULTS")
        print("=" * 80)
        
        # Export scored deals
        output_cols = [
            'deal_id', 'created_date', 'closed_date', 'sales_rep_id',
            'industry', 'region', 'product_type', 'lead_source',
            'deal_stage', 'deal_amount', 'sales_cycle_days',
            'outcome', 'risk_score', 'risk_category'
        ]
        
        self.df[output_cols].to_csv('outputs/risk_scores.csv', index=False)
        print("\n✓ Saved: outputs/risk_scores.csv")
        
        # Generate detailed insights report
        report = self._generate_risk_report()
        with open('outputs/risk_scoring_report.md', 'w') as f:
            f.write(report)
        print("✓ Saved: outputs/risk_scoring_report.md")
        
        return self
    
    def _generate_risk_report(self):
        """Generate comprehensive risk scoring report"""
        
        # Calculate key metrics
        high_risk_count = (self.df['risk_category'] == 'High').sum()
        high_risk_value = self.df[self.df['risk_category'] == 'High']['deal_amount'].sum()
        
        # Top risk factors
        top_risk_factors = sorted(self.feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
        
        report = f"""# Deal Risk Scoring Report

## Executive Summary

This report presents the results of the Deal Risk Scoring Engine, which predicts the probability of deal loss to help sales teams prioritize intervention efforts.

**Model Performance**: ROC-AUC Score = {roc_auc_score(self.df['risk_outcome'], self.df['risk_score']/100):.3f}

---

## Risk Score Distribution

**Total Deals Analyzed**: {len(self.df):,}

| Risk Category | Count | Percentage | Total Value |
|---------------|-------|------------|-------------|
| Low (0-33) | {(self.df['risk_category'] == 'Low').sum():,} | {(self.df['risk_category'] == 'Low').mean():.1%} | ${self.df[self.df['risk_category'] == 'Low']['deal_amount'].sum():,.0f} |
| Medium (34-66) | {(self.df['risk_category'] == 'Medium').sum():,} | {(self.df['risk_category'] == 'Medium').mean():.1%} | ${self.df[self.df['risk_category'] == 'Medium']['deal_amount'].sum():,.0f} |
| High (67-100) | {high_risk_count:,} | {(self.df['risk_category'] == 'High').mean():.1%} | ${high_risk_value:,.0f} |

---

## Top Risk Factors

The following features have the strongest impact on deal risk:

"""
        
        for i, (feature, coef) in enumerate(top_risk_factors, 1):
            impact = "INCREASES" if coef > 0 else "DECREASES"
            report += f"{i}. **{feature}**: Coefficient = {coef:+.3f} ({impact} risk)\n"
        
        report += f"""

### Interpretation

- **Positive coefficients**: Higher values INCREASE risk of loss
- **Negative coefficients**: Higher values DECREASE risk of loss (protective factors)

---

## High-Risk Deals Requiring Attention

Pipeline deals (Demo, Qualified, Proposal, Negotiation stages) with high risk scores:

"""
        
        pipeline_deals = self.df[self.df['deal_stage'].isin(['Demo', 'Qualified', 'Proposal', 'Negotiation'])]
        high_risk_pipeline = pipeline_deals[pipeline_deals['risk_category'] == 'High'].sort_values('risk_score', ascending=False)
        
        if len(high_risk_pipeline) > 0:
            report += f"**Total High-Risk Pipeline Deals**: {len(high_risk_pipeline)}\n\n"
            report += "| Deal ID | Risk Score | Amount | Industry | Rep | Stage |\n"
            report += "|---------|------------|--------|----------|-----|-------|\n"
            
            for _, row in high_risk_pipeline.head(15).iterrows():
                report += f"| {row['deal_id']} | {row['risk_score']:.1f} | ${row['deal_amount']:,.0f} | {row['industry']} | {row['sales_rep_id']} | {row['deal_stage']} |\n"
        else:
            report += "*No high-risk deals currently in pipeline.*\n"
        
        report += """

---

## Recommended Actions

### Immediate (This Week)

1. **Sales Manager Review**: Schedule 1-on-1 reviews for all deals with risk score > 80
2. **Executive Engagement**: Involve executives in top 5 highest-risk, high-value deals
3. **Deal Acceleration**: For high-risk deals, implement acceleration tactics:
   - Reduce POC scope
   - Offer limited-time incentives
   - Schedule executive business reviews

### Short-Term (This Month)

1. **Rep Coaching**: Focus coaching on reps with consistently high average deal risk
2. **Lead Source Optimization**: Reduce investment in lead sources with highest risk scores
3. **Segment Strategy**: Develop specialized playbooks for high-risk industries

### Strategic (This Quarter)

1. **Predictive Alerts**: Implement automated alerts when deals cross risk thresholds
2. **A/B Testing**: Test intervention strategies and measure impact on risk scores
3. **Model Refinement**: Incorporate additional signals (email engagement, meeting frequency, etc.)

---

## How Sales Leaders Should Use This System

### Weekly Pipeline Reviews

1. Sort pipeline by risk score (highest first)
2. For each high-risk deal, ask:
   - What specific factors are driving the risk?
   - What intervention can we apply this week?
   - Should we disqualify and reallocate rep time?

### Rep Performance Management

1. Track average risk score of each rep's pipeline
2. High average risk may indicate:
   - Poor qualification
   - Weak discovery
   - Ineffective deal management
3. Use for targeted coaching

### Strategic Planning

1. Monitor risk trends by segment
2. Adjust go-to-market strategy based on risk patterns
3. Allocate resources to lowest-risk, highest-value opportunities

---

## Limitations & Caveats

1. **Historical Data Dependency**: Model assumes past patterns predict future outcomes
2. **Missing Qualitative Factors**: Cannot capture relationship quality, competitive dynamics
3. **Data Quality**: Accuracy depends on CRM data hygiene
4. **Model Drift**: Requires periodic retraining as sales process evolves
5. **Self-Fulfilling Prophecy**: Risk of teams abandoning high-risk deals prematurely

---

*Report generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return report

def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("SKYGENI SALES INTELLIGENCE - DEAL RISK SCORING ENGINE")
    print("=" * 80)
    
    # Initialize engine
    engine = DealRiskScoringEngine('data/skygeni_sales_data.csv')
    
    # Run risk scoring pipeline
    (engine
     .load_and_prepare_data()
     .engineer_features()
     .train_model()
     .score_deals()
     .generate_actionable_insights()
     .export_results())
    
    print("\n" + "=" * 80)
    print("RISK SCORING COMPLETE")
    print("=" * 80)
    print("\n✓ Outputs generated:")
    print("  - outputs/risk_scores.csv")
    print("  - outputs/risk_scoring_report.md")
    print("\n✓ Next step: Review system architecture (docs/system_architecture.md)")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
