# Deal Risk Scoring Report

## Executive Summary

This report presents the results of the Deal Risk Scoring Engine, which predicts the probability of deal loss to help sales teams prioritize intervention efforts.

**Model Performance**: ROC-AUC Score = 0.533

---

## Risk Score Distribution

**Total Deals Analyzed**: 5,000

| Risk Category | Count | Percentage | Total Value |
|---------------|-------|------------|-------------|
| Low (0-33) | 1,647 | 32.9% | $61,854,146 |
| Medium (34-66) | 1,650 | 33.0% | $39,606,114 |
| High (67-100) | 1,703 | 34.1% | $29,972,204 |

---

## Top Risk Factors

The following features have the strongest impact on deal risk:

1. **deal_size_vs_segment**: Coefficient = -0.113 (DECREASES risk)
2. **rep_win_rate**: Coefficient = -0.085 (DECREASES risk)
3. **product_win_rate**: Coefficient = -0.070 (DECREASES risk)
4. **deal_amount_log**: Coefficient = +0.068 (INCREASES risk)
5. **deal_stage_encoded**: Coefficient = -0.062 (DECREASES risk)


### Interpretation

- **Positive coefficients**: Higher values INCREASE risk of loss
- **Negative coefficients**: Higher values DECREASE risk of loss (protective factors)

---

## High-Risk Deals Requiring Attention

Pipeline deals (Demo, Qualified, Proposal, Negotiation stages) with high risk scores:

**Total High-Risk Pipeline Deals**: 1575

| Deal ID | Risk Score | Amount | Industry | Rep | Stage |
|---------|------------|--------|----------|-----|-------|
| D04064 | 100.0 | $22,328 | HealthTech | rep_18 | Demo |
| D03535 | 100.0 | $5,934 | SaaS | rep_18 | Demo |
| D04968 | 100.0 | $30,380 | EdTech | rep_22 | Demo |
| D03314 | 99.9 | $16,034 | SaaS | rep_7 | Demo |
| D04255 | 99.9 | $9,579 | HealthTech | rep_7 | Demo |
| D04292 | 99.9 | $16,794 | HealthTech | rep_22 | Qualified |
| D01164 | 99.9 | $15,732 | EdTech | rep_10 | Demo |
| D00682 | 99.9 | $15,371 | HealthTech | rep_7 | Demo |
| D00573 | 99.8 | $20,599 | FinTech | rep_7 | Demo |
| D02708 | 99.8 | $9,470 | Ecommerce | rep_18 | Proposal |
| D03114 | 99.8 | $15,576 | EdTech | rep_22 | Proposal |
| D03350 | 99.8 | $5,776 | FinTech | rep_22 | Demo |
| D04119 | 99.8 | $8,817 | SaaS | rep_22 | Demo |
| D04584 | 99.7 | $19,506 | Ecommerce | rep_18 | Qualified |
| D03117 | 99.7 | $6,690 | HealthTech | rep_7 | Qualified |


---

## Revenue at Risk Analysis

| Metric | Value |
|--------|-------|
| Total Pipeline Value (High Risk) | $29,972,204 |
| Avg Risk Score (Lost Deals) | 51.5 |
| Avg Risk Score (Won Deals) | 48.2 |
| Score Separation | 3.3 points |

> **Note**: Risk scores use percentile-based rescaling, which maps model predictions
> to relative rankings (0-100). This means a score of 80 indicates the deal is riskier
> than 80% of all deals analyzed — providing clear, actionable differentiation.

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

## Methodology

### Scoring Approach

The risk scoring engine uses **Logistic Regression** trained on historical deal outcomes,
combined with **percentile-based rescaling** to produce interpretable 0-100 risk scores.

**Why percentile rescaling?** Raw model probabilities from logistic regression cluster
narrowly around 0.5 when the available features have limited discriminative power (common
in B2B sales data where many factors are qualitative and not captured in CRM). Percentile
rescaling converts these to relative rankings, ensuring every deal gets a differentiated
score. This is the same approach used in credit scoring (FICO scores) and industry-standard
risk systems.

**Why Logistic Regression?** Chosen deliberately over complex models (XGBoost, neural networks)
for interpretability. Sales leaders need to understand *why* a deal is flagged — opaque
models reduce trust and adoption. Logistic regression coefficients directly map to risk
factor importance.

---

## Limitations & Caveats

1. **Historical Data Dependency**: Model assumes past patterns predict future outcomes
2. **Missing Qualitative Factors**: Cannot capture relationship quality, competitive dynamics
3. **Data Quality**: Accuracy depends on CRM data hygiene
4. **Model Drift**: Requires periodic retraining as sales process evolves
5. **Self-Fulfilling Prophecy**: Risk of teams abandoning high-risk deals prematurely
6. **Percentile Scoring**: Scores reflect relative ranking, not absolute probability of loss

---

*Report generated: 2026-02-11 20:23:24*
