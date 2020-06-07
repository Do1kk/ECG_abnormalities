import wfdb
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


record_names = "mit-bih/RECORDS"
db_folder = "mit-bih/"
csv_folder = "csv_type_files/"
range_len = 260
shift = 25  # przesunięcie środka
L_side = int(range_len / 2) - shift
R_side = int(range_len / 2) + shift

beat_ann = (  # ilość
    # "a",  # Aberrated atrial premature beat.                                # 150
    # "J",  # Nodal (junctional) premature beat.                              # 83
    # "S",  # Supraventricular premature or ectopic beat (atrial or nodal).   # 2
    "F",  # Fusion of ventricular and normal beat.                          # 802
    # "e",  # Atrial escape beat.                                             # 16
    # "j",  # Nodal (junctional) escape beat.                                 # 229
)
beat_ann_file = (
    # "lA",
    # "J",
    # "S",
    "F",
    # "lE",
    # "lJ",
)
beat_ann_dict = dict(zip(beat_ann, beat_ann_file))

# Creating empty csv files for modificated signal.
for symbol, f_name in beat_ann_dict.items():
    file_name = "type_" + f_name
    mod_file_name = "type_mod" + f_name
    with open(csv_folder + mod_file_name + ".csv", "w") as csv_file:
        csv_file.write("")

    with open(csv_folder + file_name + ".csv", "r", newline="") as f:
        data = list(
            csv.reader(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        )
    data_from_csv = np.array(data, dtype=np.float16)

mod_data = []
# modyfikacja danych I
for data in data_from_csv:
    mod_data.append(data * np.random.uniform(0.95, 1.05))
mod_data = np.array(mod_data, dtype=np.float16)

for symbol, f_name in beat_ann_dict.items():
    file_name = "type_mod" + f_name
    with open(csv_folder + file_name + ".csv", "a", newline="") as csv_file:
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

    # mod_data2.append(data * np.random.uniform(0.95, 1.05))

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

    # plt.plot(x_new, y_smooth)
    # plt.show()

    mod_data2.append(y_smooth)

mod_data2 = np.array(mod_data2, dtype=np.float16)

for symbol, f_name in beat_ann_dict.items():
    file_name = "type_mod" + f_name
    with open(csv_folder + file_name + ".csv", "a", newline="") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for data in mod_data2:
            writer.writerow(data)
