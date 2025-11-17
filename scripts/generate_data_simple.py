#!/usr/bin/env python3
"""
Simple script to generate sample survival data CSV without pandas dependency.
"""

import csv
import random
import math

# Set random seed for reproducibility
random.seed(42)

def generate_sample_data(n_samples=500, output_file='../data/sample_survival_data.csv'):
    """Generate synthetic survival data and save as CSV."""
    
    # Initialize data list with headers
    data = [['patient_id', 'survival_time', 'event', 'age', 'gender', 'treatment', 'biomarker1', 'biomarker2']]
    
    for i in range(1, n_samples + 1):
        # Generate patient ID
        patient_id = i
        
        # Generate age (30-80 years)
        age = random.randint(30, 80)
        
        # Generate gender (categorical)
        gender = random.choice(['Male', 'Female'])
        
        # Generate treatment groups (A, B, C)
        treatment = random.choice(['A', 'B', 'C'])
        
        # Generate biomarker levels (normal distribution approximation)
        biomarker1 = round(random.gauss(50, 15), 2)
        biomarker2 = round(random.gauss(100, 25), 2)
        
        # Generate survival times based on covariates
        # Stronger effects for better demonstration:
        # - Treatment B: Strong protective effect (HR ~0.4)
        # - Treatment A: Moderate protective effect (HR ~0.7)
        # - Treatment C: Reference group (HR = 1.0)
        baseline_hazard = 0.015
        if treatment == 'B':
            treatment_effect = 0.35  # Strong protective effect - much better survival
        elif treatment == 'A':
            treatment_effect = 0.65  # Moderate protective effect - better survival
        else:
            treatment_effect = 1.0   # Control/reference group
        
        # Age effect: Strong positive association (older = worse survival)
        # Each 10 years increases hazard by ~40%
        age_effect = 1 + (age - 50) / 50 * 1.2  # Normalized around age 50
        
        # Biomarker1 effect: Strong negative association (higher biomarker = better survival)
        # Higher biomarker1 values are protective
        biomarker_effect = 1 - (biomarker1 - 50) / 100 * 0.8  # Normalized around 50
        biomarker_effect = max(0.3, biomarker_effect)  # Prevent negative values
        
        # Combine all effects multiplicatively
        hazard_rate = baseline_hazard * treatment_effect * age_effect * biomarker_effect
        
        # Generate survival time (exponential distribution)
        survival_time = random.expovariate(hazard_rate) if hazard_rate > 0 else 1825
        
        # Cap maximum survival time at 1825 days (5 years)
        survival_time = min(survival_time, 1825)
        
        # Generate censoring (target ~30% censoring rate)
        # Generate random censoring time between 1 year and 5 years
        censoring_time = random.uniform(365, 1825)
        
        # Determine if event occurs before censoring
        # Add some randomness to ensure we get both events and censoring
        if random.random() < 0.3:  # 30% chance of censoring
            # Censored case: censoring happens before event
            if survival_time > censoring_time:
                event = 0
                survival_time_observed = censoring_time
            else:
                # Event still occurs, but we'll force censoring for this case
                event = 0
                survival_time_observed = random.uniform(survival_time + 1, 1825)
        else:
            # Event case: event occurs before censoring
            event = 1
            survival_time_observed = survival_time
        
        # Round survival time
        survival_time_observed = round(survival_time_observed, 2)
        
        # Add row to data
        data.append([
            patient_id,
            survival_time_observed,
            event,
            age,
            gender,
            treatment,
            biomarker1,
            biomarker2
        ])
    
    # Write to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    
    print(f"Sample survival data created successfully!")
    print(f"Output file: {output_file}")
    print(f"Shape: {n_samples} rows, 8 columns")
    
    # Count events
    events = sum(row[2] for row in data[1:])
    print(f"Events: {events}/{n_samples} ({100*events/n_samples:.1f}%)")
    
    # Print first few rows
    print("\nFirst 5 rows:")
    for i, row in enumerate(data[:6]):
        if i == 0:
            print(" | ".join(str(x) for x in row))
        else:
            print(" | ".join(str(x) for x in row))

if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(script_dir), 'data')
    output_file = os.path.join(data_dir, 'sample_survival_data.csv')
    generate_sample_data(n_samples=500, output_file=output_file)

