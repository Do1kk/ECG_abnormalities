import numpy as np
from wfdb import rdrecord
from scipy.signal import find_peaks
from sklearn import preprocessing
import matplotlib.pyplot as plt

record = rdrecord("mit-bih/100", smooth_frames=True, sampto=1100)

signals0 = preprocessing.scale(np.nan_to_num(record.p_signal[:, 0])).tolist()
signals1 = preprocessing.scale(np.nan_to_num(record.p_signal[:, 1])).tolist()
peaks0, _ = find_peaks(signals0, distance=150)
peaks1, _ = find_peaks(signals1, distance=150)
# Opisy osi.
feature0, feature1 = record.sig_name[0], record.sig_name[1]

#  Średnia odstępu szczytów.
suma = 0
for i in range(len(peaks0) - 1):
    suma += peaks0[i + 1] - peaks0[i]
sr_odleglosc = suma / (len(peaks0) - 1)

for i in peaks0:
    Lside = int(sr_odleglosc / 2)
    Rside = int(sr_odleglosc / 2)
    if i == peaks0[0]:
        Lside = i
    plt.figure()
    plt.plot(signals0[i - Lside : i + Rside])
    plt.ylabel(feature0)
    plt.show(block=True)
