from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
import time
import multiprocessing


start_time = time.time()
images_folder = "images/"
record_name = "type_A"
beat_ann = (
    "N",  # Normal beat.
    "L",  # Left bundle branch block beat.
    "R",  # Right bundle branch block beat.
    "A",  # Atrial premature beat.
    "V",  # Premature ventricular contraction.
    "/",  # Paced beat.
)
beat_ann_file = (
    "N",
    "L",
    "R",
    "A",
    "V",
    "Pe",
)
beat_ann_dict = dict(zip(beat_ann, beat_ann_file))
y = genfromtxt("csv_type_files/" + record_name + ".csv", delimiter=";")
podzielnik = int(len(y) / 3)
x = np.array(y[:podzielnik])
xx = np.array(y[podzielnik : podzielnik * 2])
xxx = np.array(y[podzielnik * 2 :])


def save_image(x, step):
    for i, data in enumerate(x):
        # Creating a figure so that the image has dimensions of 1024x1024.
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


if __name__ == "__main__":
    step = 0
    # creating processes
    p1 = multiprocessing.Process(target=save_image, args=(x, step,))
    step += podzielnik
    p2 = multiprocessing.Process(target=save_image, args=(xx, step,))
    step += podzielnik
    p3 = multiprocessing.Process(target=save_image, args=(xxx, step,))

    # starting process 1
    p1.start()
    # starting process 2
    p2.start()
    # starting process 3
    p3.start()

    # wait until process 1 is finished
    p1.join()
    # wait until process 2 is finished
    p2.join()
    # wait until process 3 is finished
    p3.join()

    print("--- %s seconds ---" % (time.time() - start_time))
