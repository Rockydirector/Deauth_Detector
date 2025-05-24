import serial
import json
import time
import csv
import os

SERIAL_PORT = '/dev/ttyUSB0'  # Change to your ESP8266 serial port (e.g., COM3 on Windows)
BAUD_RATE = 115200
LOG_FILE = 'logs/esp8266_log.csv'

os.makedirs('logs', exist_ok=True)

if not os.path.isfile(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Event', 'ESP_Timestamp'])

def main():
    print("[*] Listening to ESP8266 serial data...")
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                line = ser.readline().decode(errors='ignore').strip()
                if line.startswith("{") and "event" in line:
                    try:
                        data = json.loads(line)
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        print(f"[ESP8266] {data['event']} @ {timestamp}")
                        with open(LOG_FILE, 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow([timestamp, data.get("event"), data.get("timestamp")])
                    except json.JSONDecodeError:
                        print("[!] Invalid JSON from ESP:", line)
    except Exception as e:
        print(f"[!] Serial Error: {e}")

if __name__ == "__main__":
    main()
