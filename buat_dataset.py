import pandas as pd

# Data contoh
data = {
    'signal_power': [
        0.02,
        0.03,
        0.05,
        0.15,
        0.18,
        0.22,
        0.75,
        0.80,
        0.92
    ],

    'label': [
        0,
        0,
        0,
        1,
        1,
        1,
        2,
        2,
        2
    ]
}

# Membuat dataframe
df = pd.DataFrame(data)

# Simpan ke CSV
df.to_csv('dataset_hujan.csv', index=False)

print("Dataset berhasil dibuat")
