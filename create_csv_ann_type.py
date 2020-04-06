import wfdb
import numpy as np
import csv


# Reading the first channel (there are two) and preprocessing.
def preprocessing(record_name, beat_ann_dict):
    sig, fields = wfdb.rdsamp(db_folder + record_name, channels=[0])
    signal = np.concatenate(sig.tolist(), axis=0)
    ann_ref = wfdb.rdann(db_folder + record_name, "atr")
    qrs_indx = ann_ref.sample
    symbols = ann_ref.symbol
    indx_sym = dict(zip(qrs_indx, symbols))
    indx_sym_beat = list(
        filter(lambda x: x[1] in beat_ann_dict.keys(), indx_sym.items())
    )
    print(
        f"Removing ann from {record_name}: {len(symbols) - len(indx_sym_beat)} <-- They don't describe peaks."
    )
    # Peaks without the first and last.
    indx_sym_beat = list(indx_sym_beat)[1:-1]
    indx_sym_dict = dict(indx_sym_beat)

    return indx_sym_dict, signal


def creating_csv(indx_sym_dict, beat_ann_dict, signal):
    for k, v in indx_sym_dict.items():
        file_name = "type_" + beat_ann_dict[v]
        with open(csv_folder + file_name + ".csv", "a", newline="") as csv_file:
            writer = csv.writer(
                csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(signal[k - L_side : k + R_side])


record_names = "mit-bih/RECORDS"
db_folder = "mit-bih/"
csv_folder = "csv_type_files/"
beat_ann = (
    "N",  # Normal beat.
    "L",  # Left bundle branch block beat.
    "R",  # Right bundle branch block beat.
    "A",  # Atrial premature beat.
    "a",  # Aberrated atrial premature beat.
    "J",  # Nodal (junctional) premature beat.
    "S",  # Supraventricular premature or ectopic beat (atrial or nodal).
    "V",  # Premature ventricular contraction.
    "F",  # Fusion of ventricular and normal beat.
    "e",  # Atrial escape beat.
    "j",  # Nodal (junctional) escape beat.
    "E",  # Ventricular escape beat.
    "/",  # Paced beat.
    "f",  # Fusion of paced and normal beat.
)
# "B" "r" "n" "Q" "?"

beat_ann_file = (
    "N",
    "L",
    "R",
    "A",
    "lA",
    "J",
    "S",
    "V",
    "F",
    "lE",
    "lJ",
    "E",
    "Pe",
    "lF",
)
beat_ann_dict = dict(zip(beat_ann, beat_ann_file))
range_len = 270
L_side = int(range_len / 2)
R_side = int(range_len / 2)

# Creating empty csv files.
for symbol, f_name in beat_ann_dict.items():
    file_name = "type_" + f_name
    with open(csv_folder + file_name + ".csv", "w") as csv_file:
        csv_file.write("")

# Reading all record names from the file and create csv files.
with open(record_names) as file:
    for line in file:
        record_name = str(line.strip())
        indx_sym_dict, signal = preprocessing(record_name, beat_ann_dict)
        creating_csv(indx_sym_dict, beat_ann_dict, signal)

        # print(f"signal shape: {signal.shape}")
        # print(f"peaks shape: {qrs_indx.shape}")
