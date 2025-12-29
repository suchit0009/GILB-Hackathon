import pandas as pd
import os
import sys

# --- CONFIGURATION ---
# Auto-detect CSV in data folder if name varies
DATA_DIR = "data"
DEFAULT_FILE = "PS_20174392719_1491204439457_log.csv"

def load_paysim_data():
    """
    Loads the PaySim dataset from the data directory.
    """
    # Find any CSV in data dir if default doesn't exist
    target_file = os.path.join(DATA_DIR, DEFAULT_FILE)
    if not os.path.exists(target_file):
        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        if csv_files:
            target_file = os.path.join(DATA_DIR, csv_files[0])
        else:
            print(f"❌ ERROR: No CSV file found in {DATA_DIR}")
            sys.exit(1)

    print(f"✅ Found Data File: {target_file}")
    print("⏳ Loading CSV (This might take a moment)...")
    
    # Read CSV
    df = pd.read_csv(target_file)
    
    # Cleanse
    if 'isFlaggedFraud' in df.columns:
        df = df.drop(['isFlaggedFraud'], axis=1)
    
    # Filter
    df = df.loc[(df['type'].isin(['TRANSFER', 'CASH_OUT']))]
    
    print(f"✅ Loaded {len(df)} relevant transactions.")
    return df

if __name__ == "__main__":
    df = load_paysim_data()
    print(df.head())
