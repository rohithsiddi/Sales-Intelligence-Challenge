# SkyGeni Sales Intelligence - Setup Instructions

## Installation Options

Due to system permission restrictions, here are alternative ways to set up the environment:

### Option 1: Using uv (Recommended)
```bash
# Clear uv cache if needed
rm -rf ~/.cache/uv

# Create virtual environment
uv venv

# Activate environment
source .venv/bin/activate

# Install dependencies
uv pip install pandas numpy scikit-learn matplotlib seaborn plotly jupyter
```

### Option 2: Using Python venv
```bash
# Create virtual environment in a different location
python3 -m venv ~/skygeni_venv

# Activate environment
source ~/skygeni_venv/bin/activate

# Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn plotly jupyter
```

### Option 3: Using Conda/Miniconda
```bash
# Create conda environment
conda create -n skygeni python=3.9

# Activate environment
conda activate skygeni

# Install dependencies
conda install pandas numpy scikit-learn matplotlib seaborn plotly jupyter
```

## Running the Analysis

Once dependencies are installed:

```bash
# Run exploratory data analysis
python src/eda_analysis.py

# Run risk scoring engine
python src/risk_scoring_engine.py
```

## Quick Test

To verify installation:
```bash
python -c "import pandas, numpy, sklearn, matplotlib, seaborn, plotly; print('All packages installed successfully!')"
```
