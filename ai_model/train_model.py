import pandas as pd
import numpy as np
import os
import glob
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = os.path.dirname(__file__)
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_OUTPUT_PATH = os.path.join(BASE_DIR, "saved_model.pkl")

def clean_and_train():
    # 1. Automatically find the real CSV file in the dataset directory
    csv_files = glob.glob(os.path.join(DATASET_DIR, "*.csv"))
    
    if not csv_files:
        print("[!] No CSV files found in ai_model/dataset/. Please download the CIC-IDS2017 file.")
        return
    
    target_file = csv_files[0]
    print(f"[*] Loading real enterprise dataset: {os.path.basename(target_file)}...")
    print("    (This might take a minute depending on file size...)")
    
    # 2. Read dataset and strip invisible spaces from the official column headers
    df = pd.read_csv(target_file)
    df.columns = df.columns.str.strip()

    print("[*] Scrubbing data (removing NaN and Infinite values)...")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    # 3. Select specific telemetry features optimized for microsecond inference speed
    features = [
        "Flow Duration",
        "Flow Bytes/s",
        "Total Fwd Packets",
        "Total Backward Packets",
        "Fwd Packet Length Mean"
    ]
    
    # 4. Map the complex real-world string labels to our speculative execution tiers
    def map_labels(label):
        label = str(label).upper()
        if "BENIGN" in label:
            return 0  # Safe Traffic
        elif "PORT" in label or "SCAN" in label:
            return 1  # Suspicious (Triggers Speculative Temporary Hardware Lock)
        else:
            return 2  # Malicious / DDoS (Triggers Permanent Lock)
            
    df["Label_Mapped"] = df["Label"].apply(map_labels)

    X = df[features]
    y = df["Label_Mapped"]

    print(f"[*] Total valid network flows after scrubbing: {len(df)}")
    
    # 5. Split data and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("[*] Training Random Forest Classifier on REAL threat data...")
    model = RandomForestClassifier(n_estimators=50, max_depth=15, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    print("[*] Evaluating real-world performance...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"[+] Real-World Model Accuracy: {acc * 100:.2f}%")
    print("-" * 55)
    print("Classification Report:")
    # Explicitly defining labels=[0, 1, 2] prevents crashes when a class is absent
    print(classification_report(
        y_test, 
        y_pred, 
        labels=[0, 1, 2], 
        target_names=["Benign (0)", "Suspicious (1)", "Malicious (2)"],
        zero_division=0
    ))
    print("-" * 55)
    
    print(f"[*] Saving compiled AI model to {MODEL_OUTPUT_PATH}...")
    joblib.dump(model, MODEL_OUTPUT_PATH)
    print("[+] Training complete. The real-world AI Threat Engine is ready.")

if __name__ == "__main__":
    clean_and_train()