#!/usr/bin/env python3
import curses
import json
import math
import time
import urllib.request

# 1. Daftar terminal & simpul transit di Semarang
TERMINAL_SEMARANG = {
    "udinus": {"nama": "Halte Kampus Udinus (Gedung H)", "lat": -6.9826, "lon": 110.4091},
    "balaikota": {"nama": "Halte Transfer Balaikota Pemuda", "lat": -6.9805, "lon": 110.4132},
    "simpang_lima": {"nama": "Halte Simpang Lima", "lat": -6.9904, "lon": 110.4229},
    "tugu_muda": {"nama": "Halte Tugu Muda", "lat": -6.9841, "lon": 110.4095},
    "stasiun_poncol": {"nama": "Halte Stasiun Poncol", "lat": -6.9727, "lon": 110.4147},
    "stasiun_tawang": {"nama": "Halte Stasiun Tawang", "lat": -6.9644, "lon": 110.4281},
    "bandara_ayani": {"nama": "Halte Bandara Ahmad Yani", "lat": -6.9725, "lon": 110.3756},
    "mangkang": {"nama": "Terminal Mangkang (Tipe A)", "lat": -6.9698, "lon": 110.3129},
    "penggaron": {"nama": "Terminal Penggaron (Tipe A)", "lat": -7.0264, "lon": 110.4851},
    "banyumanik": {"nama": "Terminal Sukun Banyumanik", "lat": -7.0652, "lon": 110.4194},
    "gunungpati": {"nama": "Terminal Gunungpati", "lat": -7.0862, "lon": 110.3675},
    "citarum": {"nama": "Sub-Terminal Citarum", "lat": -6.9745, "lon": 110.4412},
    "undip_tembalang": {"nama": "Halte Undip Tembalang", "lat": -7.0505, "lon": 110.4404},
    "unnes_sekaran": {"nama": "Halte Unnes Sekaran", "lat": -7.0494, "lon": 110.3921},
}

URL_TELEMETRI_LIVE = "https://api.wheretheiss.at/v1/satellites/25544"

def hitung_haversine(lat1, lon1, lat2, lon2):
    """Menghitung jarak permukaan bumi dalam kilometer."""
    radius_bumi = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_bumi * c

def ambil_data_live():
    """Mengambil koordinat telemetri live via HTTP request."""
    headers = {"User-Agent": "ArchLinux-Radar/1.0"}
    req = urllib.request.Request(URL_TELEMETRI_LIVE, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=2.5) as respon:
            if respon.status == 200:
                data = json.loads(respon.read().decode("utf-8"))
                return {
                    "lat": float(data["latitude"]),
                    "lon": float(data["longitude"]),
                    "speed": float(data["velocity"]),
                    "alt": float(data["altitude"]),
                    "vis": data.get("visibility", "unknown"),
                }
    except Exception:
        pass
    return None

def buat_bar_radar(jarak_km, max_jarak=20000.0, panjang=15):
    """Bar ASCII visual jarak objek ke terminal pilihan."""
    rasio = max(0.0, min(1.0, 1.0 - (jarak_km / max_jarak)))
    isi = int(rasio * panjang)
    return "#" * isi + "-" * (panjang - isi)

def cetak_aman(stdscr, y, x, teks):
    """Mencegah crash curses jika layar terminal sempit."""
    tinggi_max, lebar_max = stdscr.getmaxyx()
    if y < tinggi_max and x < lebar_max:
        teks_terpotong = teks[:lebar_max - x - 1]
        try:
            stdscr.addstr(y, x, teks_terpotong)
        except curses.error:
            pass

def menu_pilih_terminal():
    """Menu CLI interaktif sebelum masuk ke radar."""
    print("==========================================================")
    print("        PILIH TERMINAL / SIMPUL PANTAUAN SEMARANG         ")
    print("==========================================================")
    daftar_kunci = list(TERMINAL_SEMARANG.keys())
    for idx, kunci in enumerate(daftar_kunci, start=1):
        item = TERMINAL_SEMARANG[kunci]
        print(f"[{idx:2d}] {item['nama']:<40}")
    print("----------------------------------------------------------")
    while True:
        try:
            pilih = int(input(f"Pilih nomor terminal acuan [1-{len(daftar_kunci)}]: "))
            if 1 <= pilih <= len(daftar_kunci):
                kunci_pilih = daftar_kunci[pilih - 1]
                return TERMINAL_SEMARANG[kunci_pilih]
            print("Pilihan di luar rentang, masukkan angka yang ada.")
        except ValueError:
            print("Input harus berupa angka bulat.")

