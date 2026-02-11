# Manual Setup Instructions - Permission Issues Encountered

## Problem
Automated setup using `uv` failed due to system permission restrictions:
- Cannot create `.venv` directory in project folder
- Cannot write to uv cache (`~/.cache/uv`)
- Cannot install to system Python or conda environment

## Solution: Manual Setup Required

### Option 1: Using uv (Recommended)

```bash
# Navigate to home directory to avoid permission issues
cd ~

# Create virtual environment in home directory
uv venv skygeni_env

# Activate the environment
source ~/skygeni_env/bin/activate

# Install dependencies
uv pip install pandas numpy scikit-learn matplotlib seaborn plotly

# Navigate to project and run scripts
cd /Users/rohithsiddi/Desktop/SkyGeni
python src/eda_analysis.py
python src/risk_scoring_engine.py
```

### Option 2: Using Standard Python venv

```bash
# Create virtual environment in home directory
python3 -m venv ~/skygeni_env

# Activate
source ~/skygeni_env/bin/activate

# Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn plotly

# Navigate to project and run scripts
cd /Users/rohithsiddi/Desktop/SkyGeni
python src/eda_analysis.py
python src/risk_scoring_engine.py
```

### Option 3: Using Existing Conda/Miniforge

```bash
# Create new conda environment
conda create -n skygeni python=3.9 -y

# Activate
conda activate skygeni

# Install dependencies
conda install pandas numpy scikit-learn matplotlib seaborn plotly -y

# Navigate to project and run scripts
cd /Users/rohithsiddi/Desktop/SkyGeni
python src/eda_analysis.py
python src/risk_scoring_engine.py
```

## Expected Outputs After Running Scripts

### From `eda_analysis.py`:
- `outputs/visualizations/eda_overview.png` - 6-panel analysis dashboard
- `outputs/visualizations/deal_velocity_analysis.png` - Velocity distribution chart
- `outputs/insights_report.md` - Business insights and recommendations

### From `risk_scoring_engine.py`:
- `outputs/risk_scores.csv` - All deals with risk scores (0-100)
- `outputs/risk_scoring_report.md` - Comprehensive risk analysis report

## Verification

After running both scripts, verify outputs exist:
```bash
ls -la outputs/
ls -la outputs/visualizations/
```

You should see 4 new files total.
