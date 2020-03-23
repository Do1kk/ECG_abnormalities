import wfdb
import numpy as np
import csv


# Odczytanie pierwszego kanału (są dwa) i preprocesing.
def preprocessing(nazwa_pliku):
    sig, fields = wfdb.rdsamp(katalog_sygnalow + nazwa_pliku, channels=[0])
    signal = np.concatenate(sig.tolist(), axis=0)

    ann_ref = wfdb.rdann(katalog_sygnalow + nazwa_pliku, "atr")
    wzniesienia = ann_ref.sample
    symbole = ann_ref.symbol  # Symobole adnotacji.

    return wzniesienia, signal


# Tworzenie pliku .csv z funkcją zapisu.
def tworzenie_csv(nazwa_pliku, wzniesienia, signal):
    with open(katalog_csv + nazwa_pliku + ".csv", "w", newline="") as csvfile:
        wpisywanie = csv.writer(
            csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        Lside = int(zakres_wyc / 2)
        Rside = int(zakres_wyc / 2)
        # Zapisanie wyszukanych wzniesień bez 2 pierwszych i 2 ostatnich.
        print(f"Zapisywanie danych do pliku {nazwa_pliku}.csv")
        for i in wzniesienia[2:-2]:
            wpisywanie.writerow(signal[i - Lside : i + Rside])


plik_nazw = "mit-bih/RECORDS"
katalog_sygnalow = "mit-bih/"
katalog_csv = "pliki_csv/"
zakres_wyc = 270
# Odczytanie wszystkich nazwy rekordów z pliku.
with open(plik_nazw) as plik:
    for linia in plik:
        nr_pliku = str(linia.strip())
        wzniesienia, signal = preprocessing(nr_pliku)
        tworzenie_csv(nr_pliku, wzniesienia, signal)

        # print(f"sygnal shape: {signal.shape}")
        # print(f"wzniesienia shape: {wzniesienia.shape}")
