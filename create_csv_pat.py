import wfdb
from wfdb import processing
import numpy as np
import csv


# Reading the first channel (there are two) and preprocessing.
def preprocessing(record_name):
    sig, fields = wfdb.rdsamp(db_folder + record_name, channels=[0])
    xqrs = processing.XQRS(sig=sig[:, 0], fs=fields["fs"])
    xqrs.detect(verbose=False)
    signal = np.concatenate(sig.tolist(), axis=0)

    return xqrs.qrs_inds, signal


def creating_csv(record_name, qrs_indx, signal):
    with open(csv_folder + record_name + ".csv", "w", newline="") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        L_side = int(range_len / 2)
        R_side = int(range_len / 2)
        print(f"Saving data to a file {record_name}.csv")
        # Saving searched peaks without the first and last.
        for i in qrs_indx[1:-1]:
            writer.writerow(signal[i - L_side : i + R_side])


record_names = "mit-bih/RECORDS"
db_folder = "mit-bih/"
csv_folder = "csv_files/"
range_len = 260
# Reading all record names from the file.
with open(record_names) as file:
    for line in file:
        record_name = str(line.strip())
        qrs_indx, signal = preprocessing(record_name)
        creating_csv(record_name, qrs_indx, signal)
