import wfdb
from wfdb import processing
import numpy as np
import csv


# Odczytanie wszystkich nazwy wszyskich rekordów z pliku.
with open("mit-bih/RECORDS") as plik:
    for linia in plik:
        plik = linia.strip()
        sig, fields = wfdb.rdsamp("mit-bih/" + str(plik), channels=[0])
        xqrs = processing.XQRS(sig=sig[:, 0], fs=fields["fs"])
        xqrs.detect()

        wzniesienia = xqrs.qrs_inds
        signal2 = sig.tolist()
        signal = np.concatenate(signal2, axis=0)

        print(signal)
        sr_odleglosc = 270
        # Tworzenie pliku .csv z funkcją zapisu.
        with open("pliki_csv/" + str(plik) + ".csv", "w", newline="") as csvfile:
            wpisywanie = csv.writer(
                csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            Lside = int(sr_odleglosc / 2)
            Rside = int(sr_odleglosc / 2)
            for i in wzniesienia[1:-1]:
                wpisywanie.writerow(signal[i - Lside : i + Rside])
