import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Fungsi interpretasi untuk mengubah nilai fuzzy menjadi label kategori
def interpretasi_tingkat_kehebatan(nilai):
    if nilai <= 40:
        return 'Kurang Bisa'
    elif nilai <= 70:
        return 'Biasa'
    else:
        return 'Hebat'

# Fungsi interpretasi untuk mengubah nilai fuzzy menjadi label kategori usia
def interpretasi_usia(nilai):
    if nilai <= 30:
        return 'Muda'
    elif nilai <= 35:
        return 'Sedang'
    else:
        return 'Tua'

# Baca data dari file CSV
data = pd.read_excel(r"D:\python script\data 2\data_renang.xlsx")

# Definisikan variabel input
usia = ctrl.Antecedent(np.arange(25, 36, 1), 'usia')
tinggi = ctrl.Antecedent(np.arange(165, 183, 1), 'tinggi')
berat = ctrl.Antecedent(np.arange(65, 83, 1), 'berat')

# Definisikan variabel output
tingkat_kehebatan = ctrl.Consequent(np.arange(0, 101, 1), 'tingkat_kehebatan')

# Definisikan fungsi keanggotaan untuk variabel input dan output
usia.automf(3)
tinggi.automf(3)
berat.automf(3)

tingkat_kehebatan['kurang_bisa'] = fuzz.trimf(tingkat_kehebatan.universe, [0, 0, 40])
tingkat_kehebatan['biasa'] = fuzz.trimf(tingkat_kehebatan.universe, [30, 50, 70])
tingkat_kehebatan['hebat'] = fuzz.trimf(tingkat_kehebatan.universe, [60, 80, 100])

# Aturan fuzzy
rule1 = ctrl.Rule(usia['poor'] | tinggi['poor'] | berat['poor'], tingkat_kehebatan['kurang_bisa'])
rule2 = ctrl.Rule(usia['average'] | tinggi['average'] | berat['average'], tingkat_kehebatan['biasa'])
rule3 = ctrl.Rule(usia['good'] | tinggi['good'] | berat['good'], tingkat_kehebatan['hebat'])

# Buat sistem kontrol fuzzy
tingkat_kehebatan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tingkat_kehebatan_simulasi = ctrl.ControlSystemSimulation(tingkat_kehebatan_ctrl)

# Inisialisasi list untuk menyimpan hasil
hasil_tingkat_kehebatan = []

# Iterasi melalui setiap individu dalam data
for index, row in data.iterrows():
    # Masukkan nilai variabel input dari data yang dibaca
    tingkat_kehebatan_simulasi.input['usia'] = row['usia']
    tingkat_kehebatan_simulasi.input['tinggi'] = row['tinggi']
    tingkat_kehebatan_simulasi.input['berat'] = row['berat']

    # Hitung nilai variabel output
    tingkat_kehebatan_simulasi.compute()

    # Simpan hasil
    hasil_tingkat_kehebatan.append(tingkat_kehebatan_simulasi.output['tingkat_kehebatan'])

# Tambahkan hasil ke data frame
data['tingkat_kehebatan'] = hasil_tingkat_kehebatan

# Interpretasikan nilai fuzzy menjadi kategori
data['kategori_tingkat_kehebatan'] = data['tingkat_kehebatan'].apply(interpretasi_tingkat_kehebatan)
data['kategori_usia'] = data['usia'].apply(interpretasi_usia)

# Simpan ke file Excel
data.to_excel('hasil_fuzzy_karakteristik.xlsx', index=False)