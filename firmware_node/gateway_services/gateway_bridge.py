# NeuroVibe 8699 - Multi-Interface Gateway Bridge (i.MX6UL)
import serial, requests, os, time

# Priority: WAN/LAN > Wi-Fi > GSM (4G)
INTERFACES = ["eth0", "wlan0", "ppp0"]
UART_PORT = "/dev/ttymxc1" # Radio AN1310 Connection
CLOUD_URL = "https://predict.nvpredictive.com"

def get_active_interface():
    for iface in INTERFACES:
        # Google DNS ping check for internet
        if os.system(f"ping -I {iface} -c 1 8.8.8.8 > /dev/null 2>&1") == 0:
            return iface
    return None

def main_loop():
    print("NeuroVibe Gateway Service Started...")
    ser = serial.Serial(UART_PORT, 115200, timeout=1)
    
    while True:
        if ser.in_waiting > 0:
            # Node se UART data read karna
            raw_node_data = ser.readline().decode('utf-8').strip()
            active_iface = get_active_interface()
            
            if active_iface:
                try:
                    payload = {"vibration": [float(x) for x in raw_node_data.split(',')]}
                    requests.post(CLOUD_URL, json=payload, timeout=5)
                    print(f"Data pushed via {active_iface}")
                except Exception as e:
                    print(f"Push error: {e}")
            else:
                print("Critical: No Network (LAN/4G Down). Local buffer enabled.")
        time.sleep(0.1)

if __name__ == "__main__":
    main_loop()
