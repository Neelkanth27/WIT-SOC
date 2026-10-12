import pandas as pd
import numpy as np
import os
import glob
import joblib
import shutil
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = os.path.dirname(__file__)
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_OUTPUT_PATH = os.path.join(BASE_DIR, "saved_model.pkl")
BACKEND_MODEL_PATH = os.path.join(os.path.dirname(BASE_DIR), "backend", "model.pkl")

def clean_and_train():
    # 1. Automatically find the CSV file in the dataset directory
    csv_files = glob.glob(os.path.join(DATASET_DIR, "*.csv"))
    
    if not csv_files:
        print("[!] No CSV files found in ai_model/dataset/. Generating synthetic dataset first...")
        from generate_dataset import generate_telemetry_data
        generate_telemetry_data()
        csv_files = glob.glob(os.path.join(DATASET_DIR, "*.csv"))
    
    target_file = csv_files[0]
    print(f"[*] Loading training dataset: {os.path.basename(target_file)}...")
    
    df = pd.read_csv(target_file)
    df.columns = df.columns.str.strip()

    # Normalize column names to snake_case
    col_map = {
        "Flow Duration": "flow_duration",
        "Flow Bytes/s": "flow_bytes_sec",
        "Total Fwd Packets": "total_fwd_packets",
        "Total Backward Packets": "total_bwd_packets",
        "Fwd Packet Length Mean": "fwd_packet_length_mean",
        "Flow_Duration": "flow_duration",
        "Flow_Bytes_Sec": "flow_bytes_sec",
        "Total_Fwd_Packets": "total_fwd_packets",
        "Total_Bwd_Packets": "total_bwd_packets",
        "Fwd_Packet_Length_Mean": "fwd_packet_length_mean"
    }
    df.rename(columns=col_map, inplace=True)
    df = df.loc[:, ~df.columns.duplicated()]

    print("[*] Scrubbing data (removing NaN and Infinite values)...")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    features = [
        "flow_duration",
        "flow_bytes_sec",
        "total_fwd_packets",
        "total_bwd_packets",
        "fwd_packet_length_mean"
    ]
    
    # 4. Map the labels to our 3 speculative execution tiers:
    # 0: Benign (Safe Traffic)
    # 1: Suspicious (Port scan / sub-threshold anomaly -> TEMP_ISOLATE)
    # 2: Malicious (DDoS / exfiltration -> PERM_LOCK)
    def map_labels(label):
        lbl_str = str(label).upper().strip()
        if lbl_str in ["0", "BENIGN", "SAFE"]:
            return 0
        elif lbl_str in ["1", "SUSPICIOUS", "SUSPICIOUS_SCAN", "PORT", "SCAN", "PORTSCAN"]:
            return 1
        elif lbl_str in ["2", "MALICIOUS", "MALICIOUS_DDOS", "DDOS", "ATTACK"]:
            return 2
        elif "BENIGN" in lbl_str:
            return 0
        elif "PORT" in lbl_str or "SCAN" in lbl_str:
            return 1
        else:
            return 2
            
    df["Label_Mapped"] = df["Label"].apply(map_labels)

    X = df[features]
    y = df["Label_Mapped"]

    print(f"[*] Total valid network flows for training: {len(df)}")
    print(f"[*] Class distribution:\n{y.value_counts()}")
    
    # 5. Split data and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("[*] Training Random Forest Classifier on telemetry data...")
    model = RandomForestClassifier(n_estimators=50, max_depth=15, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    print("[*] Evaluating model performance...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"[+] Model Accuracy: {acc * 100:.2f}%")
    print("-" * 55)
    print("Classification Report:")
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

    # Also sync directly to backend folder for ease of execution
    os.makedirs(os.path.dirname(BACKEND_MODEL_PATH), exist_ok=True)
    shutil.copyfile(MODEL_OUTPUT_PATH, BACKEND_MODEL_PATH)
    print(f"[+] Synced model copy to {BACKEND_MODEL_PATH}")
    print("[+] Training complete. The real-world AI Threat Engine is ready.")

if __name__ == "__main__":
    clean_and_train()