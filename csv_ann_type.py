import wfdb
import numpy as np
import csv


def preprocessing(record_name, db_folder, beat_ann_dict, channel):
    """Reading the first channel (there are two) and preprocessing.

    Arguments:              
        record_name {str} -- path to the file that stores the name of all records
        db_folder {str} -- path to the folder that stores MIT-BIH database
        beat_ann_dict {dict of str} -- dict of types of heartbeats and their corresponding folder names

    Returns:
        indx_sym_dict {dict of int and str} -- dict of peak heart points and their corresponding types of heartbeat
        signal {float} -- continuous patient measurement signal (digital signal sampled 360 Hz)
    """
    sig, fields = wfdb.rdsamp(db_folder + record_name, channels=[channel])
    signal = np.concatenate(sig.tolist(), axis=0)
    ann_ref = wfdb.rdann(db_folder + record_name, "atr")
    qrs_indx = ann_ref.sample
    symbols = ann_ref.symbol
    indx_sym = dict(zip(qrs_indx, symbols))
    indx_sym_beat = [(k, v) for k, v in indx_sym.items() if v in beat_ann_dict.keys()]
    # print(f"Set of symbols in {record_name} record: {set(symbols)}")
    print(
        f"Removing ann from {record_name}: {len(symbols) - len(indx_sym_beat)} <-- They don't describe peaks."
    )
    # Peaks without the first and last.
    indx_sym_dict = dict(indx_sym_beat[1:-1])

    return indx_sym_dict, signal


def creating_csv(
    indx_sym_dict, beat_ann_dict, signal, csv_folder, L_side, R_side, channel=""
):
    """Creating .csv file.

    Arguments:
        indx_sym_dict {dict of int and str} -- dict of peak heart points and their corresponding types of heartbeat
        beat_ann_dict {dict of str} -- dict of types of heartbeats and their corresponding folder names
        signal {float} -- continuous patient measurement signal
        csv_folder {str} -- path to the folder that stores .csv files
        L_side {int} -- signal length left of the main hill
        R_side {int} -- signal length right of the main hill
    """
    for k, v in indx_sym_dict.items():
        file_name = "type_" + beat_ann_dict[v] + channel
        with open(csv_folder + file_name + ".csv", "a", newline="") as csv_file:
            writer = csv.writer(
                csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(signal[k - L_side : k + R_side])


record_names = "mit-bih/RECORDS"
db_folder = "mit-bih/"
csv_folder = "csv_type_files/"
range_len = 260
shift = 25  # przesunięcie środka
L_side = int(range_len / 2) - shift
R_side = int(range_len / 2) + shift

beat_ann = (  # ilość
    "N",  # Normal beat.                                                    # 74984
    "L",  # Left bundle branch block beat.                                  # 8069
    "R",  # Right bundle branch block beat.                                 # 7250
    "A",  # Atrial premature beat.                                          # 2544
    "a",  # Aberrated atrial premature beat.                                # 150
    "J",  # Nodal (junctional) premature beat.                              # 83
    "S",  # Supraventricular premature or ectopic beat (atrial or nodal).   # 2
    "V",  # Premature ventricular contraction.                              # 7128
    "F",  # Fusion of ventricular and normal beat.                          # 802
    "e",  # Atrial escape beat.                                             # 16
    "j",  # Nodal (junctional) escape beat.                                 # 229
    "E",  # Ventricular escape beat.                                        # 106
    "/",  # Paced beat.                                                     # 7020
    "f",  # Fusion of paced and normal beat.                                # 982
    "Q",  # Unclassifiable beat.
    # "n",
    # "x",  # Opisany jako "p" na stronie bazy danych: "Non-conducted P-wave (blocked APB)" bloced Atrial premature beat, czyli podobny do "A"
    # "!",  # Opisany jako "!" na stronie bazy danych: "Ventricular flutter wave"
)

# Nazwy przypisane, głównie ze względu na niemożność stworzenia katalogów o nazwie "/" czy z
# rozróżnieniem małych i wielkich liter.
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
    "Q",
    # "lN",
    # "lX",
    # "lV",
)
beat_ann_dict = dict(zip(beat_ann, beat_ann_file))

if __name__ == "__main__":
    # Creating empty csv files.
    for symbol, f_name in beat_ann_dict.items():
        file_name = "type_" + f_name
        with open(csv_folder + file_name + ".csv", "w") as csv_file:
            csv_file.write("")

    # Reading all record names from the file and create csv files.
    with open(record_names) as file:
        for line in file:
            record_name = str(line.strip())
            # Signal 1
            indx_sym_dict, signal1 = preprocessing(
                record_name, db_folder, beat_ann_dict, channel=0
            )
            creating_csv(
                indx_sym_dict, beat_ann_dict, signal1, csv_folder, L_side, R_side
            )
            # Signal 2
            indx_sym_dict, signal2 = preprocessing(
                record_name, db_folder, beat_ann_dict, channel=1
            )
            creating_csv(
                indx_sym_dict,
                beat_ann_dict,
                signal2,
                csv_folder,
                L_side,
                R_side,
                channel="2",
            )

            # print(f"signal shape: {signal.shape}")
            # print(f"peaks shape: {qrs_indx.shape}")
