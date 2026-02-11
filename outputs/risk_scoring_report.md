# Deal Risk Scoring Report

## Executive Summary

This report presents the results of the Deal Risk Scoring Engine, which predicts the probability of deal loss to help sales teams prioritize intervention efforts.

**Model Performance**: ROC-AUC Score = 0.533

---

## Risk Score Distribution

**Total Deals Analyzed**: 5,000

| Risk Category | Count | Percentage | Total Value |
|---------------|-------|------------|-------------|
| Low (0-33) | 0 | 0.0% | $0 |
| Medium (34-66) | 5,000 | 100.0% | $131,432,464 |
| High (67-100) | 0 | 0.0% | $0 |

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

*No high-risk deals currently in pipeline.*


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
