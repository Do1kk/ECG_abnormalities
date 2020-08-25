import numpy as np
import csv
import random
from scipy.interpolate import interp1d
from image_split import test_ratio
from csv_ann_type import csv_folder, range_len, L_side


# Creating empty csv files.
def empty_csv_file(mod_file_dir):
    with open(mod_file_dir, "w") as csv_file:
        csv_file.write("")


def read_csv_file(file_dir):
    with open(file_dir, "r", newline="") as f:
        data = list(
            csv.reader(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        )
    return data


# Append or Overwrite data to CSV files.
def modification_csv_file(file_dir, data, mode="a"):
    with open(file_dir, mode, newline="") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for d in data:
            writer.writerow(d)


# Reading data and separating some of them into a test set to be able to
# process them later.
def read_and_split_data(file_dir1, file_dir2, test_ratio):
    data1 = read_csv_file(file_dir1)
    data2 = read_csv_file(file_dir2)

    temp_data = list(zip(data1, data2))
    random.shuffle(temp_data)
    data1, data2 = zip(*temp_data)

    modification_csv_file(file_dir1, data1, mode="w")  # Overwrite csv file.
    modification_csv_file(file_dir2, data2, mode="w")  # Overwrite csv file.
    data_from_csv1 = np.array(data1, dtype=np.float16)[int(test_ratio * len(data1)) :]
    data_from_csv2 = np.array(data2, dtype=np.float16)[int(test_ratio * len(data2)) :]

    return data_from_csv1, data_from_csv2


# Data modification by multiplying by a value close to one,
# generated value should be the same for both signals.
def first_method_data_modification(data_from_csv1, data_from_csv2):
    mod_data1 = []
    mod_data2 = []
    for i in range(len(data_from_csv1)):
        rand_num_2 = np.random.uniform(0.95, 1.05)
        mod_data1.append(data_from_csv1[i] * rand_num_2)
        mod_data2.append(data_from_csv2[i] * rand_num_2)

    return np.array(mod_data1, dtype=np.float16), np.array(mod_data2, dtype=np.float16)


# Modification data with double-sided shortening, unfortunately I do not
# extend it because this would require use of a signal from the waveform.
def second_method_data_modification(mod_data1, mod_data2):
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

        x = np.linspace(0, len(y1), num=len(y1))
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


data_mult = 5
symbol = "F"  # Fusion of ventricular and normal beat. Quantity: 802.
f_name = "F"

file1_dir = csv_folder + "type_" + f_name + ".csv"
file2_dir = csv_folder + "type_" + f_name + "2.csv"
mod_file1_dir = csv_folder + "type_mod" + f_name + ".csv"
mod_file2_dir = csv_folder + "type_mod" + f_name + "2.csv"

empty_csv_file(mod_file1_dir)
empty_csv_file(mod_file2_dir)

data_from_csv1, data_from_csv2 = read_and_split_data(file1_dir, file2_dir, test_ratio)

# Duplicate data.
# (data_mult - 1) <- number of modified copies for whole type_F set.
for i in range(data_mult - 1):
    mod_data1, mod_data2 = first_method_data_modification(
        data_from_csv1, data_from_csv2
    )
    mod_data1, mod_data2 = second_method_data_modification(mod_data1, mod_data2)

    modification_csv_file(mod_file1_dir, mod_data1, mode="a")  # Append mod data.
    modification_csv_file(mod_file2_dir, mod_data2, mode="a")  # Append mod data.
