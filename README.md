# NeuroVibe_8699
End-to-End Predictive Maintenance System (Node-Gateway-Cloud) for NeuroVibe AI Technologies
### 🌐 Multi-Interface Gateway (i.MX6UL)
Our gateway is designed for 100% uptime with redundant connectivity:
* **Wired:** Dual Ethernet (WAN for Cloud, LAN for Local Diagnostics).
* **Wireless Uplink:** 4G LTE/GSM (EC20 Module) with automatic failover.
* **Local Mesh:** Sub-GHz Radio (AN1310) for long-range Node communication.
* **Short Range:** Wi-Fi (SR8233) for local monitoring and AP mode.

### 📂 Repository Structure
- `/firmware_node`: MCU logic & sensor sampling (EFM32).
- `/gateway_services`: Multi-path network manager & Radio-to-Cloud bridge.
- `/cloud_backend`: Analytics engine (RPM, Velocity, Vibration g) & Auth.
- `/cloud_frontend`: Client dashboard with real-time graphics.
