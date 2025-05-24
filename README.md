# Deauth Culprit Detection & Localization Tool

## Features
- Real-time Wi-Fi deauthentication attack detection (monitor mode)
- Logs MAC (even if spoofed), RSSI, timestamp, BSSID
- Rolling log for aggressive offenders
- Proximity estimation via RSSI
- Alerts for repeated or high-risk deauths
- MAC spoofing detection via RSSI/MAC correlation
- (Bonus) Multi-node triangulation with ESP32 nodes
- CSV logs for forensics
- Visualization samples

## Setup

1. **Enable monitor mode:**
sudo airmon-ng start wlan0

2. **Install dependencies:**
pip install -r requirements.txt

3. **Run detector:**
sudo python core/detector.py

4. **(Optional) ESP32 Node:**
- Flash `hardware/esp32_node/firmware/esp32_deauth_sniffer.ino` to ESP32.
- Place nodes at known positions for triangulation.

## Sample Output

![Alert Screenshot](samples/alert_screenshot.png)

## Forensic Logs

See `logs/sample_log.csv`.

## Triangulation

See `hardware/triangulation_diagram.png` and `samples/heatmap_example.png`.

---

**Contact:**  
Your Name  
your.email@example.com