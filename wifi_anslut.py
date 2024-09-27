import network
import time

# Använd ditt Wi-Fi-nätverkets namn och lösenord
ssid = 'TN-XE4199'           # SSID för ditt Wi-Fi-nätverk
password = 'MykDyekKits7'   # Lösenordet för ditt Wi-Fi-nätverk

# Initiera Wi-Fi
wifi = network.WLAN(network.STA_IF)  # Konfigurera Pico W som en klient (station)
wifi.active(True)                    # Aktivera Wi-Fi-modulen
wifi.connect(ssid, password)         # Anslut till Wi-Fi

# Vänta tills anslutningen är upprättad
timeout = 10  # Timeout efter 10 sekunder
while not wifi.isconnected() and timeout > 0:
    print("Försöker ansluta till Wi-Fi...")
    time.sleep(1)
    timeout -= 1

if wifi.isconnected():
    # När anslutningen är klar, skriv ut IP-konfigurationen
    print("Ansluten till Wi-Fi!")
    print("IP-adress:", wifi.ifconfig()[0])  # Skriver ut Pico W:s IP-adress
else:
    print("Kunde inte ansluta till Wi-Fi inom tidsgränsen.")
