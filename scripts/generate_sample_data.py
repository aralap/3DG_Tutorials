#!/usr/bin/env python3
"""
Script to generate sample survival data for COX regression tutorial.
This can be run independently or imported into the tutorial notebook.
"""

import pandas as pd
import numpy as np

def generate_sample_survival_data(n_samples=500, random_seed=42):
    """
    Generate synthetic survival data for COX regression analysis.
    
    Parameters:
    -----------
    n_samples : int
        Number of patients to simulate
    random_seed : int
        Random seed for reproducibility
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with survival data
    """
    np.random.seed(random_seed)
    
    # Generate patient IDs
    patient_ids = range(1, n_samples + 1)
    
    # Generate age (30-80 years)
    age = np.random.randint(30, 81, n_samples)
    
    # Generate gender (categorical)
    gender = np.random.choice(['Male', 'Female'], n_samples, p=[0.55, 0.45])
    
    # Generate treatment groups (A, B, C)
    treatment = np.random.choice(['A', 'B', 'C'], n_samples, p=[0.35, 0.35, 0.30])
    
    # Generate biomarker levels
    biomarker1 = np.random.normal(50, 15, n_samples)
    biomarker2 = np.random.normal(100, 25, n_samples)
    
    # Generate survival times based on covariates
    # Treatment B has better survival, higher age increases risk, biomarker1 affects survival
    baseline_hazard = 0.02
    treatment_effect = np.where(treatment == 'B', 0.5, np.where(treatment == 'A', 0.8, 1.0))
    age_effect = age / 80
    biomarker_effect = biomarker1 / 100
    
    # Generate hazard rates
    hazard_rate = baseline_hazard * treatment_effect * (1 + age_effect * 0.5) * (1 + biomarker_effect * 0.3)
    
    # Generate survival times (exponential distribution)
    survival_time = np.random.exponential(1 / hazard_rate)
    
    # Cap maximum survival time at 1825 days (5 years)
    survival_time = np.minimum(survival_time, 1825)
    
    # Generate censoring (30% censoring rate)
    censoring_time = np.random.uniform(365, 1825, n_samples)
    event = (survival_time <= censoring_time).astype(int)
    survival_time_observed = np.where(event == 1, survival_time, censoring_time)
    
    # Create DataFrame
    data = pd.DataFrame({
        'patient_id': patient_ids,
        'survival_time': survival_time_observed,
        'event': event,
        'age': age,
        'gender': gender,
        'treatment': treatment,
        'biomarker1': np.round(biomarker1, 2),
        'biomarker2': np.round(biomarker2, 2)
    })
    
    return data

if __name__ == "__main__":
    # Generate data
    data = generate_sample_survival_data(n_samples=500, random_seed=42)
    
    # Save to CSV
    output_path = '../data/sample_survival_data.csv'
    data.to_csv(output_path, index=False)
    
    print('Sample survival data created successfully!')
    print(f'Output file: {output_path}')
    print(f'Shape: {data.shape}')
    print(f'Events: {data["event"].sum()}/{len(data)} ({100*data["event"].sum()/len(data):.1f}%)')
    print('\nFirst 5 rows:')
    print(data.head())
    print('\nData summary:')
    print(data.describe())

