import pandas as pd
import numpy as np
import os

# Ensure the output directory exists
DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(DATASET_DIR, "synthetic_network_telemetry.csv")

def generate_telemetry_data(num_samples=5000):
    """
    Generates synthetic network telemetry data mimicking CIC-IDS2017.
    Classes:
      0: BENIGN (Normal traffic)
      1: SUSPICIOUS (Anomalous activity triggering speculative rules)
      2: MALICIOUS (High-severity attack like ransomware/DDoS)
    """
    np.random.seed(42)
    
    # 1. Benign Traffic (~70% of dataset)
    n_benign = int(num_samples * 0.70)
    benign_flow_duration = np.random.normal(loc=50000, scale=10000, size=n_benign)
    benign_flow_bytes = np.random.normal(loc=1200, scale=300, size=n_benign)
    benign_fwd_packets = np.random.randint(1, 15, size=n_benign)
    benign_bwd_packets = np.random.randint(1, 15, size=n_benign)
    benign_packet_len_mean = np.random.normal(loc=200, scale=40, size=n_benign)
    benign_labels = [0] * n_benign

    # 2. Suspicious Traffic (~15% of dataset - Sub-threshold anomaly)
    n_suspicious = int(num_samples * 0.15)
    susp_flow_duration = np.random.normal(loc=150000, scale=20000, size=n_suspicious)
    susp_flow_bytes = np.random.normal(loc=8500, scale=1500, size=n_suspicious)
    susp_fwd_packets = np.random.randint(20, 60, size=n_suspicious)
    susp_bwd_packets = np.random.randint(5, 20, size=n_suspicious)
    susp_packet_len_mean = np.random.normal(loc=650, scale=100, size=n_suspicious)
    susp_labels = [1] * n_suspicious

    # 3. Malicious Traffic (~15% of dataset - Ransomware / Exfiltration)
    n_malicious = num_samples - n_benign - n_suspicious
    mal_flow_duration = np.random.normal(loc=350000, scale=50000, size=n_malicious)
    mal_flow_bytes = np.random.normal(loc=45000, scale=5000, size=n_malicious)
    mal_fwd_packets = np.random.randint(100, 300, size=n_malicious)
    mal_bwd_packets = np.random.randint(1, 10, size=n_malicious)
    mal_packet_len_mean = np.random.normal(loc=1200, scale=200, size=n_malicious)
    mal_labels = [2] * n_malicious

    # Combine into a pandas DataFrame
    df = pd.DataFrame({
        "Flow_Duration": np.concatenate([benign_flow_duration, susp_flow_duration, mal_flow_duration]),
        "Flow_Bytes_Sec": np.concatenate([benign_flow_bytes, susp_flow_bytes, mal_flow_bytes]),
        "Total_Fwd_Packets": np.concatenate([benign_fwd_packets, susp_fwd_packets, mal_fwd_packets]),
        "Total_Bwd_Packets": np.concatenate([benign_bwd_packets, susp_bwd_packets, mal_bwd_packets]),
        "Fwd_Packet_Length_Mean": np.concatenate([benign_packet_len_mean, susp_packet_len_mean, mal_packet_len_mean]),
        "Label": np.concatenate([benign_labels, susp_labels, mal_labels])
    })

    # Shuffle dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"[+] Dataset generated successfully with {len(df)} records.")
    print(f"[+] Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_telemetry_data()