# Deauth Culprit Detection & Localization Tool

## Features
- Real-time Wi-Fi deauthentication attack detection (monitor mode)
- Logs MAC (even if spoofed), RSSI, timestamp, BSSID
- Rolling log for aggressive offenders
- Proximity estimation via RSSI
- Alerts for repeated or high-risk deauths
- MAC spoofing detection via RSSI/MAC correlation
- CSV logs for forensics
- Visualization samples

## Setup

1. **Enable monitor mode:**
sudo airmon-ng start wlan0

2. **Install dependencies:**
pip install -r requirements.txt

3. **Run detector:**
sudo python core/detector.py

## Forensic Logs

See `logs/sample_log.csv`.

---
