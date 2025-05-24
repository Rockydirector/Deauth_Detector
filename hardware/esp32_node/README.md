# ESP32 Deauth Sniffer Node

Flash `esp32_deauth_sniffer.ino` to your ESP32.  
Connect via serial to receive logs in the format:  
`DEAUTH,<RSSI>,<MAC>`

Deploy multiple ESP32s at known room positions for triangulation.

# firmware:

Detects deauthentication frames.

Prints JSON-formatted messages to serial when an attack starts or stops.


# script:

Reads JSON output from the ESP8266 over serial.

Logs to CSV.

Prints detected attack events in real-time.
