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
# Creating empty csv files for modificated signal1 and signal2.
file_dir = csv_folder + "type_" + f_name + ".csv"
file2_dir = csv_folder + "type_" + f_name + "2.csv"
mod_file_dir = csv_folder + "type_mod" + f_name + ".csv"
mod_file2_dir = csv_folder + "type_mod" + f_name + "2.csv"
with open(mod_file_dir, "w") as csv_file:
    csv_file.write("")
with open(mod_file2_dir, "w") as csv_file:
    csv_file.write("")

# Odczytanie danych by móc je później przetworzyć dla signal1 i signal2.
with open(file_dir, "r", newline="") as f:
    data = list(csv.reader(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL))
data_from_csv = np.array(data, dtype=np.float16)
with open(file2_dir, "r", newline="") as f:
    data = list(csv.reader(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL))
data_from_csv2 = np.array(data, dtype=np.float16)

mod_data = []
mod_data2 = []
# modyfikacja danych I dla signal1 i signal2
for i in range(len(data_from_csv)):
    rand_num = np.random.uniform(0.95, 1.05)
    mod_data.append(data_from_csv[i] * rand_num)
    mod_data2.append(data_from_csv2[i] * rand_num)
mod_data = np.array(mod_data, dtype=np.float16)
mod_data2 = np.array(mod_data2, dtype=np.float16)

with open(mod_file_dir, "a", newline="") as csv_file:
    writer = csv.writer(
        csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    for data in mod_data:
        writer.writerow(data)
with open(mod_file2_dir, "a", newline="") as csv_file:
    writer = csv.writer(
        csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    for data in mod_data2:
        writer.writerow(data)


mod_data_2 = []
mod_data2_2 = []
# modyfikacja danych II signal1 i signal2
# tym razem nie jest to zwykłe mnożenie, a ucięcie punktów i interpolacjia
for i in range(len(data_from_csv)):
    y = data_from_csv[i]
    y2 = data_from_csv2[i]
    # 10 proc z 260, a 14 bo
    num = np.random.randint(1, 14)
    # skracanie przedziału, niestety nie przedłużam, było trudniejsze bo wymagało by
    # użycie sygnału z przebiegu, a nie edycji danych z pliku csv
    y = y[num:-num]
    y2 = y2[num:-num]

    dlugosc = len(y)
    x = np.linspace(0, dlugosc, num=dlugosc)
    x_new = np.linspace(x.min(), x.max(), range_len)

    f = interp1d(x, y, kind="linear")
    f2 = interp1d(x, y2, kind="linear")

    y_smooth = f(x_new)
    y_smooth2 = f2(x_new)

    mod_data_2.append(y_smooth)
    mod_data2_2.append(y_smooth2)
mod_data_2 = np.array(mod_data_2, dtype=np.float16)
mod_data2_2 = np.array(mod_data2_2, dtype=np.float16)

with open(mod_file_dir, "a", newline="") as csv_file:
    writer = csv.writer(
        csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    for data in mod_data_2:
        writer.writerow(data)
with open(mod_file2_dir, "a", newline="") as csv_file:
    writer = csv.writer(
        csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    for data in mod_data2_2:
        writer.writerow(data)


# modyfikacja danych III, połączenie razem dwóch poprzednich zmian
# dla signal1 i signal2
mod_data_3 = []
mod_data_3_temp = []
mod_data2_3 = []
mod_data2_3_temp = []
for i in range(len(data_from_csv)):
    rand_num_2 = np.random.uniform(0.95, 1.05)
    mod_data_3.append(data_from_csv[i] * rand_num_2)
    mod_data2_3.append(data_from_csv2[i] * rand_num_2)
mod_data_3 = np.array(mod_data_3, dtype=np.float16)
mod_data2_3 = np.array(mod_data2_3, dtype=np.float16)

for i in range(len(mod_data_3)):
    y = mod_data_3[i]
    y2 = mod_data2_3[i]
    # 10 proc z 260, a 14 bo
    num = np.random.randint(1, 14)
    # skracanie przedziału, niestety nie przedłużam, było trudniejsze bo wymagało by
    # użycie sygnału z przebiegu, a nie edycji danych z pliku csv
    y = y[num:-num]
    y2 = y2[num:-num]

    dlugosc = len(y)
    x = np.linspace(0, dlugosc, num=dlugosc)
    x_new = np.linspace(x.min(), x.max(), range_len)

    f = interp1d(x, y, kind="linear")
    f2 = interp1d(x, y2, kind="linear")

    y_smooth = f(x_new)
    y_smooth2 = f2(x_new)

    mod_data_3_temp.append(y_smooth)
    mod_data2_3_temp.append(y_smooth2)
mod_data_3 = np.array(mod_data_3_temp, dtype=np.float16)
mod_data2_3 = np.array(mod_data2_3_temp, dtype=np.float16)


with open(mod_file_dir, "a", newline="") as csv_file:
    writer = csv.writer(
        csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    for data in mod_data_3:
        writer.writerow(data)
with open(mod_file2_dir, "a", newline="") as csv_file:
    writer = csv.writer(
        csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    for data in mod_data2_3:
        writer.writerow(data)
