import pandas as pd
import xgboost as xgb
import pickle
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score, confusion_matrix

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_pipeline.loader import load_paysim_data

MODEL_OUTPUT_PATH = "fast_lane/sentinel_xgboost.model"

def train_model():
    print("🚀 Starting Sentinel AI Training Pipeline...")
    
    # 1. Load Data
    try:
        df = load_paysim_data()
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return

    # 2. Feature Engineering
    print("🛠  Feature Engineering...")
    
    df.loc[df.type == 'TRANSFER', 'type'] = 0
    df.loc[df.type == 'CASH_OUT', 'type'] = 1
    df['type'] = df['type'].astype(int)
    
    df['errorBalanceOrig'] = df.newbalanceOrig + df.amount - df.oldbalanceOrg
    df['errorBalanceDest'] = df.oldbalanceDest + df.amount - df.newbalanceDest

    feature_cols = ['type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'errorBalanceOrig', 'errorBalanceDest']
    X = df[feature_cols]
    y = df['isFraud']

    # 3. Split
    print("✂️  Splitting Data (80% Train, 20% Test)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train
    print("🔥 Training XGBoost Model (This may take 1-2 mins)...")
    weights = (y == 0).sum() / (1.0 * (y == 1).sum())
    clf = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1,
        scale_pos_weight=weights,
        n_jobs=4,
        random_state=42
    )
    clf.fit(X_train, y_train)
    
    # 5. Evaluate
    print("📊 Evaluating Model...")
    preds = clf.predict_proba(X_test)[:, 1]
    auprc = average_precision_score(y_test, preds)
    print(f"✅ AUPRC Score: {auprc:.4f}")
    
    # 6. Save
    print(f"💾 Saving Model to {MODEL_OUTPUT_PATH}...")
    # Create directory if not exists
    os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
    
    clf.get_booster().save_model(MODEL_OUTPUT_PATH)
    with open(MODEL_OUTPUT_PATH + ".pkl", "wb") as f:
        pickle.dump(clf, f)
        
    print("🎉 BOOM! Model Trained & Saved.")

if __name__ == "__main__":
    train_model()
