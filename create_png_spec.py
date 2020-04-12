from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt
import time
import multiprocessing


def save_image(x, step):
    for i, data in enumerate(x):
        # Creating a figure so that the image has dimensions of 512x512.
        plt.figure(figsize=(5.42, 5.42))
        spectrum, freqs, t, im = plt.specgram(data, Fs=360)
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(
            f"{images_folder}{record_name}/{i + step}.png",
            bbox_inches="tight",
            pad_inches=0,
            dpi=100,
        )
        plt.close()


images_folder = "images/"
beat_ann = (
    "N",  # Normal beat.
    "L",  # Left bundle branch block beat.
    "R",  # Right bundle branch block beat.
    "A",  # Atrial premature beat.
    "V",  # Premature ventricular contraction.
    "/",  # Paced beat.
)
beat_ann_file = ("N", "L", "R", "A", "V", "Pe")
beat_ann = dict(zip(beat_ann, beat_ann_file))
record_name = "type_" + beat_ann["N"]  # A, /, V, R, L, N,

all_data = genfromtxt("csv_type_files/" + record_name + ".csv", delimiter=";")
process_number = 3
data_per_proc = int(len(all_data) / process_number)
data = []
data.append(np.array(all_data[:data_per_proc]))
data.append(np.array(all_data[data_per_proc : data_per_proc * 2]))
data.append(np.array(all_data[data_per_proc * 2 :]))

start_time = time.time()
if __name__ == "__main__":
    step = 0
    # Creating processes.
    p1 = multiprocessing.Process(target=save_image, args=(data[0], step,))
    step += data_per_proc
    p2 = multiprocessing.Process(target=save_image, args=(data[1], step,))
    step += data_per_proc
    p3 = multiprocessing.Process(target=save_image, args=(data[2], step,))

    # Starting process px.
    p1.start()
    p2.start()
    p3.start()

    # Wait until process px is finished.
    p1.join()
    p2.join()
    p3.join()

    print("--- %s seconds ---" % (time.time() - start_time))
