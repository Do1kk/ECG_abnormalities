import pywt
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

# print(pywt.wavelist(kind="continuous"))


def save_image2(sig1, sig2, waveletname="cmor"):

    time = np.arange(0, len(sig1))
    scales = np.arange(1, 128)

    dt = 1
    [coefficients, frequencies] = pywt.cwt(sig1, scales, waveletname, dt)
    [coefficients2, frequencies2] = pywt.cwt(sig2, scales, waveletname, dt)
    power = (abs(coefficients)) ** 2
    period = 1.0 / frequencies
    power2 = (abs(coefficients2)) ** 2
    period2 = 1.0 / frequencies2
    levels = [0.015625 * pow(2, i) for i in range(12)]
    contourlevels = np.log2(levels)

    fig, ax = plt.subplots(ncols=2, figsize=(2.5, 2.5))  # (2.51, 2.51)
    im = ax[0].contourf(
        time, np.log2(period), np.log2(power), contourlevels, extend="both"
    )
    im2 = ax[1].contourf(
        time, np.log2(period2), np.log2(power2), contourlevels, extend="both"
    )
    ax[0].invert_yaxis()  # odwrócenie osi y
    ax[1].invert_yaxis()  # odwrócenie osi y

    ax[0].axis("off")
    ax[1].axis("off")
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.00)
    plt.savefig(
        # f"images/type_{group_name}/{i + step}{beat_type}.png",
        f"images/aaaa.png",
        bbox_inches="tight",
        pad_inches=0,
        dpi=100,
        format="png",
    )


all_data1 = genfromtxt("csv_type_files/type_F.csv", delimiter=";")
all_data2 = genfromtxt("csv_type_files/type_F2.csv", delimiter=";")
sig1 = all_data1[5]
sig2 = all_data2[5]

save_image2(sig1, sig2)
