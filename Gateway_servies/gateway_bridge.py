import serial, requests, os, time, json

# --- CONFIGURATION ---
UART_PORT = "/dev/ttymxc1" # Radio AN1310/BC832 Connection
BAUD_RATE = 115200
# Aapka Vercel/Cloudflare URL
CLOUD_URL = "https://nvpredictive.com" 
GATEWAY_ID = "NV-GW-8699-001" # Unique Gateway IMEI/ID

# --- INTERFACE PRIORITY (Eth > WiFi > 4G) ---
INTERFACES = ["eth0", "wlan0", "ppp0"]

def get_active_interface():
    for iface in INTERFACES:
        if os.system(f"ping -I {iface} -c 1 8.8.8.8 > /dev/null 2>&1") == 0:
            return iface
    return None

def check_for_ota(model_no, current_ver):
    """Cloud se naya firmware check karna"""
    try:
        res = requests.get(f"https://nvpredictive.com{model_no}&ver={current_ver}")
        if res.status_code == 200:
            new_firmware = res.json().get('url')
            print(f"Updating Node {model_no} via OTA...")
            # OTA Flash Logic Here (UART Push to Node)
    except: pass

def main_loop():
    print(f"NeuroVibe Gateway {GATEWAY_ID} Started...")
    ser = serial.Serial(UART_PORT, BAUD_RATE, timeout=1)
    
    while True:
        if ser.in_waiting > 0:
            try:
                # Node se data read karna (Format: RadioMAC,Vib,Temp,Flux,RPM,Ultra)
                raw_line = ser.readline().decode('utf-8').strip()
                data_points = raw_line.split(',')
                
                if len(data_points) >= 6:
                    node_mac = data_points[0]
                    payload = {
                        "gateway_id": GATEWAY_ID,
                        "node_mac": node_mac,
                        "metrics": {
                            "velocity": float(data_points[1]),
                            "temp": float(data_points[2]),
                            "flux": float(data_points[3]),
                            "rpm": int(data_points[4]),
                            "ultrasound": float(data_points[5])
                        }
                    }
                    
                    iface = get_active_interface()
                    if iface:
                        requests.post(CLOUD_URL, json=payload, timeout=5)
                        print(f"Data from {node_mac} pushed via {iface}")
                    else:
                        print("Offline: Buffering data locally...")
                        
            except Exception as e:
                print(f"Stream Error: {e}")
        
        time.sleep(0.01) # High frequency pick-to-pick gap

if __name__ == "__main__":
    main_loop()