def dashboard_radar(stdscr, titik_pantau):
    """TUI loop pelacak jarak jauh real-time."""
    curses.curs_set(0)
    stdscr.nodelay(True)

    while True:
        tombol = stdscr.getch()
        if tombol in (ord('q'), ord('Q')):
            break

        tinggi_layar, lebar_layar = stdscr.getmaxyx()
        stdscr.erase()

        if tinggi_layar < 16 or lebar_layar < 55:
            cetak_aman(stdscr, 1, 2, "Ukuran terminal terlalu kecil.")
            cetak_aman(stdscr, 2, 2, "Perbesar/maximize terminal Anda.")
            stdscr.refresh()
            time.sleep(0.5)
            continue

        telemetri = ambil_data_live()
        garis = "=" * (lebar_layar - 4)

        cetak_aman(stdscr, 1, 2, garis)
        cetak_aman(stdscr, 2, 2, "  LIVE REMOTE TELEMETRY RADAR (REAL-TIME TRACKER)")
        cetak_aman(stdscr, 3, 2, f"  STASIUN ACUAN : [{titik_pantau['nama'].upper()}] ({titik_pantau['lat']}, {titik_pantau['lon']})")
        cetak_aman(stdscr, 4, 2, garis)

        if telemetri:
            jarak_permukaan = hitung_haversine(telemetri["lat"], telemetri["lon"], titik_pantau["lat"], titik_pantau["lon"])
            jarak_ruang = math.sqrt(jarak_permukaan**2 + telemetri["alt"]**2)
            bar_radar = f"[{buat_bar_radar(jarak_permukaan)}]"

            cetak_aman(stdscr, 6, 4,  "STATUS KONEKSI      : TERHUBUNG KE TELEMETRI LIVE (HTTP 200)")
            cetak_aman(stdscr, 7, 4,  f"KOORDINAT OBJEK     : {telemetri['lat']:>8.4f}° LAT, {telemetri['lon']:>8.4f}° LON")
            cetak_aman(stdscr, 8, 4,  f"KECEPATAN LAJU      : {telemetri['speed']:>10.2f} km/jam")
            cetak_aman(stdscr, 9, 4,  f"KETINGGIAN ORBIT    : {telemetri['alt']:>10.2f} km di atas laut")
            cetak_aman(stdscr, 10, 4, f"VISIBILITAS CAHAYA  : {telemetri['vis'].upper()}")
            cetak_aman(stdscr, 11, 4, "-" * (lebar_layar - 8))
            cetak_aman(stdscr, 12, 4, f"JARAK DARI TARGET   : {jarak_permukaan:>10.2f} km (Jarak Darat)")
            cetak_aman(stdscr, 13, 4, f"JARAK LINE-OF-SIGHT : {jarak_ruang:>10.2f} km (Jarak Fisik Langit)")
            cetak_aman(stdscr, 14, 4, f"INDIKATOR PROKSIMITAS: {bar_radar}")

            if jarak_permukaan < 1500.0:
                cetak_aman(stdscr, 16, 4, "STATUS: OBJEK SEDANG MELINTAS DI ATAS WILAYAH INI!")
            else:
                cetak_aman(stdscr, 16, 4, "STATUS: Objek sedang berada di belahan bumi lain.")
        else:
            cetak_aman(stdscr, 6, 4, "STATUS KONEKSI: Mengambil data telemetri live...")

        cetak_aman(stdscr, tinggi_layar - 3, 2, garis)
        cetak_aman(stdscr, tinggi_layar - 2, 4, "Data ditarik per detik via REST API. Tekan 'q' untuk keluar.")
        stdscr.refresh()
        time.sleep(1.0)

def main():
    terminal_pilihan = menu_pilih_terminal()
    try:
        curses.wrapper(dashboard_radar, terminal_pilihan)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()