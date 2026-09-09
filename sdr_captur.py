from rtlsdr import RtlSdr
import numpy as np
import time

# Inisialisasi SDR
sdr = RtlSdr()

# Setting SDR
sdr.sample_rate = 1e6
sdr.center_freq = 433e6
sdr.gain = 33.8

# LOOP REALTIME
while True:

    # Membaca sample SDR
    samples = sdr.read_samples(8192)

    # Menghitung power sinyal
    power = np.mean(np.abs(samples)**2)

    # Status hujan sederhana
    if power > 0.02:
        status = "Hujan"
    else:
        status = "Tidak Hujan"

    # Gabungkan data
    data = f"{power},{status}"

    # Tampilkan ke terminal
    print(data)

    # Simpan ke file untuk Node-RED
    with open("/home/eken/data_dashboard.txt", "w") as f:
        f.write(data)

    # Delay 1 detik
    time.sleep(1)

sdr.close()
