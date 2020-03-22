import wfdb
from wfdb import processing
import numpy as np
import csv

# Odczytanie pierwszego kanału (są dwa) i preprocesing.
def preprocessing(nazwa_pliku):
    sig, fields = wfdb.rdsamp(katalog_sygnalow + str(nazwa_pliku), channels=[0])
    xqrs = processing.XQRS(sig=sig[:, 0], fs=fields["fs"])
    xqrs.detect()
    wzniesienia = xqrs.qrs_inds
    signal = np.concatenate(sig.tolist(), axis=0)

    return wzniesienia, signal


# Tworzenie pliku .csv z funkcją zapisu.
def tworzenie_csv(nr_pliku, wzniesienia, signal):
    with open(katalog_csv + str(nr_pliku) + ".csv", "w", newline="") as csvfile:
        wpisywanie = csv.writer(
            csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        Lside = int(zakres_wyc / 2)
        Rside = int(zakres_wyc / 2)
        # Zapisanie wyszukanych wzniesień bez pierwszego i ostatniego
        for i in wzniesienia[1:-1]:
            wpisywanie.writerow(signal[i - Lside : i + Rside])


katalog_nazw = "mit-bih/RECORDS"
katalog_sygnalow = "mit-bih/"
katalog_csv = "pliki_csv/"
zakres_wyc = 270
# Odczytanie wszystkich nazwy rekordów z pliku.
with open(katalog_nazw) as plik:
    for linia in plik:
        nr_pliku = linia.strip()
        wzniesienia, signal = preprocessing(nr_pliku)
        tworzenie_csv(nr_pliku, wzniesienia, signal)
