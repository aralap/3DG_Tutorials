#!/usr/bin/env python3
"""
Standalone script for performing COX multiple regression analysis.
This can be run independently or used as a reference for the tutorial.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from lifelines import CoxPHFitter, KaplanMeierFitter
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Set style for plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_data(data_path='../data/sample_survival_data.csv'):
    """Load survival data from CSV file."""
    data = pd.read_csv(data_path)
    print(f"Data loaded successfully! Shape: {data.shape}")
    return data

def preprocess_data(data):
    """Preprocess data for COX regression."""
    print("\n=== Data Preprocessing ===")
    
    # Check for missing values
    print("\nMissing values:")
    print(data.isnull().sum())
    
    # Handle missing values
    data = data.dropna()
    print(f"\nData shape after handling missing values: {data.shape}")
    
    # Encode categorical variables
    le_gender = LabelEncoder()
    le_treatment = LabelEncoder()
    
    data['gender_encoded'] = le_gender.fit_transform(data['gender'])
    data['treatment_encoded'] = le_treatment.fit_transform(data['treatment'])
    
    print("\nCategorical encoding:")
    print(f"Gender: {dict(zip(le_gender.classes_, le_gender.transform(le_gender.classes_)))}")
    print(f"Treatment: {dict(zip(le_treatment.classes_, le_treatment.transform(le_treatment.classes_)))}")
    
    return data, le_gender, le_treatment

def explore_data(data):
    """Explore the survival data."""
    print("\n=== Data Exploration ===")
    
    print("\nFirst 5 rows:")
    print(data[['patient_id', 'survival_time', 'event', 'age', 'gender', 'treatment']].head())
    
    print("\nData summary:")
    print(data[['survival_time', 'event', 'age', 'biomarker1', 'biomarker2']].describe())
    
    print(f"\nEvent rate: {data['event'].sum()}/{len(data)} ({100*data['event'].sum()/len(data):.1f}%)")
    
    print("\nDistribution by gender:")
    print(data.groupby('gender')['event'].agg(['count', 'sum']))
    
    print("\nDistribution by treatment:")
    print(data.groupby('treatment')['event'].agg(['count', 'sum']))

def fit_cox_model(data):
    """Fit Cox Proportional Hazards model."""
    print("\n=== COX Regression Analysis ===")
    
    # Prepare data for Cox model
    cox_data = data[['survival_time', 'event', 'age', 'gender_encoded', 
                     'treatment_encoded', 'biomarker1', 'biomarker2']].copy()
    
    # Rename columns for clarity
    cox_data.columns = ['duration', 'event', 'age', 'gender', 
                        'treatment', 'biomarker1', 'biomarker2']
    
    # Initialize and fit Cox model
    cph = CoxPHFitter()
    cph.fit(cox_data, duration_col='duration', event_col='event')
    
    # Print summary
    print("\nCOX Regression Results:")
    print("=" * 80)
    cph.print_summary()
    print("=" * 80)
    
    return cph, cox_data

def plot_hazard_ratios(cph):
    """Plot hazard ratios from Cox model."""
    print("\n=== Plotting Hazard Ratios ===")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    cph.plot(ax=ax)
    ax.set_title('Hazard Ratios with 95% Confidence Intervals', fontsize=14, fontweight='bold')
    ax.axvline(x=1, color='red', linestyle='--', alpha=0.5, label='No effect (HR=1)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/hazard_ratios.png', dpi=300, bbox_inches='tight')
    print("Saved: results/hazard_ratios.png")
    plt.show()

def plot_kaplan_meier(data):
    """Plot Kaplan-Meier survival curves."""
    print("\n=== Kaplan-Meier Survival Curves ===")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # By gender
    kmf = KaplanMeierFitter()
    ax1 = axes[0]
    for gender in data['gender'].unique():
        mask = data['gender'] == gender
        kmf.fit(data[mask]['survival_time'], 
                data[mask]['event'], 
                label=f'{gender}')
        kmf.plot_survival_function(ax=ax1)
    ax1.set_title('Kaplan-Meier Curves by Gender', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Time (days)')
    ax1.set_ylabel('Survival Probability')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # By treatment
    kmf = KaplanMeierFitter()
    ax2 = axes[1]
    for treatment in sorted(data['treatment'].unique()):
        mask = data['treatment'] == treatment
        kmf.fit(data[mask]['survival_time'], 
                data[mask]['event'], 
                label=f'Treatment {treatment}')
        kmf.plot_survival_function(ax=ax2)
    ax2.set_title('Kaplan-Meier Curves by Treatment', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Time (days)')
    ax2.set_ylabel('Survival Probability')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('../results/kaplan_meier_curves.png', dpi=300, bbox_inches='tight')
    print("Saved: results/kaplan_meier_curves.png")
    plt.show()

def check_proportional_hazards(cph, data):
    """Check proportional hazards assumption."""
    print("\n=== Checking Proportional Hazards Assumption ===")
    
    try:
        # This will print warnings if assumption is violated
        cph.check_assumptions(data, p_value_threshold=0.05, show_plots=True)
        print("\nProportional hazards assumption checked.")
    except Exception as e:
        print(f"\nWarning: Could not complete PH check: {e}")
        print("This is normal if the test requires specific conditions.")

def main():
    """Main analysis pipeline."""
    print("=" * 80)
    print("COX Multiple Regression Analysis")
    print("=" * 80)
    
    # Create results directory
    import os
    os.makedirs('../results', exist_ok=True)
    
    # Load data
    data = load_data()
    
    # Preprocess
    data, le_gender, le_treatment = preprocess_data(data)
    
    # Explore
    explore_data(data)
    
    # Fit Cox model
    cph, cox_data = fit_cox_model(data)
    
    # Visualize
    plot_hazard_ratios(cph)
    plot_kaplan_meier(data)
    
    # Check assumptions
    check_proportional_hazards(cph, cox_data)
    
    print("\n" + "=" * 80)
    print("Analysis Complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()

