import pandas as pd
import numpy as np
import os

# --- CONFIGURATION ---
# Ensure this path matches where your titanic.csv is located
file_path = r"C:\Users\bruhman\Documents\Titanic Project\titanic.csv"
output_path = r"C:\Users\bruhman\Documents\Titanic Project\error_report.csv"

# --- LOAD DATA ---
if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    exit()

df = pd.read_csv(file_path)

# --- VALIDATION RULES ---
errors = []

# Rule 1: Age must be between 0 and 120
invalid_age = df[(df['age'] < 0) | (df['age'] > 120)]
if len(invalid_age) > 0:
    errors.append(f"Invalid Age: {len(invalid_age)} rows")

# Rule 2: Fare must be non-negative
invalid_fare = df[df['fare'] < 0]
if len(invalid_fare) > 0:
    errors.append(f"Negative Fare: {len(invalid_fare)} rows")

# Rule 3: Fare = 0 but passenger is in paying class (1, 2, or 3)
zero_fare_paying = df[(df['fare'] == 0) & (df['pclass'].isin([1,2,3]))]
if len(zero_fare_paying) > 0:
    errors.append(f"Zero Fare for Paying Class: {len(zero_fare_paying)} rows")

# Rule 4: SibSp + Parch can't be negative
invalid_family = df[(df['sibsp'] < 0) | (df['parch'] < 0)]
if len(invalid_family) > 0:
    errors.append(f"Negative Family Count: {len(invalid_family)} rows")

# Rule 5: Name field should not be empty
invalid_name = df[df['name'].str.strip() == '']
if len(invalid_name) > 0:
    errors.append(f"Blank Name: {len(invalid_name)} rows")

# --- REPORTING ---
print("=== DATA QUALITY AUDIT REPORT ===")
print(f"Total rows checked: {len(df)}")
print(f"Rules applied: 5")

if errors:
    print(f"\n⚠️  ERRORS FOUND:")
    for e in errors:
        print(f"  - {e}")
    
    # Export errors to CSV
    if len(zero_fare_paying) > 0:
        zero_fare_paying.to_csv(output_path, index=False)
        print(f"\n✅ Error report saved to: {output_path}")
else:
    print("\n✅ No logical errors found. Data passes validation.")
