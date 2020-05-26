from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt
import time
import multiprocessing


def save_image(x, step, record_name, group_name):
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

    for i, data in enumerate(x):
        # Creating a figure so that the image has dimensions of 220x220.
        plt.figure(figsize=(2.5, 2.5))
        spectrum, freqs, t, im = plt.specgram(data, Fs=360)
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(
            f"images/{record_name[:5]}{group_name}/{i + step}{record_name[5:]}.png",
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
    "F": "F",  # <- fusion beats,
    "Q": "/fQ",  # <- Unknown beats.
}

beat_ann_dict = {
    "N": "N",
    "L": "L",
    "R": "R",
    "A": "A",
    "a": "lA",
    "J": "J",
    "S": "S",
    "V": "V",
    "F": "F",
    "e": "lE",
    "j": "lJ",
    "E": "E",
    "/": "Pe",
    "f": "lF",
    "Q": "Q",
}

# Setting to enable multiprocessing.
if __name__ == "__main__":
    print("początek instrukcji po if __name__")
    for key, val in beat_ann_dict.items():
        print()
        print(f"tworzenie zdjęć z pliku: {val}.csv")
        [group_name] = [k for k, v in beat_ann_group.items() if key in v]
        record_name = (
            "type_" + val
        )  # A, L, V, /, R, N ustawić pętlę by robił wszystkie na raz

        all_data = genfromtxt("csv_type_files/" + record_name + ".csv", delimiter=";")

        # Division of data for individual processes.
        process_number = 3
        data_per_proc = int(len(all_data) / process_number)
        data = []
        data.append(np.array(all_data[:data_per_proc]))
        data.append(np.array(all_data[data_per_proc : data_per_proc * 2]))
        data.append(np.array(all_data[data_per_proc * 2 :]))

        start_time = time.time()
        print("włączenie podziału na procesy")  # debagowanie
        step = 0
        # Creating processes.
        p1 = multiprocessing.Process(
            name="p1", target=save_image, args=(data[0], step, record_name, group_name)
        )
        step += data_per_proc
        p2 = multiprocessing.Process(
            name="p2", target=save_image, args=(data[1], step, record_name, group_name)
        )
        step += data_per_proc
        p3 = multiprocessing.Process(
            name="p3", target=save_image, args=(data[2], step, record_name, group_name)
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
