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
    indx_sym_beat = [(k, v) for k, v in indx_sym.items() if v in beat_ann_dict.keys()]
    print(
        f"Removing ann from {record_name}: {len(symbols) - len(indx_sym_beat)} <-- They don't describe peaks."
    )
    # Peaks without the first and last.
    indx_sym_dict = dict(indx_sym_beat[1:-1])

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
beat_ann = (  # ilość
    "N",  # Normal beat.                                                    # 74984
    "L",  # Left bundle branch block beat.                                  # 8069
    "R",  # Right bundle branch block beat.                                 # 7250
    "A",  # Atrial premature beat.                                          # 2544
    "a",  # Aberrated atrial premature beat.                                # 150 odrzucone
    "J",  # Nodal (junctional) premature beat.                              # 83 odrzucone
    "S",  # Supraventricular premature or ectopic beat (atrial or nodal).   # 2 odrzucone
    "V",  # Premature ventricular contraction.                              # 7128
    "F",  # Fusion of ventricular and normal beat.                          # 802 odrzucone
    "e",  # Atrial escape beat.                                             # 16 odrzucone
    "j",  # Nodal (junctional) escape beat.                                 # 229 odrzucone
    "E",  # Ventricular escape beat.                                        # 106 odrzucone
    "/",  # Paced beat.                                                     # 7020
    "f",  # Fusion of paced and normal beat.                                # 982 odrzucone
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
range_len = 260
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
