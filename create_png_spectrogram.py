import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt


record_name = "type_S"
y = genfromtxt("csv_type_files/" + record_name + ".csv", delimiter=";")
x = np.array(y[0])

# Utworzenie figury by ostatecznie obraz miał 1024x1024.
plt.figure(figsize=(10.54, 10.54))
spectrum, freqs, t, im = plt.specgram(x, Fs=360)
plt.axis("off")
plt.tight_layout()
plt.savefig("pict.png", bbox_inches="tight", pad_inches=0, dpi=100)
