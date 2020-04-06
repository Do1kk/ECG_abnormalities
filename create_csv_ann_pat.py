import wfdb
import numpy as np
import csv


# Reading the first channel (there are two) and preprocessing.
def preprocessing(record_name):
    sig, fields = wfdb.rdsamp(db_folder + record_name, channels=[0])
    signal = np.concatenate(sig.tolist(), axis=0)
    ann_ref = wfdb.rdann(db_folder + record_name, "atr")
    qrs_indx = ann_ref.sample
    symbols = ann_ref.symbol
    # Reject annotations that do not mark heartbeat points.
    for i in range(len(qrs_indx)):
        if not symbols[i] in beat_annotations:
            qrs_indx[i] = 0
    qrs_indx = qrs_indx[qrs_indx != 0]  # Delete all zeros that occur.
    print(
        f"Removing annotations: {len(symbols) - len(qrs_indx)}. <-- They do not describe peaks."
    )

    return qrs_indx, signal


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
beat_annotations = (
    "N" "L" "R" "A" "a" "J" "S" "V" "F" "e" "j" "E" "/" "f"  # "B" "r" "n" "Q" "?"
)  # Q - Unclassifiable beat. ? - Beat not classified during learning.
range_len = 270
# Reading all record names from the file.
with open(record_names) as file:
    for line in file:
        record_name = str(line.strip())
        qrs_indx, signal = preprocessing(record_name)
        creating_csv(record_name, qrs_indx, signal)

        # print(f"signal shape: {signal.shape}")
        # print(f"peaks shape: {qrs_indx.shape}")
