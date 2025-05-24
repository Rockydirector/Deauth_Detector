#include <ESP8266WiFi.h>

extern "C" {
#include "user_interface.h"
}

// ===== SETTINGS ===== //
#define LED 2              /* LED pin (2=built-in LED) */
#define LED_INVERT true    /* Invert HIGH/LOW for LED */
#define SERIAL_BAUD 115200 /* Baudrate for serial communication */
#define CH_TIME 140        /* Scan time (in ms) per channel */
#define PKT_RATE 5         /* Min. packets before it gets recognized as an attack */
#define PKT_TIME 1         /* Min. interval (CH_TIME*CH_RANGE) before it gets recognized as an attack */

const short channels[] = { 1,2,3,4,5,6,7,8,9,10,11,12,13 };

// ===== Runtime variables ===== //
int ch_index { 0 };
int packet_rate { 0 };
int attack_counter { 0 };
unsigned long update_time { 0 };
unsigned long ch_time { 0 };

// ===== Sniffer function ===== //
void sniffer(uint8_t *buf, uint16_t len) {
  if (!buf || len < 28) return;

  byte pkt_type = buf[12];
  if (pkt_type == 0xA0 || pkt_type == 0xC0) {
    ++packet_rate;
  }
}

void attack_started() {
  digitalWrite(LED, !LED_INVERT);
  Serial.println("{\"event\":\"attack_started\",\"timestamp\":" + String(millis()) + "}");
}

void attack_stopped() {
  digitalWrite(LED, LED_INVERT);
  Serial.println("{\"event\":\"attack_stopped\",\"timestamp\":" + String(millis()) + "}");
}

void setup() {
  Serial.begin(SERIAL_BAUD);

  pinMode(LED, OUTPUT);
  digitalWrite(LED, LED_INVERT);

  WiFi.disconnect();
  wifi_set_opmode(STATION_MODE);
  wifi_set_promiscuous_rx_cb(sniffer);
  wifi_set_channel(channels[0]);
  wifi_promiscuous_enable(true);

  Serial.println("{\"event\":\"started\"}");
}

void loop() {
  unsigned long current_time = millis();

  if (current_time - update_time >= (sizeof(channels)*CH_TIME)) {
    update_time = current_time;

    if (packet_rate >= PKT_RATE) {
      ++attack_counter;
    } else {
      if (attack_counter >= PKT_TIME) attack_stopped();
      attack_counter = 0;
    }

    if (attack_counter == PKT_TIME) {
      attack_started();
    }

    packet_rate = 0;
  }

  if (sizeof(channels) > 1 && current_time - ch_time >= CH_TIME) {
    ch_time = current_time;
    ch_index = (ch_index+1) % (sizeof(channels)/sizeof(channels[0]));
    short ch = channels[ch_index];
    wifi_set_channel(ch);
  }
}
