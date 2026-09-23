# Trans-radar

Terminal User Interface (TUI) transit telemetry radar for public buses in Semarang, built entirely with Python and the native `curses` library. The application monitors dynamic fleet kinematics, calculates real-time spherical distances (Haversine formula), and computes live Estimated Time of Arrival (ETA) to designated transit hubs and stops across Semarang.

> **DISCLAIMER / NOTICE:**  
> This project currently operates using a deterministic **Kinematic Telemetry Simulation Engine (Mock Stream)**. Because municipal transit authorities (e.g., BLU Trans Semarang) do not currently provide an unauthenticated, publicly accessible REST or GTFS-Realtime API feed, all coordinate deltas, velocity fluctuations, and proximity vectors are mathematically generated locally to model real-world vehicular behavior. The codebase is architected with a decoupled telemetry ingestion interface, allowing direct plug-and-play integration once a live production endpoint or GTFS-RT feed becomes available.

---

## Features

- **Terminal & Hub Selection:** Interactive CLI prompt supporting major transit terminals and commuter hubs in Semarang (Terminal Mangkang, Penggaron, Halte Udinus, Balaikota, Simpang Lima, Stasiun Poncol, Bandara Ahmad Yani, etc.).
- **Geospatial Distance Vectoring:** Real-time distance calculation relative to the target transit hub using the spherical Haversine formula.
- **Dynamic Kinematic Calculations:**
  - Real-time road velocity tracking in km/h with contextual throttling (deceleration upon approaching stops, acceleration on open roads).
  - Dynamic distance formatting (automatic conversion from kilometers to meters when distance is under 1 km).
  - Physical ETA estimation ($t = \frac{s}{v}$) updated on every cycle.
- **Adaptive Terminal UI:** Built with standard Python `curses`, featuring dynamic terminal boundary detection (`getmaxyx`) and text clipping to prevent terminal resizing exceptions.
- **Zero External Dependencies:** Runs out-of-the-box on standard Python 3 installations without requiring third-party packages or virtual environment setups.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Alif-fiansyah/udinus-netpulse.git](https://github.com/Alif-fiansyah/udinus-netpulse.git)
   cd udinus-netpulse
   ```

2. **Run the script (Requires Python 3.8+):**
   ```bash
   python3 radar.py
   ```

3. **Controls:**
   - Select the target transit hub/stop by entering its corresponding numeric index.
   - Press `q` inside the radar dashboard to gracefully exit back to your shell prompt.


---

## Sample Output

### 1. Terminal Selection Menu
```text
==========================================================
      PANTAU BUS TRANS SEMARANG (KOSAN & TERMINAL)        
==========================================================
[ 1] Halte Kampus Udinus (Imam Bonjol)       
[ 2] Halte Transfer Balaikota Pemuda         
[ 3] Halte Simpang Lima                      
[ 4] Halte Tugu Muda                         
[ 5] Halte Stasiun Poncol                    
[ 6] Halte Stasiun Tawang                    
[ 7] Halte Bandara Ahmad Yani                
[ 8] Terminal Mangkang (Tipe A)              
[ 9] Terminal Penggaron (Tipe A)             
[10] Terminal Sukun Banyumanik               
[11] Terminal Gunungpati                     
[12] Sub-Terminal Citarum                    
[13] Halte Undip Tembalang                   
[14] Halte Unnes Sekaran                     
----------------------------------------------------------
Mau pantau bus dari halte nomor berapa? [1-14]: 1
```

### 2. Live Curses TUI Radar Dashboard
```text
================================================================================
  LIVE RADAR TRANS SEMARANG -> TARGET: [HALTE KAMPUS UDINUS (IMAM BONJOL)]
  KOORDINAT PEMBERHENTIAN: -6.9826, 110.4091
================================================================================

ID BUS    KORIDOR     KECEPATAN    SISA JARAK   ESTIMASI (ETA)   PROKSIMITAS / STATUS
--------------------------------------------------------------------------------
TS-018    Koridor 3A   9.5 km/jam  120 meter    SUDAH SAMPAI     [BURU NAIK!]
TS-044    Koridor 4   18.2 km/jam  480 meter    ~1m 34s          [##########--] MENDEKAT
TS-012    Koridor 1   34.0 km/jam  1.42 km      ~2m 30s          [########----] MELAJU
TS-007    Koridor 2   22.5 km/jam  2.15 km      ~5m 44s          [######------] LAMBAT
TS-029    Koridor 1   38.5 km/jam  3.60 km      ~5m 36s          [####--------] NGEBUT
TS-061    Koridor 6   31.0 km/jam  4.85 km      ~9m 23s          [##----------] MELAJU

================================================================================
  Telemetri bus update tiap detik. Tekan 'q' untuk keluar.
```
