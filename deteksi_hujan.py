from rtlsdr import RtlSdr
import numpy as np
import pandas as pd
import joblib
import time
import csv
import os
from datetime import datetime

# ==========================
# LOAD MODEL MACHINE LEARNING
# ==========================
model = joblib.load("model_hujan.pkl")

# ==========================
# KONFIGURASI RTL-SDR
# ==========================
sdr = RtlSdr()
sdr.sample_rate = 1e6
sdr.center_freq = 433e6
sdr.gain = 33.8

# ==========================
# FILE DATASET CSV
# ==========================
csv_file = "/home/eken/dataset_hujan.csv"

# Buat file dan header jika belum ada
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "signal_power", "kondisi"])

print("Sistem Deteksi Hujan Aktif")

# ==========================
# LOOP DETEKSI
# ==========================
while True:
    try:

        # Baca sampel SDR
        samples = sdr.read_samples(8192)

        # Hitung signal power
        power = np.mean(np.abs(samples)**2)

        # Data untuk Machine Learning
        data_baru = pd.DataFrame(
            [[power]],
            columns=['signal_power']
        )

        # Prediksi
        hasil = model.predict(data_baru)[0]

        # Klasifikasi
        if hasil == 0:
            kondisi = "Tidak Hujan"
        elif hasil == 1:
            kondisi = "Gerimis"
        else:
            kondisi = "Hujan Deras"

        # Tampilkan di terminal
        print(f"{power:.5f} --> {kondisi}")

        # Simpan ke CSV
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, power, kondisi])

        # Kirim ke Node-RED Dashboard
        with open('/home/eken/data_dashboard.txt', 'w') as f:
            f.write(f"{power},{kondisi}")

        time.sleep(1)

    except Exception as e:
        print("Error:", e)
        time.sleep(1)

# Tutup SDR
sdr.close()
