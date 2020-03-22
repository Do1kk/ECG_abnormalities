import numpy as np
from wfdb import rdrecord
from scipy.signal import find_peaks
from sklearn import preprocessing
import matplotlib.pyplot as plt
import csv


# Odczytanie wszystkich nazwy wszyskich rekordów z pliku.
with open("mit-bih/RECORDS") as plik:
    for linia in plik:
        plik = linia.strip()
        record = rdrecord("mit-bih/" + str(plik), smooth_frames=True)
        signals0 = preprocessing.scale(np.nan_to_num(record.p_signal[:, 0])).tolist()
        peaks0, _ = find_peaks(signals0, distance=200)

        sr_odleglosc = 300

        # Sprawdzanie ilości przechwyconych wzniesień.
        print(signals0)

        # Wyświetlanie przechwyconych przedziałów.
        # for i in peaks0[1:40]:
        #     Lside = int(sr_odleglosc / 2)
        #     Rside = int(sr_odleglosc / 2)
        #     plt.figure()
        #     plt.plot(signals0[i - Lside : i + Rside])
        #     plt.show(block=True)

        # Tworzenie pliku .csv z funkcją zapisu.
        with open("pliki_csv/" + str(plik) + ".csv", "w", newline="") as csvfile:
            wpisywanie = csv.writer(
                csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            Lside = int(sr_odleglosc / 2)
            Rside = int(sr_odleglosc / 2)
            for i in peaks0[1:-1]:
                wpisywanie.writerow(signals0[i - Lside : i + Rside])
