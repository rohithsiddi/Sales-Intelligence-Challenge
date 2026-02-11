# SkyGeni Sales Intelligence Challenge

## Project Overview

This project builds a **decision intelligence system** to help a B2B SaaS CRO diagnose why win rates have dropped over the last two quarters and provide actionable insights for improving sales performance.

**Challenge Context**: A B2B SaaS company's CRO reports: *"Our win rate has dropped over the last two quarters, but pipeline volume looks healthy. I don't know what exactly is going wrong or what my team should focus on."*

---

## Part 1: Problem Framing

### The Real Business Problem

The surface-level issue is a **declining win rate**, but the deeper business problem is **inefficient resource allocation in the sales process**. The CRO faces three critical challenges:

1. **Diagnostic Gap**: Unable to pinpoint which factors are driving the win rate decline
2. **Action Paralysis**: Unclear which interventions would have the highest impact
3. **Resource Misallocation**: Sales teams may be investing time in deals unlikely to close while neglecting high-potential opportunities

The real problem isn't just *knowing* the win rate is down—it's **not knowing where to focus limited sales resources** to reverse the trend.

### Key Questions the AI System Should Answer

1. **Segmentation Analysis**:
   - Which segments (industry, region, product type) are experiencing the steepest win rate decline?
   - Are there segments that are actually improving despite the overall trend?

2. **Deal Quality vs. Quantity**:
   - Is pipeline volume masking a decline in deal quality?
   - Are we pursuing the right types of deals, or has our ideal customer profile shifted?

3. **Sales Process Efficiency**:
   - Where in the sales funnel are deals falling off?
   - Which sales stages show the most significant degradation?

4. **Resource Optimization**:
   - Which open deals are at highest risk of loss?
   - Where should sales managers focus coaching and intervention efforts?

5. **Leading Indicators**:
   - What early warning signals predict deal failure?
   - Can we identify at-risk deals before they reach late stages?

### Metrics That Matter Most

#### Standard Metrics
- **Win Rate by Segment**: Overall and by industry, region, product type, lead source
- **Sales Cycle Length**: Time from creation to close, by outcome
- **Deal Velocity**: Speed of progression through pipeline stages
- **Pipeline Coverage**: Ratio of pipeline value to quota

#### Custom Metrics (Designed for This Analysis)

**1. Deal Velocity Score**
- **Definition**: Normalized measure of how quickly a deal progresses relative to segment benchmarks
- **Formula**: `(Expected Days to Close - Actual Days) / Expected Days`
- **Why It Matters**: Identifies deals moving unusually slow (risk indicator) or fast (high intent)
- **Action**: Prioritize slow-moving deals for intervention or disqualification

**2. Pipeline Health Index**
- **Definition**: Composite score combining win rate trend, deal quality, and stage progression
- **Components**: 
  - Win rate momentum (30%)
  - Average deal size trend (30%)
  - Stage conversion rates (40%)
- **Why It Matters**: Single number to track overall pipeline health beyond just volume
- **Action**: Triggers strategic reviews when index drops below threshold

### Assumptions

**Data Assumptions**:
1. The provided dataset is representative of the actual CRM data
2. Deal outcomes (won/lost) are accurately recorded
3. Closed dates reflect actual close dates, not data entry dates
4. Deal amounts represent Annual Contract Value (ACV)

**Business Assumptions**:
1. The sales process and stages are consistent across all deals
2. Sales reps have similar territories and quotas (or differences are accounted for)
3. The company's product/market fit hasn't fundamentally changed
4. External market conditions (economy, competition) are relatively stable
5. CRM data hygiene is maintained (no systematic data quality issues)

**Analytical Assumptions**:
1. Historical patterns are predictive of future outcomes
2. Correlation between features and outcomes indicates causation (with business validation)
3. The two-quarter timeframe is sufficient to identify meaningful trends
4. Sample size is adequate for statistical significance in segment analysis

---

## How to Run This Project

### Prerequisites
- Python 3.9+
- Required packages: pandas, numpy, scipy, scikit-learn, matplotlib, seaborn, plotly

### Installation

```bash
# Clone the repository
git clone https://github.com/rohithsiddi/-Sales-Intelligence-Challenge.git
cd SkyGeni

# Install dependencies (using uv)
uv sync

# Or using pip
pip install pandas numpy scipy scikit-learn matplotlib seaborn plotly jupyter
```

### Execution

```bash
# Run exploratory data analysis
python src/eda_analysis.py

# Run risk scoring engine
python src/risk_scoring_engine.py

# View outputs
ls outputs/visualizations/
cat outputs/insights_report.md
```

---

## Project Structure

```
SkyGeni/
├── README.md                          # This file
├── pyproject.toml                     # Dependencies (uv)
├── .gitignore                         # Git ignore rules
├── data/
│   └── skygeni_sales_data.csv        # Sales dataset (5000 deals)
├── src/
│   ├── eda_analysis.py               # Exploratory data analysis
│   ├── risk_scoring_engine.py        # Deal risk scoring model
│   └── utils.py                      # Helper functions
├── outputs/
│   ├── visualizations/               # Generated charts
│   ├── insights_report.md            # Business insights
│   ├── risk_scoring_report.md        # Risk scoring results
│   └── risk_scores.csv               # Scored deals
└── docs/
    ├── system_architecture.md        # System design
    └── reflection.md                 # Critical reflection
```

---

## Solution Approach

This project implements **Option A: Deal Risk Scoring** to help sales teams prioritize intervention efforts on deals most likely to be lost.

### Key Components

1. **Part 1: Problem Framing** ✓ (This document)
2. **Part 2: Data Exploration & Insights** (See `outputs/insights_report.md`)
3. **Part 3: Deal Risk Scoring Engine** (See `src/risk_scoring_engine.py`)
4. **Part 4: System Design** (See `docs/system_architecture.md`)
5. **Part 5: Reflection** (See `docs/reflection.md`)

---

## Key Decisions

### Why Deal Risk Scoring (Option A)?
- **Most actionable**: Sales teams can immediately use risk scores to prioritize deals
- **Clear ROI**: Preventing even a few deal losses justifies the investment
- **Interpretable**: Can explain *why* a deal is at risk, not just *that* it is
- **Scalable**: Works for any pipeline size and can run continuously

### Why Logistic Regression + Percentile Rescaling?
- **Interpretability**: Can explain feature importance to sales leaders
- **Speed**: Fast training and scoring for real-time use
- **Percentile rescaling**: Converts raw model probabilities to relative rankings (0-100), ensuring well-distributed scores even with limited signal — the same approach used in credit scoring (FICO)
- **Robust**: Less prone to overfitting than complex models

### Design Philosophy
- **Business value over technical complexity**: Focus on actionable insights
- **Transparency over black-box accuracy**: Sales leaders need to trust the system
- **Practical over perfect**: Ship something useful quickly, iterate based on feedback

---

## Next Steps

See `docs/reflection.md` for detailed discussion of:
- Weakest assumptions and how to validate them
- Production deployment considerations
- 1-month roadmap for enhancements
- Areas requiring further research

---

