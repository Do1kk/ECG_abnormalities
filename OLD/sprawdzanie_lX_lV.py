from csv_ann_type import beat_ann_dict

from numpy import genfromtxt
import matplotlib.pyplot as plt

# import itertools

l = ("A", "V", "x", "!")
beat_ann_dict = {key: beat_ann_dict[key] for key in l}

record_name = "type_"
how_many = 100
# beat_ann_dict = dict(itertools.islice(beat_ann_dict.items(), 4))
number_of_type = len(beat_ann_dict)

fig, axs = plt.subplots(number_of_type, figsize=(10, 8), constrained_layout=True)
for index, name in enumerate(beat_ann_dict.values()):
    all_data = genfromtxt(
        "csv_type_files/" + record_name + name + ".csv", delimiter=";", max_rows=100
    )
    some_data = all_data[:how_many]
    image_f_name = "type_" + name + "/"
    axs[index].set_title(name)

    for i in range(how_many):
        axs[index].plot(some_data[i])
        axs[index].axis("off")
plt.show()
