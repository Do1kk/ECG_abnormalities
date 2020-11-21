import time
import os
import multiprocessing

import pywt
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from scipy.interpolate import interp1d
from csv_ann_type import beat_ann_dict


def save_image(sig1, sig2, step, beat_type, group_name):
    """Save image. Walking Fourier Transform.

    Arguments:
        sig1 {list of np.array of float} -- portion of the data from the .csv file,
        continuous patient measurement signal0 divided into equal intervals
        sig2 {list of np.array of float} -- portion of the data from the .csv file,
        continuous patient measurement signal1 divided into equal intervals
        step {int} -- the beginning of photo numbering allows to divide data
        into individual processes in an appropriate way
        beat_type {str} -- heartbeat type name
        group_name {str} -- name of the group of heartbeat types
    """
    name = multiprocessing.current_process().name
    print(f"Process running: {name}, beginning of pic numbering {step}.")
    # Checking if folder exists, if not it will be created.
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, "images")
    group_results_dir = os.path.join(results_dir, "group_" + group_name)
    if not os.path.isdir(group_results_dir):
        os.makedirs(group_results_dir)

    NFFT = 64
    noverlap = 32
    point_multiply = 8  # 2080 - number of points in one slice.
    # Height - 64 levels (NFFT = 64),
    # width - 128 levels ((260 * 8 - noverlap) / (NFFT - noverlap) x 2 signals).
    signal = zip(sig1, sig2)
    for i, (data1, data2) in enumerate(signal):
        # Creating a linear representation and sampling a second time to get
        # more points for making better spectrograms.
        dl_org = len(data1)
        dl_new = dl_org * point_multiply
        x = np.linspace(0, dl_org, num=dl_org)
        x_new = np.linspace(0, dl_org, num=dl_new)
        f1 = interp1d(x, data1, kind="linear")
        f2 = interp1d(x, data2, kind="linear")
        data1 = f1(x_new)
        data2 = f2(x_new)
        # Creating a figure so that the image has dimensions of 220x220.
        plt.figure(figsize=(2.51, 2.51))
        # First signal.
        plt.subplot(1, 2, 1), plt.specgram(data1, Fs=360, NFFT=NFFT, noverlap=noverlap)
        plt.axis("off")
        plt.tight_layout()
        # Second signal.
        plt.subplot(1, 2, 2), plt.specgram(data2, Fs=360, NFFT=NFFT, noverlap=noverlap)
        plt.axis("off")
        plt.tight_layout()
        # Set the interval between two images.
        plt.subplots_adjust(wspace=0.00)
        plt.savefig(
            f"{group_results_dir}/{i + step}{beat_type}.png",
            bbox_inches="tight",
            pad_inches=0,
            dpi=100,
        )
        plt.close()


def save_image2(sig1, sig2, step, beat_type, group_name, waveletname="cmor"):
    """Save image. Continuous wavelet transform.

    Arguments:
        sig1 {list of np.array of float} -- portion of the data from the .csv file,
        continuous patient measurement signal0 divided into equal intervals
        sig2 {list of np.array of float} -- portion of the data from the .csv file,
        continuous patient measurement signal1 divided into equal intervals
        step {int} -- the beginning of photo numbering allows to divide data
        into individual processes in an appropriate way
        beat_type {str} -- heartbeat type name
        group_name {str} -- name of the group of heartbeat types
        waveletname {str} -- nazwa jądra transformaty falkowej
    """
    name = multiprocessing.current_process().name
    print(f"Process running: {name}, beginning of pic numbering {step}.")
    # Checking if folder exists, if not it will be created.
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, "images")
    group_results_dir = os.path.join(results_dir, "group_" + group_name)
    if not os.path.isdir(group_results_dir):
        os.makedirs(group_results_dir)

    scales = np.arange(1, 128)
    dt = 1
    time = np.arange(0, len(sig1[0]))  # Length of one data slice.
    levels = [0.015625 * pow(2, i) for i in range(12)]
    contourlevels = np.log2(levels)
    signal = zip(sig1, sig2)
    for i, (data1, data2) in enumerate(signal):
        [coefficients, frequencies] = pywt.cwt(data1, scales, waveletname, dt)
        [coefficients2, frequencies2] = pywt.cwt(data2, scales, waveletname, dt)
        power = (abs(coefficients)) ** 2
        period = 1.0 / frequencies
        power2 = (abs(coefficients2)) ** 2
        period2 = 1.0 / frequencies2

        fig, ax = plt.subplots(ncols=2, figsize=(2.5, 2.5))
        im1 = ax[0].contourf(
            time, np.log2(period), np.log2(power), contourlevels, extend="both"
        )
        im2 = ax[1].contourf(
            time, np.log2(period2), np.log2(power2), contourlevels, extend="both"
        )
        ax[0].invert_yaxis()
        ax[1].invert_yaxis()
        ax[0].axis("off")
        ax[1].axis("off")
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.00)
        plt.savefig(
            f"{group_results_dir}/{i + step}{beat_type}.png",
            bbox_inches="tight",
            pad_inches=0,
            dpi=100,
        )
        plt.close()


# New grouping of data.
beat_ann_group = {
    "N": "NLRB",  # Non-ectopic.
    "S": "aJASjen",  # Supraventricular ectopic.
    "V": "VE",  # Ventricular ectopic.
    "F": "FmodF",  # Fusion beats.
    "Q": "/fQ",  # Unknown beats.
}
# Add modified type F.
beat_ann_dict["modF"] = "modF"

# Setting to enable multiprocessing.
if __name__ == "__main__":
    print("Start of process allocation.")
    for key, val in beat_ann_dict.items():
        print()
        print(f"Creating pic from a file: type_{val}.csv.")
        [group_name] = [k for k, v in beat_ann_group.items() if key in v]
        record_name = "csv_type_files/type_" + val

        all_data = genfromtxt(record_name + ".csv", delimiter=";")
        all_data2 = genfromtxt(record_name + "2.csv", delimiter=";")

        # Division of data for individual processes, signal1.
        process_number = 3
        data_per_proc = int(len(all_data) / process_number)
        data = []
        data.append(np.array(all_data[:data_per_proc]))
        data.append(np.array(all_data[data_per_proc : data_per_proc * 2]))
        data.append(np.array(all_data[data_per_proc * 2 :]))

        # Division of data for individual processes, signal2.
        data2 = []
        data2.append(np.array(all_data2[:data_per_proc]))
        data2.append(np.array(all_data2[data_per_proc : data_per_proc * 2]))
        data2.append(np.array(all_data2[data_per_proc * 2 :]))

        start_time = time.time()
        print("Allocating processes.")
        step = 0
        # Creating processes.
        p1 = multiprocessing.Process(
            name="p1",
            target=save_image,
            args=(data[0], data2[0], step, val, group_name),
        )
        step += data_per_proc
        p2 = multiprocessing.Process(
            name="p2",
            target=save_image,
            args=(data[1], data2[1], step, val, group_name),
        )
        step += data_per_proc
        p3 = multiprocessing.Process(
            name="p3",
            target=save_image,
            args=(data[2], data2[2], step, val, group_name),
        )
        # Starting process px.
        p1.start()
        p2.start()
        p3.start()
        # Wait until process px is finished.
        p1.join()
        p2.join()
        p3.join()

        print("--- %s seconds ---" % (time.time() - start_time))
