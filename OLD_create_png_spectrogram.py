from numpy import genfromtxt
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


record_name = "type_A"
y = genfromtxt("csv_type_files/" + record_name + ".csv", delimiter=";")
sig = np.array(y[1])

freqs, times, Sxx = signal.spectrogram(sig, scaling="density")
plt.figure(figsize=(7, 7), dpi=100)
plt.imshow(Sxx, aspect="auto", cmap="hot_r", origin="lower")

plt.axis("off")
plt.tight_layout()
# plt.savefig("pict.png", bbox_inches="tight", pad_inches=0)
plt.show()
