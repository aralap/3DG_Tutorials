# COX Multiple Regression Tutorial

A comprehensive step-by-step tutorial on performing Cox Proportional Hazards Multiple Regression for survival analysis.

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Quick Start with Google Colab](#quick-start-with-google-colab)
4. [Step-by-Step Guide](#step-by-step-guide)
5. [Understanding the Data](#understanding-the-data)
6. [Running the Analysis](#running-the-analysis)
7. [Interpreting Results](#interpreting-results)
8. [Resources](#resources)

## 🔬 Introduction

Cox Proportional Hazards Regression (also known as Cox multiple regression) is a statistical method used to analyze survival data and assess the relationship between multiple predictor variables and the time until an event occurs (e.g., death, disease progression, treatment failure).

**Key Features:**
- Handles censored data (subjects who haven't experienced the event during the study period)
- Can include multiple covariates simultaneously
- Provides hazard ratios for each predictor
- Assumes proportional hazards over time

## 🎯 Prerequisites

- Basic understanding of statistics and survival analysis
- Python 3.7+ installed (for local execution)
- OR Google Colab account (recommended for beginners)

**Required Python Packages:**
- pandas
- numpy
- lifelines
- matplotlib
- seaborn
- scipy

## 🚀 Quick Start with Google Colab

The easiest way to run this tutorial is through Google Colab:

### **Option 1: Direct Colab Link**
👉 **[Open Tutorial in Google Colab](https://colab.research.google.com/github/aralap/3DG_Tutorials/blob/main/tutorials/COX_Regression_Tutorial.ipynb)**

### **Option 2: Manual Setup**
1. Go to [Google Colab](https://colab.research.google.com/)
2. Click `File` → `Upload notebook`
3. Upload `tutorials/COX_Regression_Tutorial.ipynb`
4. Or use the GitHub option and navigate to this repository

### **Option 3: Using gdown (if files are in Google Drive)**
See the notebook for instructions on downloading sample data from Google Drive.

## 📚 Step-by-Step Guide

### Step 1: Load and Explore the Data

Our sample dataset contains:
- **Survival time**: Time until event or censoring
- **Event status**: 1 = event occurred, 0 = censored
- **Predictor variables**: Age, Gender, Treatment, Biomarker levels

```python
import pandas as pd
import numpy as np

# Load data
data = pd.read_csv('data/sample_survival_data.csv')
metadata = pd.read_csv('data/sample_metadata.csv')

print(data.head())
print(data.describe())
```

### Step 2: Data Preprocessing

```python
# Check for missing values
print(data.isnull().sum())

# Handle missing values if any
data = data.dropna()

# Check data types
print(data.dtypes)

# Encode categorical variables if needed
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data['Gender'] = le.fit_transform(data['Gender'])
```

### Step 3: Perform Cox Regression

```python
from lifelines import CoxPHFitter

# Initialize the Cox model
cph = CoxPHFitter()

# Fit the model with multiple covariates
cph.fit(data, duration_col='survival_time', event_col='event')

# Print summary
cph.print_summary()
```

### Step 4: Visualize Results

```python
# Plot hazard ratios
cph.plot()

# Kaplan-Meier curves stratified by predictor
from lifelines import KaplanMeierFitter
kmf = KaplanMeierFitter()

# Example: Compare survival by treatment group
for treatment in data['Treatment'].unique():
    mask = data['Treatment'] == treatment
    kmf.fit(data[mask]['survival_time'], 
            data[mask]['event'], 
            label=f'Treatment {treatment}')
    kmf.plot_survival_function()
```

### Step 5: Check Proportional Hazards Assumption

```python
# Schoenfeld residuals test
cph.check_assumptions(data, p_value_threshold=0.05, show_plots=True)
```

## 📊 Understanding the Data

### Sample Data Files

1. **`data/sample_survival_data.csv`**
   - Main dataset with survival times, events, and covariates
   - Contains 500 simulated patient records

2. **`data/sample_metadata.csv`**
   - Description of variables and their meanings
   - Data collection protocols
   - Variable units and ranges

### Data Structure

| Column | Description | Type | Values |
|--------|-------------|------|--------|
| `patient_id` | Unique patient identifier | Integer | 1-500 |
| `survival_time` | Time until event or censoring | Float | Days |
| `event` | Event status | Binary | 0 (censored), 1 (event) |
| `age` | Patient age | Integer | Years |
| `gender` | Patient gender | Categorical | Male, Female |
| `treatment` | Treatment group | Categorical | A, B, C |
| `biomarker1` | Biomarker level 1 | Float | Continuous |
| `biomarker2` | Biomarker level 2 | Float | Continuous |

## 🔍 Running the Analysis

### Option A: Google Colab (Recommended)

1. Click the Colab link above
2. The notebook will automatically install dependencies
3. Data files are included in the repository or can be loaded from GitHub
4. Run cells sequentially using `Shift + Enter`

### Option B: Local Python Environment

1. Clone this repository:
```bash
git clone https://github.com/aralap/3DG_Tutorials.git
cd 3DG_Tutorials
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the tutorial notebook:
```bash
jupyter notebook tutorials/COX_Regression_Tutorial.ipynb
```

OR run the standalone script:
```bash
python scripts/cox_regression_analysis.py
```

## 📈 Interpreting Results

### Hazard Ratio (HR)

- **HR = 1**: No effect on survival
- **HR > 1**: Increased hazard (worse survival)
- **HR < 1**: Decreased hazard (better survival)

### Example Interpretation

If Treatment B has HR = 0.65 with 95% CI [0.45, 0.94] and p < 0.05:
- Treatment B reduces the hazard of the event by 35% compared to the reference
- The effect is statistically significant

### Model Fit Statistics

- **Concordance Index (C-index)**: Similar to AUC; >0.7 indicates good discrimination
- **Log-likelihood**: Lower is better (used for model comparison)
- **AIC (Akaike Information Criterion)**: Lower is better (model selection)

## 📁 Project Structure

```
3DG_Tutorials/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore file
│
├── data/                              # Sample data directory
│   ├── sample_survival_data.csv       # Main survival dataset
│   └── sample_metadata.csv            # Data documentation
│
├── tutorials/                         # Tutorial notebooks
│   └── COX_Regression_Tutorial.ipynb  # Main Colab-compatible notebook
│
└── scripts/                           # Python scripts
    └── cox_regression_analysis.py     # Standalone analysis script
```

## 🔗 Resources

### Recommended Reading

- Cox, D. R. (1972). Regression models and life-tables. *Journal of the Royal Statistical Society: Series B*, 34(2), 187-202.
- [Lifelines Documentation](https://lifelines.readthedocs.io/)
- [Survival Analysis Guide](https://www.statsdirect.com/help/survival_analysis/cox_regression.htm)

### Useful Tools

- [Google Colab](https://colab.research.google.com/) - Free Jupyter notebook environment
- [Lifelines Python Package](https://lifelines.readthedocs.io/) - Survival analysis library
- [R Survival Package](https://cran.r-project.org/web/packages/survival/index.html) - Alternative in R

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This tutorial is provided for educational purposes. Feel free to use and modify as needed.

## ❓ FAQ

**Q: What is the difference between Cox regression and logistic regression?**
A: Cox regression analyzes time-to-event data with censoring, while logistic regression predicts binary outcomes at a fixed time point.

**Q: Can I use Cox regression with non-proportional hazards?**
A: The basic Cox model assumes proportional hazards. If violated, consider time-dependent covariates or stratified models.

**Q: How do I handle missing data?**
A: Common approaches include complete case analysis, multiple imputation, or sensitivity analyses. See the tutorial for examples.

**Q: What sample size do I need?**
A: General rule: at least 10-20 events per predictor variable. For 3 predictors, aim for 30-60 events minimum.

---

**Happy Analyzing! 📊**

For questions or issues, please open an issue on GitHub.

