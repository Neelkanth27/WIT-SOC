import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "siem_audit.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite SIEM Audit Database table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            client_ip TEXT NOT NULL,
            flow_duration REAL,
            flow_bytes_sec REAL,
            total_fwd_packets INTEGER,
            total_bwd_packets INTEGER,
            fwd_packet_length_mean REAL,
            threat_score REAL NOT NULL,
            threat_class TEXT NOT NULL,
            action TEXT NOT NULL,
            hardware_signal TEXT NOT NULL,
            detection_engine TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_event(
    client_ip: str,
    payload: Dict[str, Any],
    threat_score: float,
    threat_class: str,
    action: str,
    hardware_signal: str,
    detection_engine: str = "ML_RANDOM_FOREST"
):
    """Logs a single telemetry event and verdict into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO telemetry_logs (
            timestamp, client_ip, flow_duration, flow_bytes_sec,
            total_fwd_packets, total_bwd_packets, fwd_packet_length_mean,
            threat_score, threat_class, action, hardware_signal, detection_engine
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        client_ip,
        float(payload.get("flow_duration", 0.0)),
        float(payload.get("flow_bytes_sec", 0.0)),
        int(payload.get("total_fwd_packets", 0)),
        int(payload.get("total_bwd_packets", 0)),
        float(payload.get("fwd_packet_length_mean", 0.0)),
        float(threat_score),
        threat_class,
        action,
        hardware_signal,
        detection_engine
    ))
    conn.commit()
    conn.close()

def get_recent_logs(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves the most recent telemetry logs."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM telemetry_logs 
        ORDER BY id DESC 
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_audit_stats() -> Dict[str, Any]:
    """Retrieves summary analytics for the SOC Dashboard."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM telemetry_logs")
    total_logs = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM telemetry_logs WHERE hardware_signal = 'GREEN'")
    green_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM telemetry_logs WHERE hardware_signal = 'YELLOW'")
    yellow_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM telemetry_logs WHERE hardware_signal = 'RED'")
    red_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT DISTINCT client_ip FROM telemetry_logs WHERE action = 'PERM_LOCK'")
    isolated_ips = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return {
        "total_packets": total_logs,
        "green_count": green_count,
        "yellow_count": yellow_count,
        "red_count": red_count,
        "isolated_ips": isolated_ips
    }

def clear_audit_logs():
    """Clears the audit logs table on manual reset."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM telemetry_logs")
    conn.commit()
    conn.close()
