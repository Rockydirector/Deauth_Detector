from scapy.all import sniff, Dot11, RadioTap
from collections import defaultdict
import time
import csv
import os

class FastDeauthDetector:
    def __init__(self, interface='wlan0', rssi_threshold=-50, time_window=60, log_dir='logs'):
        self.interface = interface
        self.rssi_threshold = rssi_threshold
        self.time_window = time_window
        self.mac_stats = defaultdict(lambda: {'count': 0, 'first_seen': 0, 'last_seen': 0})

        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, 'deauth_log.csv')

        # Write header if the file does not exist
        if not os.path.isfile(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Source MAC', 'Destination MAC', 'RSSI', 'Alert'])

    def start(self):
        print(f"[*] Fast deauth detection started on interface '{self.interface}'")
        try:
            sniff(iface=self.interface, prn=self._handle_packet, store=False, monitor=True)
        except Exception as e:
            print(f"[!] Error during sniffing: {e}")

    def _handle_packet(self, pkt):
        if pkt.haslayer(Dot11):
            dot11 = pkt.getlayer(Dot11)

            # Deauthentication frame (type 0, subtype 12)
            if dot11.type == 0 and dot11.subtype == 12:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                src_mac = dot11.addr2 or 'Unknown'
                dst_mac = dot11.addr1 or 'Unknown'
                rssi = self._extract_rssi(pkt)

                stats = self.mac_stats[src_mac]
                stats['count'] += 1
                now = time.time()
                stats['last_seen'] = now
                if stats['first_seen'] == 0:
                    stats['first_seen'] = now

                # Determine alerts
                alerts = []
                if stats['count'] > 10:
                    alerts.append("Rate Alert")
                if rssi > self.rssi_threshold:
                    alerts.append("Proximity Alert")

                alert_str = '; '.join(alerts)
                print(f"[DEAUTH] {src_mac} -> {dst_mac} | RSSI: {rssi} dBm {'| ' + alert_str if alert_str else ''}")

                # Log to CSV
                with open(self.log_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, src_mac, dst_mac, rssi, alert_str])

    def _extract_rssi(self, pkt):
        try:
            if pkt.haslayer(RadioTap):
                return int(pkt.dBm_AntSignal)
        except:
            pass
        return -100  # Default fallback RSSI if not available

if __name__ == "__main__":
    detector = FastDeauthDetector(interface='wlan0', log_dir='logs')  # Replace 'wlan0' with your monitor interface
    detector.start()
