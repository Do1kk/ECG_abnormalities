from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np


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
x = np.array(y)

# Creating a figure so that the image has dimensions of 1024x1024.
plt.figure(figsize=(10.54, 10.54))
spectrum, freqs, t, im = plt.specgram(x, Fs=360)
plt.axis("off")
plt.tight_layout()
plt.savefig("pict.png", bbox_inches="tight", pad_inches=0, dpi=100)
