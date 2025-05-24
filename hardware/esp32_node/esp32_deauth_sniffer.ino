#include <WiFi.h>
#include <esp_wifi.h>

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_promiscuous_rx_cb(&promisc_cb);
}

void promisc_cb(void* buf, wifi_promiscuous_pkt_type_t type) {
  wifi_promiscuous_pkt_t *pkt = (wifi_promiscuous_pkt_t*)buf;
  if (type == WIFI_PKT_MGMT && pkt->payload[0] == 0xC0) { // Deauth frame
    int rssi = pkt->rx_ctrl.rssi;
    Serial.printf("DEAUTH,%d,%02x:%02x:%02x:%02x:%02x:%02x\n", rssi,
      pkt->payload[10], pkt->payload[11], pkt->payload[12],
      pkt->payload[13], pkt->payload[14], pkt->payload[15]);
  }
}

void loop() {}
