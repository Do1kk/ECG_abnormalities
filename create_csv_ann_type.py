import wfdb
import numpy as np
import csv


# Reading the first channel (there are two) and preprocessing.
def preprocessing(record_name, beat_ann):
    sig, fields = wfdb.rdsamp(db_folder + record_name, channels=[0])
    signal = np.concatenate(sig.tolist(), axis=0)
    ann_ref = wfdb.rdann(db_folder + record_name, "atr")
    qrs_indx = ann_ref.sample
    symbols = ann_ref.symbol
    indx_sym = dict(zip(qrs_indx, symbols))
    indx_sym_beat = dict(filter(lambda x: x[1] in beat_ann, indx_sym.items()))
    print(
        f"Removing annotations: {len(symbols) - len(indx_sym_beat)} <-- They do not describe peaks."
    )

    return list(indx_sym_beat.keys())[1:-1], signal


def creating_csv(record_name, qrs_indx, signal):
    with open(csv_folder + record_name + ".csv", "w", newline="") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        L_side = int(range_len / 2)
        R_side = int(range_len / 2)
        print(f"Saving data to a file {record_name}.csv")
        # Saving searched peaks without the first and last.
        for i in qrs_indx:
            writer.writerow(signal[i - L_side : i + R_side])


record_names = "mit-bih/RECORDS"
db_folder = "mit-bih/"
csv_folder = "csv_type_files/"
beat_ann = (
    "N",
    "L",
    "R",
    "B",
    "A",
    "a",
    "J",
    "S",
    "V",
    "r",
    "F",
    "e",
    "j",
    "n",
    "E",
    "/",
    "f",  # "Q" "?"
)  # Q - Unclassifiable beat. ? - Beat not classified during learning.
beat_ann_file = (
    "N",
    "L",
    "R",
    "B",
    "A",
    "lA",
    "J",
    "S",
    "V",
    "lR",
    "F",
    "lE",
    "lJ",
    "lN",
    "E",
    "Pe",
    "lF",
)
beat_ann_dict = dict(zip(beat_ann, beat_ann_file))
range_len = 270

# print(beat_ann_dict)

# Creating empty csv files.
for symbol, f_name in beat_ann_dict.items():
    file_name = "type_" + f_name
    with open(csv_folder + file_name + ".csv", "w") as csv_file:
        csv_file.write("Stores arrhythmia type: " + symbol)

# Reading all record names from the file.
with open(record_names) as file:
    for line in file:
        record_name = str(line.strip())
        qrs_indx, signal = preprocessing(record_name, beat_ann)
        creating_csv(record_name, qrs_indx, signal)

        # print(f"signal shape: {signal.shape}")
        # print(f"peaks shape: {qrs_indx.shape}")
