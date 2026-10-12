import pandas as pd
import numpy as np
import os

# Ensure the output directory exists
DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(DATASET_DIR, "synthetic_network_telemetry.csv")

def generate_telemetry_data(num_samples=10000):
    """
    Generates synthetic network telemetry data mimicking CIC-IDS2017 features.
    Classes:
      0: BENIGN (Normal background traffic)
      1: SUSPICIOUS (Port scanning, reconnaissance, sub-threshold anomaly)
      2: MALICIOUS (Volumetric DDoS, ransomware exfiltration, high-rate flood)
    """
    np.random.seed(42)
    
    # 1. Benign Traffic (~70% of dataset)
    n_benign = int(num_samples * 0.70)
    benign_flow_duration = np.random.uniform(20.0, 500.0, size=n_benign)
    benign_flow_bytes = np.random.uniform(10.0, 500.0, size=n_benign)
    benign_fwd_packets = np.random.randint(2, 25, size=n_benign)
    benign_bwd_packets = np.random.randint(2, 25, size=n_benign)
    benign_packet_len_mean = np.random.uniform(40.0, 1200.0, size=n_benign)
    benign_labels = ["BENIGN"] * n_benign

    # 2. Suspicious Traffic (~15% of dataset - Port scanning / stealth reconnaissance)
    n_suspicious = int(num_samples * 0.15)
    susp_flow_duration = np.random.uniform(5.0, 40.0, size=n_suspicious)
    susp_flow_bytes = np.random.uniform(20.0, 120.0, size=n_suspicious)
    susp_fwd_packets = np.random.randint(1, 4, size=n_suspicious)
    susp_bwd_packets = np.random.randint(0, 2, size=n_suspicious)
    susp_packet_len_mean = np.random.uniform(30.0, 80.0, size=n_suspicious)
    susp_labels = ["SUSPICIOUS_SCAN"] * n_suspicious

    # 3. Malicious Traffic (~15% of dataset - Volumetric DDoS & Exfiltration)
    n_malicious = num_samples - n_benign - n_suspicious
    mal_flow_duration = np.random.uniform(1.0, 15.0, size=n_malicious)
    mal_flow_bytes = np.random.uniform(1000000.0, 10000000.0, size=n_malicious)
    mal_fwd_packets = np.random.randint(1000, 5000, size=n_malicious)
    mal_bwd_packets = np.random.randint(0, 5, size=n_malicious)
    mal_packet_len_mean = np.random.uniform(3000.0, 9000.0, size=n_malicious)
    mal_labels = ["MALICIOUS_DDOS"] * n_malicious

    # Combine into a pandas DataFrame using standardized feature names
    df = pd.DataFrame({
        "flow_duration": np.concatenate([benign_flow_duration, susp_flow_duration, mal_flow_duration]),
        "flow_bytes_sec": np.concatenate([benign_flow_bytes, susp_flow_bytes, mal_flow_bytes]),
        "total_fwd_packets": np.concatenate([benign_fwd_packets, susp_fwd_packets, mal_fwd_packets]),
        "total_bwd_packets": np.concatenate([benign_bwd_packets, susp_bwd_packets, mal_bwd_packets]),
        "fwd_packet_length_mean": np.concatenate([benign_packet_len_mean, susp_packet_len_mean, mal_packet_len_mean]),
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