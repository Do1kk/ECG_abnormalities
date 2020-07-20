from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt
import time
import multiprocessing
from csv_ann_type import beat_ann_dict


def save_image(sig1, sig2, step, beat_type, group_name):
    """Save image.

    Arguments:
        x {list of np.array of float} -- portion of the data from the .csv file, continuous patient measurement signal divided into equal intervals
        step {int} -- the beginning of photo numbering allows to divide data into individual processes in an appropriate way
        record_name {str} -- heartbeat type name
        group_name {str} -- name of the group of heartbeat types
    """
    # sprawdzanie jaki to proces
    name = multiprocessing.current_process().name
    print(f"teraz działa proces: {name}, początek numeracji zdj {step}")
    signal = zip(sig1, sig2)
    for i, (data1, data2) in enumerate(signal):
        # Creating a figure so that the image has dimensions of 220x220.
        plt.figure(figsize=(2.51, 2.51))
        # Pierwszy sygnał.
        plt.subplot(1, 2, 1), plt.specgram(data1, Fs=360)
        plt.axis("off")
        plt.tight_layout()
        # Drugi sygnał.
        plt.subplot(1, 2, 2), plt.specgram(data2, Fs=360)
        plt.axis("off")
        plt.tight_layout()
        # Ustawienie odstępu między dwoma obrazami.
        plt.subplots_adjust(wspace=0.00)

        plt.savefig(
            f"images/type_{group_name}/{i + step}{beat_type}.png",
            bbox_inches="tight",
            pad_inches=0,
            dpi=100,
        )
        plt.close()


# Nowy podział na grupy:
# co ciekawe zostały jeszcze typy "!, P, p".....
beat_ann_group = {
    "N": "NLRB",  # <- non-ectopic,                     brak B (bo to uogólnienie L i R)
    "S": "aJASjen",  # <- supraventricular ectopic,     brak n
    "V": "VE",  # <- ventricular ectopic,
    "F": "FmodF",  # <- fusion beats,
    "Q": "/fQ",  # <- Unknown beats.
}
# Dodanie dodatkowo zmodyfikowanego typu F.
beat_ann_dict["modF"] = "modF"

# Setting to enable multiprocessing.
if __name__ == "__main__":
    print("początek przydzielania procesów")
    for key, val in beat_ann_dict.items():
        print()
        print(f"tworzenie zdjęć z pliku: {val}.csv")
        [group_name] = [k for k, v in beat_ann_group.items() if key in v]
        record_name = "csv_type_files/type_" + val

        all_data = genfromtxt(record_name + ".csv", delimiter=";")
        all_data2 = genfromtxt(record_name + "2.csv", delimiter=";")

        # Division of data for individual processes, signal1.
        process_number = 3
        data_per_proc = int(len(all_data) / process_number)
        data = []
        data.append(np.array(all_data[:data_per_proc]))
        data.append(np.array(all_data[data_per_proc : data_per_proc * 2]))
        data.append(np.array(all_data[data_per_proc * 2 :]))

        # Division of data for individual processes, signal2.
        data2 = []
        data2.append(np.array(all_data2[:data_per_proc]))
        data2.append(np.array(all_data2[data_per_proc : data_per_proc * 2]))
        data2.append(np.array(all_data2[data_per_proc * 2 :]))

        start_time = time.time()
        print("włączenie podziału na procesy")  # debagowanie
        step = 0
        # Creating processes.
        p1 = multiprocessing.Process(
            name="p1",
            target=save_image,
            args=(data[0], data2[0], step, val, group_name),
        )
        step += data_per_proc
        p2 = multiprocessing.Process(
            name="p2",
            target=save_image,
            args=(data[1], data2[1], step, val, group_name),
        )
        step += data_per_proc
        p3 = multiprocessing.Process(
            name="p3",
            target=save_image,
            args=(data[2], data2[2], step, val, group_name),
        )
        # Starting process px.
        p1.start()
        p2.start()
        p3.start()
        # Wait until process px is finished.
        p1.join()
        p2.join()
        p3.join()

        print("--- %s seconds ---" % (time.time() - start_time))
