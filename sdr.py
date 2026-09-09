from rtlsdr import RtlSdr
import numpy as np
import time

sdr = RtlSdr()

sdr.sample_rate = 1e6
sdr.center_freq = 433e6
sdr.gain = 33.8

# LOOP REALTIME
while True:

    # baca sample SDR
    samples = sdr.read_samples(8192)

    # hitung power sinyal
    power = np.mean(np.abs(samples)**2)

    # status sederhana
    if power > 0.02:
        status = "Hujan"
    else:
        status = "Tidak Hujan"

    # gabungkan data
    data = f"{power},{status}"

    # tampilkan di terminal
    print(data)

    # simpan ke file Node-RED
    with open("/home/eken/data_dashboard.txt", "w") as f:
        f.write(data)

    # delay
    time.sleep(1)

sdr.close()
