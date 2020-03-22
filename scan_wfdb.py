from wfdb import rdrecord, rdann, plot_wfdb, io
import numpy as np


record = rdrecord("mit-bih/100", smooth_frames=True, sampfrom=0, sampto=1000)
annotation = rdann("mit-bih/100", "atr", sampfrom=0, sampto=1000)
plot_wfdb(
    record=record,
    annotation=annotation,
    plot_sym=True,
    time_units="seconds",
    title="MIT-BIH Record 100",
    figsize=(8, 6),
)

myarray = np.fromfile("mit-bih/100.atr", count=-1, sep="", offset=0)
# fromfile(file, dtype=float, count=-1, sep='', offset=0)
ile = 0
for i in myarray[1:-1]:
    ile += 1
    # Lside = int(sr_odleglosc / 2)
    # Rside = int(sr_odleglosc / 2)
    # plt.figure()
    # plt.plot(signals0[i - Lside : i + Rside])
    # plt.show(block=True)
print(ile)
