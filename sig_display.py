from png_spec import beat_ann_dict

from numpy import genfromtxt
import matplotlib.pyplot as plt
import imageio

record_name = "type_"
images_folder = "images/"
how_many = 2
number_of_type = len(beat_ann_dict)

fig, axs = plt.subplots(2, number_of_type, figsize=(17, 5), constrained_layout=True)
axs[0, 0].set_ylabel("10 przykładowych przebiegów")
for index, name in enumerate(beat_ann_dict.values()):
    all_data = genfromtxt(
        "csv_type_files/" + record_name + name + ".csv", delimiter=";", max_rows=2
    )
    some_data = all_data[:how_many]
    image_f_name = "type_" + name + "/"
    im = imageio.imread(images_folder + image_f_name + "0" + name + ".png")[:, :, :3]
    axs[0, index].set_title(name)

    for i in range(how_many):
        axs[0, index].plot(some_data[i])
    axs[1, index].axis("off")
    axs[1, index].set_title("spekr.")
    axs[1, index].imshow(im)
plt.show()
