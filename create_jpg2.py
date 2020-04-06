from numpy import genfromtxt
import numpy as np
from scipy import signal
import matplotlib as mpl
import matplotlib.pyplot as plt
import requests

mpl.rcParams["figure.figsize"] = [12, 8]


# r = requests.get("https://forums.ni.com/ni/attachments/ni/170/322886/1/ecg.txt")
# data = r.text
# data = np.array([float(el) for el in data.splitlines()])

record_name = "type_S"
y = genfromtxt("csv_type_files/" + record_name + ".csv", delimiter=";")
data = np.array(y[1])


# Plot spectrogram
fig, ax = plt.subplots()
f, t, Sxx = signal.spectrogram(data)
pc = ax.pcolormesh(
    t, f, Sxx, norm=mpl.colors.LogNorm(vmin=Sxx.min(), vmax=Sxx.max()), cmap="inferno"
)
ax.set_ylabel("Frequency")
ax.set_xlabel("Time")
fig.colorbar(pc)
plt.show()
