import numpy as np
import csv
import random
from scipy.interpolate import interp1d


# Creating empty csv files for modificated signal.
def empty_csv_file(mod_file_dir):
    with open(mod_file_dir, "w") as csv_file:
        csv_file.write("")


# Usunąć stąd test_data, po zrobieniu zdjęć, zostaną przeniesione przed podzieleniem.
# Odczytanie danych i oddzielenie danych na zbiór testowy by móc je później przetworzyć.
def read_and_split_data(file_dir):
    with open(file_dir, "r", newline="") as f:
        data = list(
            csv.reader(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        )
    random.shuffle(data)
    data_from_csv = np.array(data, dtype=np.float16)[int(test_set_perc * len(data)) :]
    test_data = np.array(data, dtype=np.float16)[: int(test_set_perc * len(data))]

    return data_from_csv, test_data


# Dopisywanie danych do plików już po zmodyfikowaniu.
def append_mod_data(mod_file_dir, mod_data):
    with open(mod_file_dir, "a", newline="") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for data in mod_data:
            writer.writerow(data)


# Modyfikacja danych przy pomocy mnożenia przez wartość bliską jedynki.
# Trzeba przerowbić dwa sygnały, ponieważ wygenerowana wartość powinna być
# taka sama dla obu sygnałów.
# Można to jakoś uogólnić *args czy coś, by rozumiał ile dostaje argumentów
# i tyle ich funkcja zwracała.
def first_metod_data_modification(data_from_csv1, data_from_csv2):
    mod_data1 = []
    mod_data2 = []
    for i in range(len(data_from_csv1)):
        rand_num_2 = np.random.uniform(0.95, 1.05)
        mod_data1.append(data_from_csv1[i] * rand_num_2)
        mod_data2.append(data_from_csv2[i] * rand_num_2)

    return np.array(mod_data1, dtype=np.float16), np.array(mod_data2, dtype=np.float16)


# Modyfikacja danych przy pomocy skracania obustronnego, niestety nie przedłużam
# bo wymagało by to użycia sygnału z przebiegu, a nie edycji danych z pliku csv.
def second_metod_data_modification(mod_data1, mod_data2):
    mod_data1_temp = []
    mod_data2_temp = []
    for i in range(len(mod_data1)):
        y1 = mod_data1[i]
        y2 = mod_data2[i]
        # <=10 % z 260
        num = np.random.randint(1, 27)
        num_L = int(num * L_side / range_len)
        num_R = num - num_L
        y1 = y1[num_L:-num_R]
        y2 = y2[num_L:-num_R]

        dlugosc = len(y1)
        x = np.linspace(0, dlugosc, num=dlugosc)
        x_new = np.linspace(x.min(), x.max(), range_len)

        f1 = interp1d(x, y1, kind="linear")
        f2 = interp1d(x, y2, kind="linear")
        y_smooth1 = f1(x_new)
        y_smooth2 = f2(x_new)
        mod_data1_temp.append(y_smooth1)
        mod_data2_temp.append(y_smooth2)

    return (
        np.array(mod_data1_temp, dtype=np.float16),
        np.array(mod_data2_temp, dtype=np.float16),
    )


csv_folder = "csv_type_files/"
range_len = 260
shift = 25  # przesunięcie środka
L_side = int(range_len / 2) - shift
R_side = int(range_len / 2) + shift
test_set_perc = 0.15

symbol = "F"  # Fusion of ventricular and normal beat. Ilość: 802
f_name = "F"

file1_dir = csv_folder + "type_" + f_name + ".csv"
file2_dir = csv_folder + "type_" + f_name + "2.csv"
mod_file1_dir = csv_folder + "type_mod" + f_name + ".csv"
mod_file2_dir = csv_folder + "type_mod" + f_name + "2.csv"

empty_csv_file(mod_file1_dir)
empty_csv_file(mod_file2_dir)

data_from_csv1, test_data1 = read_and_split_data(file1_dir)
data_from_csv2, test_data2 = read_and_split_data(file2_dir)

mod_data1, mod_data2 = first_metod_data_modification(data_from_csv1, data_from_csv2)
mod_data1, mod_data2 = second_metod_data_modification(mod_data1, mod_data2)

append_mod_data(mod_file1_dir, mod_data1)
append_mod_data(mod_file2_dir, mod_data2)
