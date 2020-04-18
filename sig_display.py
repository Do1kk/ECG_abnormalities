from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt


beat_ann = (
    "N",  # Normal beat.
    "L",  # Left bundle branch block beat.
    "R",  # Right bundle branch block beat.
    "A",  # Atrial premature beat.
    "V",  # Premature ventricular contraction.
    "/",  # Paced beat.
)
beat_ann_file = ("N", "L", "R", "A", "V", "Pe")
beat_ann = dict(zip(beat_ann, beat_ann_file))
record_name = "type_"
how_many = 10


fig, axs = plt.subplots(1, 6, figsize=(14, 4), constrained_layout=True)
for index, name in enumerate(beat_ann_file):
    all_data = genfromtxt(
        "csv_type_files/" + record_name + name + ".csv", delimiter=";", max_rows=100
    )
    some_data = all_data[:how_many]
    # axs[index].axis("off")
    axs[index].set_title(name)
    for i in range(how_many):
        axs[index].plot(some_data[i])
plt.show()
