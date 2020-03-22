import numpy as np
from wfdb import rdrecord
from sklearn import preprocessing
import matplotlib.pyplot as plt
from matplotlib.pyplot import pause

record = rdrecord("mit-bih/100", smooth_frames=True)

signals0 = preprocessing.scale(np.nan_to_num(record.p_signal[:, 0])).tolist()
signals1 = preprocessing.scale(np.nan_to_num(record.p_signal[:, 1])).tolist()

# Opisy osi.
feature0, feature1 = record.sig_name[0], record.sig_name[1]

fig, axs = plt.subplots(2)
for i in range(0, 3000, 10):
    axs[0].plot(signals0[i : i + 800])
    axs[1].plot(signals1[i : i + 800])

    pause(0.1)
    axs[0].cla()
    axs[1].cla()
