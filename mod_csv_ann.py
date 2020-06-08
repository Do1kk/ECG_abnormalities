import numpy as np
import csv
from scipy.interpolate import interp1d


csv_folder = "csv_type_files/"
range_len = 260
shift = 25  # przesunięcie środka
L_side = int(range_len / 2) - shift
R_side = int(range_len / 2) + shift

beat_ann = "F"  # Fusion of ventricular and normal beat. Ilość: 802
beat_ann_file = "F"

symbol = beat_ann
f_name = beat_ann_file
# Creating empty csv files for modificated signal.
file_name = "type_" + f_name
mod_file_name = "type_mod" + f_name
with open(csv_folder + mod_file_name + ".csv", "w") as csv_file:
    csv_file.write("")

# Odczytanie danych by móc je później przetworzyć.
with open(csv_folder + file_name + ".csv", "r", newline="") as f:
    data = list(csv.reader(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL))
data_from_csv = np.array(data, dtype=np.float16)

mod_data = []
# modyfikacja danych I
for data in data_from_csv:
    mod_data.append(data * np.random.uniform(0.95, 1.05))
mod_data = np.array(mod_data, dtype=np.float16)

with open(csv_folder + mod_file_name + ".csv", "a", newline="") as csv_file:
    writer = csv.writer(
        csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    for data in mod_data:
        writer.writerow(data)

mod_data2 = []
# modyfikacja danych II
# tym razem nie jest to zwykłe mnożenie a ucięcie punktów i interpolacjia
# by zasymulować rozciągnięcie sygnału
for data in data_from_csv:
    y = data
    # 10 proc z 260, a 14 bo
    num = np.random.randint(1, 14)
    # skracanie przedziału, niestety nie przedłużam, było trudniejsze bo wymagało by
    # użycie sygnału z przebiegu, a nie edycji danych z pliku csv
    y = y[num:-num]

    dlugosc = len(y)
    x = np.linspace(0, dlugosc, num=dlugosc)

    x_new = np.linspace(x.min(), x.max(), range_len)

    f = interp1d(x, y, kind="linear")
    y_smooth = f(x_new)

    mod_data2.append(y_smooth)

mod_data2 = np.array(mod_data2, dtype=np.float16)

with open(csv_folder + mod_file_name + ".csv", "a", newline="") as csv_file:
    writer = csv.writer(
        csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    for data in mod_data2:
        writer.writerow(data)


# modyfikacja danych III, czyli połączenie razem dwóch poprzednich
mod_data3 = []
mod_data3_2 = []

for data in data_from_csv:
    mod_data3.append(data * np.random.uniform(0.95, 1.05))
mod_data3 = np.array(mod_data3, dtype=np.float16)


for data in mod_data3:
    y = data
    # 10 proc z 260, a 14 bo
    num = np.random.randint(1, 14)
    # skracanie przedziału, niestety nie przedłużam, było trudniejsze bo wymagało by
    # użycie sygnału z przebiegu, a nie edycji danych z pliku csv
    y = y[num:-num]

    dlugosc = len(y)
    x = np.linspace(0, dlugosc, num=dlugosc)

    x_new = np.linspace(x.min(), x.max(), range_len)

    f = interp1d(x, y, kind="linear")
    y_smooth = f(x_new)

    mod_data3_2.append(y_smooth)
mod_data3 = np.array(mod_data3_2, dtype=np.float16)

with open(csv_folder + mod_file_name + ".csv", "a", newline="") as csv_file:
    writer = csv.writer(
        csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    for data in mod_data3:
        writer.writerow(data)
